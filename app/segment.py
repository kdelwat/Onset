class Segment:
    '''A representation of a phonetic segment, stored in terms of features.'''

    def __init__(self, positive, negative):
        self._positive = positive
        self._negative = negative

    @classmethod
    def from_dictionary(cls, feature_dictionary):
        '''Initialise the segment from a dictionary of features. The feature name
        is the key, and the value is one of '+', '-', or '0'. The only ignored
        key is "IPA".'''

        positive = [key for key, value in feature_dictionary.items()
                    if value == '+']
        negative = [key for key, value in feature_dictionary.items()
                    if value == '-']

        return cls(positive, negative)

    @property
    def positive(self):
        return self._positive

    def add_positive(self, feature):
        '''Add the feature to the positive list. If it already exists in the
        negative list, remove it from negative.'''

        if feature not in self._positive:
            if feature in self._negative:
                self._negative.remove(feature)

            self._positive.append(feature)

    @property
    def negative(self):
        return self._negative

    def add_negative(self, feature):
        '''Add the feature to the negative list. If it already exists in the
        positive list, remove it from positive.'''

        if feature not in self._negative:
            if feature in self._positive:
                self._positive.remove(feature)

            self._negative.append(feature)

    @property
    def diacritics(self):
        '''Return all diacritic features on the segment.'''
        diacritic_features = {'dsyllabic',
                              'creaky',
                              'breathy',
                              'voiceless',
                              'dental',
                              'frontedvelar',
                              'backedvelar',
                              'lengthened',
                              'aspirated',
                              'palatalized',
                              'labialized',
                              'velarized',
                              'pharyngealized',
                              'nasalized',
                              'rhotic',
                              'ejective'}

        return set(self._positive).intersection(diacritic_features)

    def meets_conditions(self, conditions):
        '''Takes a dictionary of features, in the format:

            {'positive': ['feature1', 'feature2'], 'negative': ['feature3']}

        Returns True if all features specified as positive are in
        self._positive and those specified as negative are in self._negative.
        Otherwise returns false.

        '''
        return (set(conditions.get('positive', [])).issubset(self._positive)
                and set(conditions.get('negative', [])).issubset(self._negative))

    def __add__(self, other):
        '''Override the regular addition behaviour. When two segments are added
        together, the values of the second override those of the first that
        differ.'''
        for positive_feature in other.positive:
            self.add_positive(positive_feature)

        for negative_feature in other.negative:
            self.add_negative(negative_feature)

        return self
