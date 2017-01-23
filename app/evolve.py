from collections import defaultdict

import metrics


def filter_rules(words, rules):
    '''Given a list of words and a list of rules, return only those rules which are
    applicable to the given words.

    '''
    return [rule for rule in rules
            if any([word.applicable(rule) for word in words])]


def apply_rules(words, rules):
    '''Given a list of words and a list of rules, return a list of tuples. The
    first value of each tuple is the rule applied, while the second is the list
    of words with that rule applied.

    '''
    results = []

    for rule in rules:
        results.append((rule, [word.apply_rule(rule) for word in words]))

    return results


def average_metric_value(words, metric):
    '''Apply the metric function to each word in words, returning the average
    result.'''
    return sum(map(metric, words)) / len(words)


def optimal_rule_pair(rule_pairs, metric, optimisation_function=min):
    '''Given a list of tuples of form (rule, words), rank each pair according to
    the given metric function. Return the rule and words which are first when
    ranked using the optimisation function.

    '''
    ranked_pairs = defaultdict(list)

    # Add each pair to the dictionary with the key given by the average metric
    # value of the words.
    for rule, words in rule_pairs:
        ranked_pairs[average_metric_value(words, metric)].append((rule, words))

    # If there is more than one pair for the best metric value, return the
    # first
    return ranked_pairs[optimisation_function(ranked_pairs.keys())][0]


def evolve(words, rules):
    '''Evolve a list of Words, returning the applied rule and the new list of
    Words.'''

    rules = filter_rules(words, rules)

    # If there are no applicable rules, inform the evolution controller
    if len(rules) == 0:
        raise StopIteration

    rule_pairs = apply_rules(words, rules)

    return optimal_rule_pair(rule_pairs, metrics.phonetic_product)
