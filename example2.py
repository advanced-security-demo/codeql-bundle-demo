__author__ = 'adri7917'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()
browser.get('http://yahoo.com')

assert 'Yahoo' in browser.title

element = browser.find_element_by_name('p')

raw_input('PRESS ENTER PROCEED')
element.send_keys('seleniumhq' + Keys.RETURN)
raw_input('ENTER TO PROCEED')
browser.quit()
