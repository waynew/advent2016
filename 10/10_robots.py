from collections import defaultdict, namedtuple

instructions = '''
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
'''.strip().split('\n')


class Bin:
    def __init__(self, bin_id):
        self.id = bin_id
        self.values = []

    def receive_chip(self, value):
        self.values.append(value)


class Give:
    def __init__(self, chip_A_type, chip_A_output, chip_B_type, chip_B_output):
        if chip_A_type == 'low':
            self.low_output = chip_A_output
            self.high_output = chip_B_output
        else:
            self.low_output = chip_B_output
            self.high_output = chip_A_output

    def __repr__(self):
        return 'Give high to {} {} and low to {} {}'.format(
            type(self.high_output),
            self.high_output.id,
            type(self.low_output),
            self.low_output.id,
        )

    def give_high(self, value):
        self.high_output.receive_chip(value)

    def give_low(self, value):
        self.low_output.receive_chip(value)


class Robot:
    def __init__(self, robot_id):
        self.id = robot_id
        self.instructions = []
        self.values = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def receive_chip(self, value):
        self.values.append(value)
        if len(self.values) > 1:
            self.process_instructions()

    def process_instructions(self):
        while self.instructions and self.values:
            instruction = self.instructions.pop(0)
            print('{} processing {}'.format(self.id, instruction))
            instruction.give_high(self.high_value)
            instruction.give_low(self.low_value)
            self.values.remove(self.high_value)
            self.values.remove(self.low_value)
            print(self.values)

    @property
    def high_value(self):
        return max(self.values)

    @property
    def low_value(self):
        return min(self.values)


class RobotFactory:
    robots = {}
    bins = {}

    @classmethod
    def get_robot(cls, robot_id):
        robot = cls.robots.get(robot_id, Robot(robot_id))
        cls.robots[robot_id] = robot
        return robot

    @classmethod
    def get_bin(cls, bin_id):
        output_bin = cls.bins.get(bin_id, Bin(bin_id))
        cls.bins[bin_id] = output_bin
        return output_bin
        

class Output:
    def __init__(self):
        self.values = []


def parse_val_instruction(instruction):
    instruction = instruction.split()
    return instruction[1], instruction[-1]


def parse_give_instruction(instruction):
    instruction = instruction.split()
    from_ = instruction[1]
    to_one_chip_type = instruction[3]
    to_one_output_type = instruction[5]
    to_one_output_id = instruction[6]

    to_two_chip_type = instruction[8]
    to_two_output_type = instruction[10]
    to_two_output_id = instruction[11]
    if to_one_output_type == 'bot':
        a_output = RobotFactory.get_robot(to_one_output_id)
    else:
        a_output = RobotFactory.get_bin(to_one_output_id)

    if to_two_output_type == 'bot':
        b_output = RobotFactory.get_robot(to_two_output_id)
    else:
        b_output = RobotFactory.get_bin(to_two_output_id)

    return from_, Give(
        to_one_chip_type,
        a_output,
        to_two_chip_type,
        b_output,
    )


def process(instructions):
    for instruction in instructions:
        if instruction.startswith('value'):
            val, bot_id = parse_val_instruction(instruction)
            robot = RobotFactory.get_robot(bot_id)
            robot.receive_chip(val)
        elif instruction.startswith('bot'):
            robot_id, instruction = parse_give_instruction(instruction)
            robot = RobotFactory.get_robot(bot_id)
            robot.add_instruction(instruction)
        else:
            assert False, 'Unknown instruction type '+instruction

    import pprint; 
    print('Robots:')
    for robot_id in RobotFactory.robots:
        print('\t',robot_id, RobotFactory.robots[robot_id].values)

    print('Bins:')
    for bin_id in RobotFactory.bins:
        print('\t',bin_id, RobotFactory.bins[bin_id].values)

    print('robots: ', pprint.pformat(RobotFactory.robots))
    print('Output bins: ', pprint.pformat(RobotFactory.bins))

process(instructions)
