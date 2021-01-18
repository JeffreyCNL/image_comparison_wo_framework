import unittest
from config import server_token
import requests

class ImageComparisonTestCase(unittest.TestCase):
    """ Unit tests for image comparison.
    """
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_identical_image_local_jpg(self):
        res = requests.get('http://localhost:5000/image-comparison?img_a=image/black.jpg&img_b=image/black.jpg&token=kmrhn74zgzcq4nqb')
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.text.find('True'), -1)
        self.assertNotEqual(res.text.find('100.0%'), -1)

    def test_image_local_png(self):
        res = requests.get('http://localhost:5000/image-comparison?img_a=image/half_black_white.png&img_b=image/black.jpg&token=kmrhn74zgzcq4nqb')
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.text.find('True'), -1)
        self.assertNotEqual(res.text.find('50.0%'), -1)

    def test_different_file_type(self):
        res = requests.get('http://localhost:5000/image-comparison?img_a=image/black.png&img_b=image/black.jpg&token=kmrhn74zgzcq4nqb')
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.text.find('True'), -1)
        self.assertNotEqual(res.text.find('100.0%'), -1)

    def test_url_input(self):
        res = requests.get('http://localhost:5000/image-comparison?img_a=https://i.imgur.com/gZKMme4.jpg&img_b=https://i.imgur.com/gWzHdpx.png&token=kmrhn74zgzcq4nqb')
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.text.find('True'), -1)
        self.assertNotEqual(res.text.find('50.0%'), -1)

    def test_url_local_input(self):
        res = requests.get('http://localhost:5000/image-comparison?img_a=image/black.png&img_b=https://i.imgur.com/gWzHdpx.png&token=kmrhn74zgzcq4nqb')
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.text.find('True'), -1)
        self.assertNotEqual(res.text.find('50.0%'), -1)

    def test_url_local_input_jpg_png(self):
        res = requests.get('http://localhost:5000/image-comparison?img_a=image/black.jpg&img_b=https://i.imgur.com/gWzHdpx.png&token=kmrhn74zgzcq4nqb')
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.text.find('True'), -1)
        self.assertNotEqual(res.text.find('50.0%'), -1)

    def test_invalid_token(self):
        res = requests.get('http://localhost:5000/image-comparison?img_a=https://i.imgur.com/gZKMme4.jpg&img_b=https://i.imgur.com/gWzHdpx.png&token=kmrhn74zgzcq4n')
        self.assertEqual(res.status_code, 403)
        # print(res.text)
        self.assertNotEqual(res.text.find('Invalid credentials'), -1)

    def test_no_token(self):
        res = requests.get('http://localhost:5000/image-comparison?img_a=https://i.imgur.com/gZKMme4.jpg&img_b=https://i.imgur.com/gWzHdpx.png')
        self.assertEqual(res.status_code, 401)
        # print(res.text)
        self.assertNotEqual(res.text.find('Authetication failed.'), -1)

    def test_invalid_path(self):
        res = requests.get('http://localhost:5000/image-comparison?img_a=pink.jpg&img_b=https://i.imgur.com/gWzHdpx.png&token=kmrhn74zgzcq4nqb')
        self.assertEqual(res.status_code, 404)
        self.assertNotEqual(res.text.find('resource not found'), -1)


if __name__ == "__main__":
    unittest.main()
