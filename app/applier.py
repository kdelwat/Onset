import regex as re

def apply_rule(words, rule):
    '''Applies the given rule to the list of words.'''

    # Combine the word list into one string, separated by newlines, to speed up
    # regex search.
    combined_words = '\n'.join(words)

    # Get the environments before and after the placeholder (.) which will be
    # the spot where phonemes are replaced.
    before, after = rule.environments[0].split('.')

    # Make the substitution for each target - replacement pair in dictionary.
    for target, replacement in rule.changes.items():
        regex = '(?<={0}){1}(?={2})'.format(before, target, after)
        print(regex)
        combined_words = re.sub(regex, replacement, combined_words,
                                flags=re.MULTILINE)

    # Return the split word list.
    return combined_words.split('\n')
