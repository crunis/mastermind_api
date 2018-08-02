import unittest, re
from mastermind import remove_char, compute_answer, generate_code

class TestMastermind(unittest.TestCase):
    def test_remove_char(self):
        self.assertEqual(remove_char("12345", 0), "2345")
        self.assertEqual(remove_char("12345", 2), "1245")
        self.assertEqual(remove_char("12345", 4), "1234")
        self.assertRaises(IndexError, remove_char, "12345", 5)
        
    def test_compute_answer(self):
        self.assertEqual(compute_answer("123","144"),   [1,0])
        self.assertEqual(compute_answer("123","444"),   [0,0])
        self.assertEqual(compute_answer("123","124"),   [2,0])
        self.assertEqual(compute_answer("1234","1244"), [3,0])
        self.assertEqual(compute_answer("1234","4555"), [0,1])
        self.assertRaises(ValueError, compute_answer, "12345", "1234")

    def test_generate_code(self):
        length = 15
        code = generate_code(length, "12345")
        self.assertEqual(len(code), length)
        p = re.compile('[12345]*')
        self.assertEqual(len(p.match(code).group()), length)

if __name__ == '__main__':
    unittest.main()