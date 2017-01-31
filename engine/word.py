from segment import Segment


class Word:
    '''A representation of a word, containing multiple Segments.'''

    def __init__(self, segments):
        self.segments = segments

    def __eq__(self, other):
        '''Compares Word objects by ensuring each segment is equal.'''

        # If the two words aren't the same length, they are automatically
        # inequal.
        if len(self.segments) != len(other.segments):
            return False

        for own_segment, other_segment in zip(self.segments, other.segments):
            positive_match = (set(own_segment.positive) ==
                              set(other_segment.positive))
            negative_match = (set(own_segment.negative) ==
                              set(other_segment.negative))

            if not positive_match or not negative_match:
                return False

        return True

    def index_applicable(self, index, rule):
        '''Given an index and a rule, check if the segment at the given index
        meets the conditions of the current rule.'''

        # Store the results of each check
        valid = {}

        # Break out if the segment does not obey optional first/last
        # indicators.
        if 'first' in rule:
            if rule['first']:
                if index != 0:
                    return False
            else:
                if index == 0:
                    return False

        if 'last' in rule:
            if rule['last']:
                if index != len(self.segments) - 1:
                    return False
            else:
                if index == len(self.segments) - 1:
                    return False

        if 'before' in rule:
            if index == 0:
                return False

            before_segment = self.segments[index - 1]
            valid['before'] = before_segment.meets_conditions(rule['before'])

        if 'after' in rule:
            if index == len(self.segments) - 1:
                return False

            after_segment = self.segments[index + 1]
            valid['after'] = after_segment.meets_conditions(rule['after'])

        current_segment = self.segments[index]
        valid['current'] = current_segment.meets_conditions(rule['conditions'])

        return all(valid.values())

    def applicable(self, rule):
        '''Returns True if any segment in the word meets all conditions of the
        given rule.'''

        return any(self.index_applicable(i, rule) for i in
                   range(len(self.segments)))

    def apply_rule(self, rule):
        '''Apply the given rule to the current Segments, returning a new Word.'''
        new_segments = []

        # Create a Segment from the rule to add to current segments
        rule_segment = Segment(rule['applies'].get('positive', []),
                               rule['applies'].get('negative', []))

        for i in range(len(self.segments)):
            if self.index_applicable(i, rule):
                # If the rule contains the deletion feature, don't add the new
                # segment, effectively removing it entirely. Otherwise, add the
                # modified segment.
                if 'deletion' not in rule['applies'].get('positive', []):
                    new_segments.append(self.segments[i] + rule_segment)

            else:
                new_segments.append(self.segments[i])

        return Word(new_segments)
