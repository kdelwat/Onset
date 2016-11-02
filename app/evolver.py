import selector
import applier

from rules import rules

words = ['oxxaotatop', 'tobapɸcɒ', 'pɸxxtabasco']


def evolve(words, generations=5, rewrite_rules=[]):
    '''Evolves the language specified by:

        words: list [strings]

    for the given number of generations. One sound change is applied per
    generation.'''

    for _ in range(generations):
        sound_change = selector.select_rule(words, rules)
        print(sound_change)
        words = applier.apply_rule(words, sound_change)

    return words

if __name__ == '__main__':
    print(evolve(words, 3))


