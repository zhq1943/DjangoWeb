from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import unittest
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os

MAX_WAIT = 10
class NewVisitorTest(StaticLiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server=os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url='http://'+staging_server
    def tearDown(self):
        self.browser.quit()
    def wait_for_row_in_list_table(self, row_text):
        start_time=time.time()
        while True:
            try:
                table=self.browser.find_element_by_id('id_list_table')
                rows=table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    def test_can_start_a_list_for_one_user(self):


        #Edith has heard about a cool new online to-do app. she goes 
        #to check out its homepage

        self.browser.get(self.live_server_url)


        #she notices the page title and header mention to-do lists
        self.assertIn( 'To-Do', self.browser.title)
        header_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)
        #she is invited to enter a to-do tiem straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a to-do item')
        #she type "Buy peacock feathers" into a text box (Edith's hobby
        #is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        #When she hits enter, the page updates , and now the page lists
        #"1:Buy peacock feathers" as an ite in a to-do list
        inputbox.send_keys(Keys.ENTER)
        #time.sleep(3)
        self.wait_for_row_in_list_table('1:Buy peacock feathers')
        #table=self.browser.find_element_by_id('id_list_table')

        #rows=table.find_elements_by_tag_name('tr')
        #self.assertTrue(any(row.text=='1:Buy peacock feathers' for row in rows),
        #f"New to-do item did not appear in table. Contents were:\n{table.text}")
        #There is still a text box inviting her to add another item. She
        #enters "Use peacock faethers to make a fly" (Edith is very methodical)

        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        #time.sleep(3)
        #The page updates anain, and now both items on her list

        self.wait_for_row_in_list_table('1:Buy peacock feathers')
        self.wait_for_row_in_list_table('2:Use peacock feathers to make a fly')
        #Edith wonders whether the site will remember her list. Then she sees
        #that the site has genrated a unique URL for her --there is some 
        #explanatory text to the effect

        #She visite that URL - her to-do list is still there

        #Satisfied , she goes back to sleep
        self.fail('Finish the test!')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy peacock feathers')

        edith_list_url=self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        #Now a new user,Francis come along to the site
        ##we use a new browser session to make sure that no information
        ##of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser=webdriver.Firefox()

        #Francis visits the home page there is no sign of Edith's
        #list
        self.browser.get(self.live_server_url)
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly',page_text)

        #Francis starts a new list by entering a new item. He is
        #less interesting that Edith
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy milk')
        
        #Francis gets his own unique URL
        francis_list_url=self.browser.current_url
        self.assertRegex(francis_list_url,edith_list_url)

        #Again, there is no trace of Edith's list
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk',page_text)
    def test_layout_and_styling(self):
        #Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        #she notice the input box is nicely centered
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location["x"] + inputbox.size['width']/2,512,delta=10)

        #she starts a new list and sees the input is nicely
        #centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:testing')
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10)
