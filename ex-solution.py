__author__ = 'adri7917'
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8888/')

search_element = browser.find_element_by_css_selector('input[type="submit"]')
search_element.click()
