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


def evolve(words, rules):
    '''Evolve a list of Words, returning the applied rule and the new list of
    Words.'''
    pass


