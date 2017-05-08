from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()
    def test_can_start_a_list_and_retrieve_it_later(self):


        #Edith has heard about a cool new online to-do app. she goes 
        #to check out its homepage

        self.browser.get('http://localhost:8000')


        #she notices the page title and header mention to-do lists
        self.assertIn( 'To-Do', self.browser.title)
        self.fail('Finish the test!')

        #she is invited to enter a to-do tiem straight away

        #she type "Buy peacock feathers" into a text box (Edith's hobby
        #is tying fly-fishing lures)

        #When she hits enter, the page updates , and now the page lists
        #"1:Buy peacock feathers" as an ite in a to-do list

        #There is still a text box inviting her to add another item. She
        #enters "Use peacock faethers to make a fly" (Edith is very methodical)

        #The page updates anain, and now both items on her list

        #Edith wonders whether the site will remember her list. Then she sees
        #that the site has genrated a unique URL for her --there is some 
        #explanatory text to the effect

        #She visite that URL - her to-do list is still there

        #Satisfied , she goes back to sleep
if __name__=='__main__':
    unittest.main(warnings='ignore')
