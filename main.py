from itertools import takewhile

from table import Table

PULMONIC = Table('pulmonic.csv')

def load_rules(filename):
    '''Loads a list of rules, in the following format:

    [label1]
    x:y
    z:a

    [label2]
    b:c

    which would become:

    {'label1': (x, y) ..., 'label2': (b,c)}'''

    # Read stripped, non-blank lines into list
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() != '']

    # Iterate through list, splitting on labels
    rules_list = []
    current_rule = [lines[0][1:-1]]

    for item in lines[1:]:
        if item[0] == '[':
            rules_list.append(current_rule)
            current_rule = [item[1:-1]]
        else:
            current_rule.append(tuple(item.split(':')))
    rules_list.append(current_rule)

    # Convert rule list to dictionary
    rules = {}
    for rule in rules_list:
        rules[rule[0]] = rule[1:]

    return rules

def main():
    rules = load_rules('rules.txt')

if __name__ == '__main__':
    main()
