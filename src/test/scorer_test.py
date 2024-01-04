import unittest
import json
from src.variant_analyzer.scorer import app


class FlaskAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_scorer(self):
        new_entry = {
            "isoform": 'NX_P00533-1',
            "variants": [
                {
                    "start": 452,
                    "end": 452,
                    "original": 'N',
                    "variant": 'H'
                },
                {
                    "start": 21,
                    "end": 21,
                    "original": 'D',
                    "variant": 'H'
                },
                {
                    "start": 1,
                    "end": 1,
                    "original": 'M',
                    "variant": 'I'
                },
                {
                    "start": 510,
                    "end": 510,
                    "original": 'M',
                    "variant": 'I'
                }
            ]
        }

        response = self.app.post('/score', data=json.dumps(new_entry), content_type='application/json')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list, type(data))


if __name__ == '__main__':
    unittest.main()
