import unittest
from preprocessing import clean_text  # importer la fonction depuis preprocessing.py

class TestCleanText(unittest.TestCase):
    def test_basic_text(self):
        text = "This is a simple test."
        result = clean_text(text)
        expected_words = ['simple', 'test']
        for word in expected_words:
            self.assertIn(word, result)
        self.assertNotIn('this', result)

    def test_empty_text(self):
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_text("   "), "")
        self.assertEqual(clean_text(None), "")

    def test_text_with_url(self):
        text = "Check this website https://example.com for info."
        result = clean_text(text)
        self.assertNotIn("https", result)
        self.assertIn("check", result)

    def test_text_with_html(self):
        text = "<p>This is a paragraph.</p>"
        result = clean_text(text)
        self.assertNotIn("<p>", result)
        self.assertIn("paragraph", result)

    def test_text_with_punctuation(self):
        text = "Hello!!! How's everything?"
        result = clean_text(text)
        self.assertNotIn("!", result)
        self.assertNotIn("'", result)
        self.assertIn("hello", result)
        self.assertIn("everything", result)

    def test_stopwords_removal(self):
        text = "This and that are stopwords."
        result = clean_text(text)
        self.assertNotIn("and", result)
        self.assertNotIn("are", result)
        self.assertNotIn("this", result)
        self.assertIn("stopword", result)

if __name__ == '__main__':
    unittest.main()
