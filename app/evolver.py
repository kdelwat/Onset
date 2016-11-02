import app.selector as selector
import app.applier as applier

from app.rules import rules


def rule_representation(rule):
    '''Takes a Rule and returns a list of strings which represent it, in the
    form [name, target, replacement, environment]'''
    return [rule.name, rule.target, rule.replacement, rule.environments[0][1]]


def evolve(words, generations=5, rewrite_rules=[]):
    '''Evolves the language specified by:

        words: list [strings]

    for the given number of generations. One sound change is applied per
    generation.'''

    changes = []

    for _ in range(generations):

        # Try to select a valid rule
        try:
            sound_change = selector.select_rule(words, rules)
        # If there aren't any, finish early by breaking from the loop.
        except ValueError:
            break

        changes.append(rule_representation(sound_change))
        print(sound_change)
        words = applier.apply_rule(words, sound_change)

    return words, changes
