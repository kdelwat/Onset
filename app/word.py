class Word:
    '''A representation of a word, containing multiple Segments.'''

    def applicable(self, rule):

        '''Returns True if the word meets all conditions of the given rule.'''

        pass
    def __init__(self, segments):
        self.segments = segments

    @staticmethod
    def overlapping_chunks(segment_list, size):
        '''Given a list, returns a list of lists, where each sublist has length
        size and overlaps with the previous list except for its final item.

        For example, [1, 2, 3, 4, 5] chunked with length 3 would give:

            [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

        '''
        return [segment_list[x: x + size] for x in range(0, len(segment_list) -
                                                         size + 1)]

