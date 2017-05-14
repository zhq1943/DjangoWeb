from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import unittest
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()
    def check_for_row_in_list_table(self, row_text):
        table=self.browser.find_element_by_id('id_list_table')
        rows=table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
    def test_can_start_a_list_and_retrieve_it_later(self):


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
        time.sleep(3)

        #table=self.browser.find_element_by_id('id_list_table')

        #rows=table.find_elements_by_tag_name('tr')
        #self.assertTrue(any(row.text=='1:Buy peacock feathers' for row in rows),
        #f"New to-do item did not appear in table. Contents were:\n{table.text}")
        #There is still a text box inviting her to add another item. She
        #enters "Use peacock faethers to make a fly" (Edith is very methodical)

        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)
        #The page updates anain, and now both items on her list

        self.check_for_row_in_list_table('1:Buy peacock feathers')
        self.check_for_row_in_list_table('2:Use peacock feathers to make a fly')
        #Edith wonders whether the site will remember her list. Then she sees
        #that the site has genrated a unique URL for her --there is some 
        #explanatory text to the effect

        #She visite that URL - her to-do list is still there

        #Satisfied , she goes back to sleep
        self.fail('Finish the test!')
