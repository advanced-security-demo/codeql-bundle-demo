import unittest
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException


# Helper function to get all the GET variables in a given URL
def extract_url_variables(url):
    matches = re.findall('[\?&]([^=]+)=([^\?&$ ]+)', url)
    return matches


class TestSequenceFunctions(unittest.TestCase):

    # Set up our class for each test case
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.base_url = 'http://localhost:8888/'
        self.vulnerable_urls = []

    # Tear down our class after each test case, print vulnerabilities if any
    def tearDown(self):
        try:
            self.driver.close()
            # self.driver.quit()
        except UnexpectedAlertPresentException as e:
            if int(e.alert_text) is 1:
                self.vulnerable_urls.append(self.driver.current_url)
            self.driver.quit()
        if len(self.vulnerable_urls) > 0:
            print "\nFound vulnerabilities!\n"
            for vuln in self.vulnerable_urls:
                print vuln
        else:
            print "\nNo vulnerabilities found\n"
        print "=" * 70, "\n"

    # Find our login fields, login as demo//demo
    def login(self):
        self.driver.get(self.base_url + 'login.php')

        user_field = self.driver.find_element_by_name('user')
        pass_field = self.driver.find_element_by_name('pass')
        submit_field = self.driver.find_element_by_name('signin')

        user_field.send_keys("demo")
        pass_field.send_keys("demo")
        submit_field.send_keys(Keys.RETURN)

    # Test for SQL injection on the billing.php page
    def test_sqli1(self):
        self.login()

        us_billing_link = self.driver.find_element_by_name('us_billing')
        us_billing_link.click()

        variables = extract_url_variables(self.driver.current_url)

        print "-" * 70, "\nStarting SQLi attack #1...\n", "-" * 70

        for variable in variables:
            attack_url = self.base_url + 'billing.php?{0}={1}'
            test_payload = "'"

            self.driver.get(attack_url.format(variable[0], test_payload))

            # Look for a common SQL server error message to determine success
            if "SQL syntax" in self.driver.page_source:
                self.vulnerable_urls.append(self.driver.current_url)

    # Test for Cross-site scripting on the billing.php page
    def test_xss1(self):
        self.login()

        us_billing_link = self.driver.find_element_by_name('us_billing')
        us_billing_link.click()

        variables = extract_url_variables(self.driver.current_url)

        print "-" * 70, "\nStarting XSS attack #1...\n", "-" * 70

        for variable in variables:
            attack_url = self.base_url + 'billing.php?{0}={1}'
            test_payload = "'\"><img src=x onerror=alert(1)>"

            try:
                self.driver.get(attack_url.format(variable[0], test_payload))

            # Deal with the Selenium exception raised when an alert box pops up
            # If we got an alert box with the text "1", we sere successful
            except UnexpectedAlertPresentException as e:
                if int(e.alert_text) is 1:
                    self.vulnerable_urls.append(self.driver.current_url)

    # Test for SQL injection on the billing.php page
    def test_sqli2(self):
        self.login()

        self.driver.get(self.base_url + 'detail.php')

        variables = [('id', 1)]

        print "-" * 70, "\nStarting SQLi attack #2...\n", "-" * 70

        for variable in variables:
            attack_url = self.base_url + 'detail.php?{0}={1}'
            test_payload = "'"

            self.driver.get(attack_url.format(variable[0], test_payload))

            # Look for a common SQL server error message to determine success
            if "SQL syntax" in self.driver.page_source:
                self.vulnerable_urls.append(self.driver.current_url)

    # Test for Cross-site scripting on the billing.php page
    def test_xss2(self):
        self.login()

        account_field = self.driver.find_element_by_name('account')
        account_field.send_keys('1' + Keys.RETURN)

        variables = extract_url_variables(self.driver.current_url)

        print "-" * 70, "\nStarting XSS attack #2...\n", "-" * 70

        for variable in variables:
            attack_url = self.base_url + 'account.php?{0}={1}'
            test_payload = "'\"><img src=x onerror=alert(1)>"

            try:
                self.driver.get(attack_url.format(variable[0], test_payload))

            # Deal with the Selenium exception raised when an alert box pops up
            # If we got an alert box with the text "1", we sere successful
            except UnexpectedAlertPresentException as e:
                if int(e.alert_text) is 1:
                    self.vulnerable_urls.append(self.driver.current_url)


if __name__ == '__main__':
    unittest.main(verbosity=0)
