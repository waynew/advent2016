import io
import logging

logger = logging.getLogger(__name__)


def read_marker(data):
    marker = ''
    while True:
        byte = data.read(1)
        if byte == ')':
            length, times = [int(x) for x in marker.split('x')]
            return length, times
        else:
            marker += byte


def decompress(data, version=1, checksum_only=False, show_progress=False):
    '''
    Usage:
    >>> import io
    >>> data = decompress(io.StringIO('ADVENT'))
    >>> len(data)
    6
    >>> data
    'ADVENT'
    >>> data = decompress(io.StringIO('A(1x5)BC'))
    >>> data
    'ABBBBBC'
    >>> len(data)
    7
    >>> data = decompress(io.StringIO('(3x3)XYZ'))
    >>> data
    'XYZXYZXYZ'
    >>> len(data)
    9
    >>> data = decompress(io.StringIO('A(2x2)BCD(2x2)EFG'))
    >>> data
    'ABCBCDEFEFG'
    >>> len(data)
    11
    >>> data = decompress(io.StringIO('(6x1)(1x3)A'))
    >>> data
    '(1x3)A'
    >>> len(data)
    6
    >>> decompress(io.StringIO('X(8x2)(3x3)ABCY'))
    'X(3x3)ABC(3x3)ABCY'
    >>> decompress(io.StringIO('(3x3)XYZ'), 2)[0]
    'XYZXYZXYZ'
    >>> decompress(io.StringIO('X(8x2)(3x3)ABCY'), 2)[0]
    'XABCABCABCABCABCABCY'
    >>> a_lot, checksum = decompress(io.StringIO('(27x12)(20x12)(13x14)(7x10)(1x12)A'), 2)
    >>> a_lot == 'A'*checksum
    True
    >>> checksum
    241920
    >>> decompress(io.StringIO('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'), 2, checksum_only=True)
    445
    '''

    response = io.StringIO()
    in_marker = False
    byte = ''
    checksum = 0
    update_factor = 100
    next_update_point = 0

    while True:
        last_byte = byte
        byte = data.read(1)
        if byte.isspace():
            continue
        elif byte == '(':
            length, times = read_marker(data)
            to_decompress = data.read(length)
            if version == 1:
                checksum += len(to_decompress)*times
                if not checksum_only:
                    response.write(to_decompress*times)
            elif version == 2:
                if checksum_only:
                    checksum += decompress(io.StringIO(to_decompress), version=2, checksum_only=True, show_progress=show_progress)*times
                else:
                    logger.debug('Decompressing %r', to_decompress)
                    decompressed, other_checksum = decompress(io.StringIO(to_decompress), version=2, show_progress=show_progress)
                    checksum += other_checksum*times
                    response.write(decompressed*times)
        else:
            checksum += len(byte)
            logger.debug('Checksum: %r Byte: %r', checksum, byte)
            if not checksum_only:
                response.write(byte)

        if show_progress:
            if checksum > next_update_point:
                next_update_point += update_factor
                print(checksum, end='\r')
            #print(checksum > next_update_point, end='\r')

        if not byte:
            logger.debug('Return checksum %r', checksum)
            file_end = response.tell()
            response.seek(0)
            if version == 2:
                if checksum_only:
                    return checksum
                else:
                    assert file_end == checksum, '{} == {}'.format(file_end, checksum)
                    return response.read(), checksum
            else:
                return response.read()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import time
    start = time.time()
    with open('input.txt') as f:
        out = decompress(f)
        print('Part 1: ', len(out))

        f.seek(0)
        print('Part 2: ', decompress(f, version=2, checksum_only=True, show_progress=True))
    print('Took {:.2f}s'.format(time.time()-start))
