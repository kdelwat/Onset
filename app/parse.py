from segment import Segment


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


def find_segment(string, available_segments):
    '''Search the segment dictionary for the segment with the correct IPA
    string.'''
    return [segment for segment in available_segments
            if segment['IPA'] == string][0]


def token_to_segment(token, segment_list, diacritic_list):
    '''Converts a string token in IPA to Segment object, given
    a list of dictionaries representing segments and the same representing
    diacritics.'''

    available_diacritics = [segment['IPA'] for segment in diacritic_list]

    # Isolate the base IPA segment string
    base_string = ''.join(filter(lambda x: x not in available_diacritics,
                                 token))

    # Isolate an iterable of diacritics
    diacritics = filter(lambda x: x in available_diacritics, token)

    # Initialise the base Segment
    segment = Segment.from_dictionary(find_segment(base_string,
                                                   segment_list))

    # Add each diacritic to the segment
    for diacritic in diacritics:
        segment += Segment.from_dictionary(find_segment(diacritic,
                                                        diacritic_list))

    return segment
