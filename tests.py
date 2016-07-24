import unittest

from app.evolve import apply_rule

class TestApplyRule(unittest.TestCase):

    def test_intra_word(self):
        # Should be substitution
        self.assertEqual(apply_rule('abcde', ('c', 'x', '_')), 'abxde')
        self.assertEqual(apply_rule('abcde', ('c', 'x', 'b_')), 'abxde')
        self.assertEqual(apply_rule('abcde', ('c', 'x', '_d')), 'abxde')
        self.assertEqual(apply_rule('abcde', ('c', 'x', 'b_d')), 'abxde')
        self.assertEqual(apply_rule('abcde', ('c', 'x', 'ab_de')), 'abxde')

        self.assertEqual(apply_rule('abcde', ('c', 'xyz', 'ab_de')), 'abxyzde')

        self.assertEqual(apply_rule('abcde', ('cd', 'x', '_')), 'abxe')

        # Shouldn't be substitution
        self.assertEqual(apply_rule('abcde', ('c', 'x', 'a_')), 'abcde')
        self.assertEqual(apply_rule('abcde', ('c', 'x', 'a_d')), 'abcde')

        self.assertEqual(apply_rule('abcde', ('c', 'xyz', 'a_')), 'abcde')
        self.assertEqual(apply_rule('abcde', ('c', 'xyz', 'a_d')), 'abcde')

        # Deletion
        self.assertEqual(apply_rule('abcde', ('c', '', '_')), 'abde')

    def test_beginning(self):
        # Should be substitution
        self.assertEqual(apply_rule('abcde', ('a', 'x', '^_')), 'xbcde')
        self.assertEqual(apply_rule('abcde', ('a', 'x', '^_b')), 'xbcde')
        self.assertEqual(apply_rule('abcde', ('a', 'x', '^_bc')), 'xbcde')

        # Shouldn't be substitution
        self.assertEqual(apply_rule('abcde', ('b', 'x', '^_')), 'abcde')

        # Deletion
        self.assertEqual(apply_rule('abcde', ('a', '', '^_')), 'bcde')
        self.assertEqual(apply_rule('abcde', ('a', '', '^_b')), 'bcde')

    def test_beginning_multi(self):
        self.assertEqual(apply_rule('abcde', ('ab', 'x', '^_')), 'xcde')
        self.assertEqual(apply_rule('abcde', ('ab', 'x', '^_c')), 'xcde')

        self.assertEqual(apply_rule('abcde', ('a', 'xyz', '^_')), 'xyzbcde')
        self.assertEqual(apply_rule('abcde', ('a', 'xyz', '^_b')), 'xyzbcde')

        # Deletion
        self.assertEqual(apply_rule('abcde', ('ab', '', '^_')), 'cde')

    def test_ending(self):
        # Should be substitution
        self.assertEqual(apply_rule('abcde', ('e', 'x', '_$')), 'abcdx')
        self.assertEqual(apply_rule('abcde', ('e', 'x', 'd_$')), 'abcdx')
        self.assertEqual(apply_rule('abcde', ('e', 'x', 'cd_$')), 'abcdx')

        # Shouldn't be substitution
        self.assertEqual(apply_rule('abcde', ('d', 'x', '_$')), 'abcde')

        # Deletion
        self.assertEqual(apply_rule('abcde', ('e', '', '_$')), 'abcd')

    def test_ending_multi(self):
        # Should be substitution
        self.assertEqual(apply_rule('abcde', ('de', 'x', '_$')), 'abcx')
        self.assertEqual(apply_rule('abcde', ('de', 'x', 'c_$')), 'abcx')

        self.assertEqual(apply_rule('abcde', ('e', 'xyz', '_$')), 'abcdxyz')
        self.assertEqual(apply_rule('abcde', ('e', 'xyz', 'd_$')), 'abcdxyz')

        # Deletion
        self.assertEqual(apply_rule('abcde', ('de', '', '_$')), 'abc')

if __name__=='__main__':
    unittest.main()
