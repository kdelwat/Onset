def filter_rules(words, rules):
    '''Given a list of words and a list of rules, return only those rules which are
    applicable to the given words.

    '''
    return [rule for rule in rules
            if any([word.applicable(rule) for word in words])]


def evolve(words, rules):
    '''Evolve a list of Words, returning the applied rule and the new list of
    Words.'''
    pass


