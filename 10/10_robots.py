from collections import defaultdict, namedtuple

instructions = '''
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
'''.strip().split('\n')

instructions = [line.strip() for line in open('input.txt')]


class Bot:
    def __init__(self, id):
        self.id = id
        self.values = []
        self.instructions = []

    def have_this_chip(self, chip):
        self.values.append(chip)
        self.values.sort()
        if len(self.values) > 1:
            if self.values == [17, 61]:
                print('I am the one who knocks 2 and 5 chips', self.id)
            while self.instructions:
                instruction = self.instructions.pop(0).split()
                _, _, _, low_or_high, _, where_one, where_one_id, _, _, _, where_two, where_two_id = instruction
                where_one_id = int(where_one_id)
                where_two_id = int(where_two_id)
                if low_or_high == 'low':
                    one_chip, two_chip = self.values
                else:
                    two_chip, one_chip = self.values
                self.values.clear()

                if where_one == 'bot':
                    Factory.get_bot(where_one_id).have_this_chip(one_chip)
                else:
                    Factory.get_bin(where_one_id).have_this_chip(one_chip)

                if where_two == 'bot':
                    Factory.get_bot(where_two_id).have_this_chip(two_chip)
                else:
                    Factory.get_bin(where_two_id).have_this_chip(two_chip)


class Factory:
    bots = {}
    bins = {}
    
    @staticmethod
    def get_bot(id):
        bot = Factory.bots.get(id)
        if bot is None:
            bot = Bot(id)
        Factory.bots[id] = bot
        return bot
    
    @staticmethod
    def get_bin(id):
        bin = Factory.bins.get(id)
        if bin is None:
            bin = Bot(id)
        Factory.bins[id] = bin
        return bin


def process(instructions):
    chips = {}
    bots = {}
    for instruction in instructions:
        if instruction.startswith('bot'):
            bot_id = int(instruction.split(None, 2)[1])
            bot = Factory.get_bot(bot_id)
            bot.instructions.append(instruction)
    for instruction in instructions:
        if instruction.startswith('value'):
            _, val, _, _, _, bot_id = instruction.split()
            chip, bot_id = int(val), int(bot_id)
            bot = Factory.get_bot(bot_id)
            bot.have_this_chip(chip)

def foo():
    print('Bots:')
    for bot_id in Factory.bots:
        print(bot_id)
        for val in Factory.bots[bot_id].values:
            print('\t', val)

    print('Bins:')
    for bin_id in Factory.bins:
        print(bin_id)
        for val in Factory.bins[bin_id].values:
            print('\t', val)

process(instructions)
values = []
for id in (0, 1, 2):
    values.extend(Factory.bins[id].values)
print(values[0]*values[1]*values[2])
