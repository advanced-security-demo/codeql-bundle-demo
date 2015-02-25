import unittest
from selenium import webdriver


class GoogleTestCase(unittest.TestCase):
    """
    Example taken from selenium/python site:
    https://pypi.python.org/pypi/selenium
    """
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.addCleanup(self.browser.quit)

    def testPageTitle(self):
        self.browser.get('http://www.google.com')
        raw_input('Press ENTER to continue')
        self.assertIn('Google', self.browser.title)
        raw_input('Press ENTER to continue')

if __name__ == '__main__':
    unittest.main(verbosity=2)
