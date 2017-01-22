class Word:
    '''A representation of a word, containing multiple Segments.'''

    def __init__(self, segments):
        self.segments = segments

    def index_applicable(self, index, rule):
        '''Given an index and a rule, check if the segment at the given index
        meets the conditions of the current rule.'''

        # Store the results of each check
        valid = {}

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

        return any([self.index_applicable(i, rule) for i in
                    range(len(self.segments))])
