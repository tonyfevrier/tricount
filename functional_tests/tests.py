from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        
    
    def test_Welcome_Page(self):
        
        #Le visiteur arrive sur la page il voit le titre. 
        url = self.live_server_url 
        self.browser.get(url + '/count') 
        self.assertIn('Tricount',self.browser.title)
        
        #Il clique sur le lien du nouveau tricount
        link = self.browser.find_element(By.ID,'id_newcount') 
        link.send_keys(Keys.ENTER)
        time.sleep(2)  

        self.assertEqual(self.browser.current_url, url + '/count/newcount') 

        
        #Il voit la liste des tricount présents.
        table = self.browser.find_element(By.ID, 'list_counts')
        rows = table.find_elements(By.TAG_NAME,'td')
        self.assertIn('Tony',[row for row in rows]) 
        

        