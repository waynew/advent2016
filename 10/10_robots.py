from collections import defaultdict, namedtuple

instructions = '''
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
'''.strip().split('\n')


Robot = namedtuple('Robot', 'id,instructions,values')
Give = namedtuple('Give', ('from_id',
                           'one_chip_type',
                           'one_output_type',
                           'one_output_id',
                           'two_chip_type',
                           'two_output_type',
                           'two_output_id',
                           ))

class RobotFactory:
    robots = {}

    @classmethod
    def get_robot(cls, robot_id):
        robot = cls.robots.get(robot_id, Robot(robot_id))
        cls.robots[robot_id] = robot
        return robot


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
    return Give(
        from_,
        to_one_chip_type,
        to_one_output_type,
        to_one_output_id,
        to_two_chip_type,
        to_two_output_type,
        to_two_output_id,
    )


def process(instructions):
    robots = {}
    outputs = defaultdict(Output)
    for instruction in instructions:
        print(instruction)
        if instruction.startswith('value'):
            val, bot_id = parse_val_instruction(instruction)
            robot = robots.get(bot_id, Robot(bot_id, [], []))
            robots[robot.id] = robot
            robot.values.append(val)
        elif instruction.startswith('bot'):
            instruction = parse_give_instruction(instruction)
            robot = robots.get(instruction.from_id, Robot(bot_id, [], []))
            robots[instruction.from_id] = robot
            robot.instructions.append(instruction)
        else:
            assert False, 'Unknown instruction type '+instruction

        for id in robots:
            robot = robots[id]
            print(robot.id)
            if len(robot.values) > 1:
                for instruction in robot.instructions:
                    print(instruction)
#                if instruction.one_chip_type == 'low':
#                    if instruction == 'low':
#                        chip_one = min(robot['values'])
#                        chip_two = max(robot['values'])
#                    else:
#                        chip_two = min(robot['values'])
#                        chip_one = max(robot['values'])
#                    robot['values'].remove(chip_one)
#                    robot['values'].remove(chip_two)
#
#                    if instruction[2] == 'bot':
#                        robots[instruction[3]]['values'].append(chip_one)
#                    else:
#                        outputs[instruction[3]]['values'].append(chip_one)
#
#                    if instruction[5] == 'bot':
#                        robots[instruction[3]]['values'].append(chip_two)
#                    else:
#                        outputs[instruction[3]]['values'].append(chip_two)
#
    import pprint; 
    print('robots: ', pprint.pformat(robots))
#    print('outputs: ', pprint.pformat(dict(outputs)))
#    print()
#

process(instructions)
