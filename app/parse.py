def valid_subword(subword, available_segments, available_diacritics):
    '''Determines whether a string is a valid IPA segment.'''

    # If it's a simple IPA sequence, return True
    if subword in available_segments:
        return True

    # Iterate through the string, slicing at each index. If the first part is
    # an IPA sequence and the second half is entirely made up of diacritics,
    # it's valid.
    for i in range(1, len(subword)):
        if subword[:i] in available_segments and all([x in available_diacritics
                                                      for x in subword[i:]]):
            return True
    else:
        return False


def tokenise(word, available_segments, available_diacritics):
    '''Recursively tokenise a string of IPA characters, with support for diacritics
    and digraphs. Example: bok͡piʰ becomes ["b", "o", "k͡p", "iʰ"].

    '''

    # The end condition for the recursion: an empty string.
    if len(word) == 0:
        return []

    # Iterate through substrings of the word, removing one letter at a time
    # from the end
    for length in range(len(word), -1, -1):
        subword = word[:length]

        # If the current substring is a valid sequence in IPA, add it to the
        # results list and recur
        if valid_subword(subword, available_segments, available_diacritics):
            return [subword] + tokenise(word[length:], available_segments,
                                        available_diacritics)

    raise ValueError('Invalid character in word: {0}'.format(word))
