import io

def read_marker(data):
    marker = ''
    while True:
        byte = data.read(1)
        if byte == ')':
            length, times = [int(x) for x in marker.split('x')]
            return length, times
        else:
            marker += byte


def decompress(data):
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
    >>> data = decompress(io.StringIO('X(8x2)(3x3)ABCY'))
    >>> data
    'X(3x3)ABC(3x3)ABCY'
    >>> len(data)
    18
    '''

    response = io.StringIO()
    in_marker = False
    byte = ''

    while True:
        last_byte = byte
        byte = data.read(1)
        if byte == '(':
            length, times = read_marker(data)
            response.write(data.read(length)*times)
        else:
            response.write(byte)
        if not byte:
            if last_byte == '\n':
                response.seek(response.tell()-1)
                response.truncate()
            response.seek(0)
            return response.read()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    print()
    print(decompress(io.StringIO('A(1x5)BC')))
    with open('input.txt') as f:
        out = decompress(f)
        print(len(out))
