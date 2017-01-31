from segment import Segment
from word import Word


def parse_words(strings, segments, diacritics):
    '''Given a list of word strings (in IPA), return a list of Word objects
    containing parsed segments. Use the given list of segment dictionaries and
    diacritic rules.

    '''

    # Create two lists of available segments and diacritics
    segment_strings = [segment['IPA'] for segment in segments]
    diacritic_strings = [diacritic['IPA'] for diacritic in diacritics]

    words = []

    for word in strings:
        try:
            tokens = tokenise(word, segment_strings, diacritic_strings)
        except ValueError as subword:
            error = ('Error parsing word: {0}. There was an unknown character '
                     'in the subword: {1}')
            raise ValueError(error.format(word, subword))

        parsed_segments = [token_to_segment(token, segments, diacritics) for
                           token in tokens]
        words.append(Word(parsed_segments))

    return words


def valid_subword(subword, segment_strings, diacritic_strings):
    '''Determines whether a string is a valid IPA segment.'''

    # If it's a simple IPA sequence, return True
    if subword in segment_strings:
        return True

    # Iterate through the string, slicing at each index. If the first part is
    # an IPA sequence and the second half is entirely made up of diacritics,
    # it's valid.
    for i in range(1, len(subword)):
        if subword[:i] in segment_strings and all([x in diacritic_strings
                                                      for x in subword[i:]]):
            return True
    else:
        return False


def tokenise(word, segment_strings, diacritic_strings):
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
        if valid_subword(subword, segment_strings, diacritic_strings):
            return [subword] + tokenise(word[length:], segment_strings,
                                        diacritic_strings)

    raise ValueError(word)


def find_segment(string, segment_strings):
    '''Search the segment dictionary for the segment with the correct IPA
    string.'''
    return [segment for segment in segment_strings
            if segment['IPA'] == string][0]


def token_to_segment(token, segment_list, diacritic_list):
    '''Converts a string token in IPA to Segment object, given
    a list of dictionaries representing segments and the same representing
    diacritics.'''

    diacritic_strings = [segment['IPA'] for segment in diacritic_list]

    # Isolate the base IPA segment string
    base_string = ''.join(filter(lambda x: x not in diacritic_strings,
                                 token))

    # Isolate an iterable of diacritics present
    diacritics = [diacritic for diacritic in diacritic_list
                  if diacritic['IPA'] in token]

    # Initialise the base Segment
    segment = Segment.from_dictionary(find_segment(base_string,
                                                   segment_list))

    # Add each diacritic feature to the segment
    for diacritic in diacritics:
        diacritic_segment = Segment(diacritic['applies'].get('positive', []),
                                    diacritic['applies'].get('negative', []))
        segment = segment + diacritic_segment

    return segment
