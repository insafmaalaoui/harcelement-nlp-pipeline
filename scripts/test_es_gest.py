import unittest
from unittest.mock import patch, MagicMock
from es_gest import analyze_sentiment

class TestESGest(unittest.TestCase):

    def test_analyze_sentiment_positif(self):
        text = "J'adore ce produit, il est excellent !"
        sentiment, score = analyze_sentiment(text)
        self.assertEqual(sentiment, "positif")
        self.assertGreater(score, 0)

    def test_analyze_sentiment_negatif(self):
        text = "C'est une horreur, je déteste ça."
        sentiment, score = analyze_sentiment(text)
        self.assertEqual(sentiment, "negatif")
        self.assertLess(score, 0)

    def test_analyze_sentiment_neutre(self):
        text = "Ceci est un texte."
        sentiment, score = analyze_sentiment(text)
        self.assertEqual(sentiment, "neutre")

    @patch("es_gest.pymongo.MongoClient")
    def test_mongodb_connection(self, mock_client):
        mock_client.return_value.__getitem__.return_value = MagicMock()
        from es_gest import collection
        self.assertTrue(collection)

    @patch("es_gest.Elasticsearch")
    def test_elasticsearch_connection(self, mock_es):
        mock_instance = mock_es.return_value
        mock_instance.indices.exists.return_value = False
        mock_instance.indices.create.return_value = {"acknowledged": True}
        from es_gest import es
        self.assertTrue(es.indices)

if __name__ == "__main__":
    unittest.main()
