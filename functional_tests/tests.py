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
        
    
    def test_listecount_Page(self):
        
        #Le visiteur arrive sur la page il voit le titre. 
        url = self.live_server_url 
        self.browser.get(url + '/count') 
        self.assertIn('Tricount',self.browser.title)
        
        #Il voit la liste des tricount présents ou absents et clique sur le lien pour créer un nouveau tricount
        link = self.browser.find_element(By.ID,'id_newcount') 
        link.send_keys(Keys.ENTER)
        time.sleep(2)  

        self.assertEqual(self.browser.current_url, url + '/count/newcount') 

        #Il remplit les données d'un nouveau tricount et les envoie
        titlebox = self.browser.find_element(By.NAME,"newtricount_title")
        descriptionbox = self.browser.find_element(By.NAME,"newtricount_description")
        categorybox = self.browser.find_element(By.NAME,"newtricount_category")
        submitbox = self.browser.find_element(By.NAME,"submit")
        titlebox.send_keys('tricount 1')
        descriptionbox.send_keys('description 1')
        categorybox.send_keys('Voyage')
        submitbox.send_keys(Keys.ENTER)
        time.sleep(3)
        
        self.assertEqual(self.browser.current_url, url + '/count/') 
        self.assertIn('Tricount',self.browser.title)

        #Il est alors renvoyé vers la page recensant la liste des tricount : son tricount est apparu.
        title = self.browser.find_elements(By.CLASS_NAME,'tricount_title')
        description = self.browser.find_elements(By.CLASS_NAME,'tricount_description')
        self.assertIn('tricount 1',[titre.text for titre in title]) 
        self.assertIn('description 1',[desc.text for desc in description])

        #Il reclique pour recréer un second tricount.
        link = self.browser.find_element(By.ID,'id_newcount') 
        link.send_keys(Keys.ENTER)
        time.sleep(2)  

        self.assertEqual(self.browser.current_url, url + '/count/newcount') 

        #Il remplit les données d'un nouveau tricount et les envoie
        titlebox = self.browser.find_element(By.NAME,"newtricount_title")
        descriptionbox = self.browser.find_element(By.NAME,"newtricount_description")
        categorybox = self.browser.find_element(By.NAME,"newtricount_category")
        submitbox = self.browser.find_element(By.NAME,"submit")
        titlebox.send_keys('tricount 2')
        descriptionbox.send_keys('description 2')
        categorybox.send_keys('Projet')
        submitbox.send_keys(Keys.ENTER)
        time.sleep(3)

        title = self.browser.find_elements(By.CLASS_NAME,'tricount_title')
        description = self.browser.find_elements(By.CLASS_NAME,'tricount_description')
        self.assertIn('tricount 2',[titre.text for titre in title]) 
        self.assertIn('description 2',[desc.text for desc in description])
        

        