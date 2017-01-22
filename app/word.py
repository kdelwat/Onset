class Word:
    '''A representation of a word, containing multiple Segments.'''

    def __init__(self, segments):
        self.segments = segments

    @staticmethod
    def overlapping_chunks(segment_list, size):
        '''Given a list, returns a generator of lists, where each list has length
        size and overlaps with the previous list except for its final item.

        For example, [1, 2, 3, 4, 5] chunked with length 3 would give:

            [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

        '''
        for x in range(0, len(segment_list) - size + 1):
            yield tuple(segment_list[x:x + size])

    def applicable(self, rule):
        '''Returns True if any segment in the word meets all conditions of the
        given rule.'''

        # When before and after conditions are both present, check all three
        if 'before' in rule and 'after' in rule:
            chunks = self.overlapping_chunks(self.segments, 3)
            for before, current, after in chunks:
                if all([before.meets_conditions(rule['before']),
                        current.meets_conditions(rule['conditions']),
                        after.meets_conditions(rule['after'])]):
                    return True

        # When before conditions are present, check that and the current
        # conditions
        elif 'before' in rule:
            chunks = self.overlapping_chunks(self.segments, 2)
            for before, current in chunks:
                if all([before.meets_conditions(rule['before']),
                        current.meets_conditions(rule['conditions'])]):
                    return True

        # When after conditions are present, check that and the current
        # conditions
        elif 'after' in rule:
            chunks = self.overlapping_chunks(self.segments, 2)
            for current, after in chunks:
                if all([current.meets_conditions(rule['conditions']),
                        after.meets_conditions(rule['after'])]):
                    return True

        # Otherwise, just check each current segment
        else:
            for current in self.segments:
                if current.meets_conditions(rule['conditions']):
                    return True

        # If none of the segments met the conditions, return False
        return False
