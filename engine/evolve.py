from collections import defaultdict

import metrics


def filter_rules(words, rules):
    '''Given a list of words and a list of rules, return only those rules which are
    applicable to the given words.

    '''
    return [rule for rule in rules
            if any(word.applicable(rule) for word in words)]


def get_metric_from_words(words, rule, metric):
    '''Given a list of words and a rule, apply the rule to the words. Return the
    value of the metric applied to the new rules.'''

    return average_metric_value([word.apply_rule(rule) for word in words],
                                metric)


def average_metric_value(words, metric):
    '''Apply the metric function to each word in words, returning the average
    result.'''
    return sum(map(metric, words)) / len(words)


def evolve(words, rules, metric, optimisation_function):
    '''Evolve a list of Words, returning the applied rule and the new list of
    Words.'''

    rules = filter_rules(words, rules)

    # If there are no applicable rules, inform the evolution controller
    if len(rules) == 0:
        raise StopIteration

    # Establish a baseline for evolution effectiveness using the first
    # available rule.
    best_rule = rules[0]
    best_metric = get_metric_from_words(words, rules[0], metric)

    # Loop through the rest of the rules. If a rule is better than the
    # current best, it becomes the new best.
    for rule in rules[1:]:
        new_metric = get_metric_from_words(words, rule, metric)

        if optimisation_function(new_metric, best_metric) == new_metric:
            best_metric = new_metric
            best_rule = rule

    # Return the best rule and the words with the best rule applied
    return best_rule, [word.apply_rule(best_rule) for word in words]
