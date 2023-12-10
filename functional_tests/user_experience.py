import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
 
class Click():
    def __init__(self,browser,live_server_url) -> None:
        self.browser = browser
        self.live_server_url = live_server_url

    def register_someone(self,username,email,password):
        """
        Function for registering a new user.
        Inputs : 
            -username (str)
            -email (str)
            -password (str)
        """
        user = self.browser.find_element(By.NAME, "username")
        mail = self.browser.find_element(By.NAME, "email")
        pwd = self.browser.find_element(By.NAME, "password")
        submit = self.browser.find_element(By.CLASS_NAME, "submit")

        user.send_keys(username)
        mail.send_keys(email)
        pwd.send_keys(password) 
        submit.send_keys(Keys.ENTER)
        time.sleep(2)
    
    def clear_registration_inputs(self,*elements):
        for element in elements:
            element.clear()


    def login_someone(self,username,password):
        """
        Function for logging someone who is already registered
        Inputs : 
            -username (str) 
            -password (str)
        """
        self.click_on_a_link(By.CLASS_NAME, "login")

        user = self.browser.find_element(By.NAME, "username") 
        pwd = self.browser.find_element(By.NAME, "password")
        submit = self.browser.find_element(By.CLASS_NAME, "submit")

        user.send_keys(username) 
        pwd.send_keys(password)
        submit.send_keys(Keys.ENTER)
        time.sleep(2)

    def logout_someone_from_listecount_page(self):
        """
        Function which logout the user from the page listing the counts of the user
        """
        self.click_on_a_link(By.CLASS_NAME,"parameters")
        self.click_on_a_link(By.CLASS_NAME,"myparameters")

        logout = self.browser.find_element(By.CLASS_NAME, "logout")
        logout.send_keys(Keys.ENTER)
        time.sleep(2)
    
    def click_on_a_link(self,literal,name):
        """
        Function which clicks on a link given by its id.

        literal : the html attribute to find the element.
        name : the name of the attribute.
        """
        link = self.browser.find_element(literal,name) 
        link.send_keys(Keys.ENTER)
        time.sleep(2) 

    def add_participants(self,*participants):
        for participant in participants:
            participantbox = self.browser.find_element(By.NAME,"new_participant")
            buttonbox = self.browser.find_element(By.CLASS_NAME,"add_participant") 
            participantbox.send_keys(participant)
            buttonbox.send_keys(Keys.ENTER)
            time.sleep(2)

    def add_tricount_characteristics(self,title,description,category):
        titlebox = self.browser.find_element(By.NAME,"newtricount_title")
        descriptionbox = self.browser.find_element(By.NAME,"newtricount_description") 
        categorybox = self.browser.find_element(By.ID,f"{category}") 
        submitbox = self.browser.find_element(By.NAME,"submit")
        
        titlebox.send_keys(title)
        descriptionbox.send_keys(description) 
        categorybox.click()

        #He chooses to go on the currency page: 
        submitbox.send_keys(Keys.ENTER)
        time.sleep(2)

    def create_a_tricount(self,title, description, category,*participants):
        self.browser.get(self.live_server_url+ '/count')

        #Clicks to add a tricount 
        self.click_on_a_link(By.ID,'id_newcount') 

        #Enter the participants 
        self.add_participants(*participants) 

        #Enter  the other characteristics and click to validate
        self.add_tricount_characteristics(title,description,category)

    def click_on_an_existing_tricount(self,tricount_number):
        """
        Function which clicks on a tricount and check the title and the participants are the good ones.
        participants : the participants we want to verify the presence.
        """
        link = self.browser.find_element(By.ID,"link-tricount-" + str(tricount_number))
        link.send_keys(Keys.ENTER)
        time.sleep(2) 

    def click_on_create_spending(self):
        link_spending = self.browser.find_element(By.CLASS_NAME,'new-spending')
        link_spending.send_keys(Keys.ENTER)
        time.sleep(2)

    def create_a_spending(self,title,amount,payer,receivers):#,respective_amounts):
        """
        Function creating a new spending
        """
        titlebox = self.browser.find_element(By.NAME, 'title')
        amountbox = self.browser.find_element(By.NAME, 'amount')
        spenderbox = self.browser.find_element(By.NAME, 'spender')
        receiverbox = self.browser.find_element(By.NAME, 'receiver') 
        submitbox = self.browser.find_element(By.NAME,'submit') 

        titlebox.send_keys(title)
        amountbox.send_keys(amount)
        spenderbox.send_keys(payer)
        receiverbox.send_keys(receivers)

        """
        #association of the respective amounts to receivers
        for i in range(len(receivers)):
            participantbox = self.browser.find_element(By.NAME,receivers[i])
            participantbox.send_keys(respective_amounts[i])
        """

        submitbox.send_keys(Keys.ENTER)
        time.sleep(2)

    def click_on_an_existing_spending(self,spending_number):
        """
        Function which clicks on a tricount and check the title and the participants are the good ones.
        participants : the participants we want to verify the presence.
        """
        link = self.browser.find_element(By.ID,"spending-" + str(spending_number))
        link.send_keys(Keys.ENTER)
        time.sleep(2) 


class Check():
    def __init__(self,browser,live_server_url) -> None:
        self.browser = browser
        self.live_server_url = live_server_url

    def check_if_popup_displayed(self,classname,bool):
        """
        Inputs : 
            classname : name of the class of the html elt
            bool : True or False to see if the popup is displayed or not.
        """
        popup = self.browser.find_element(By.CLASS_NAME, classname)
        self.assertEqual(popup.is_displayed(),bool) 

    def check_informations_of_a_spending(self,titre,prix,payeur,ptcpts,amnts):
        title = self.browser.find_element(By.CLASS_NAME,"title-spending")
        price = self.browser.find_element(By.CLASS_NAME,"price-spending")
        payer = self.browser.find_element(By.CLASS_NAME,"payer")
        participants = self.browser.find_elements(By.CLASS_NAME,"participant-name")
        amounts = self.browser.find_elements(By.CLASS_NAME,"participant-amount")
        Date = self.browser.find_element(By.CLASS_NAME,"date")

        self.assertEqual(title.text, titre)
        self.assertEqual(price.text, prix)
        self.assertEqual(payer.text, payeur)

        for i in range(len(ptcpts)):
            self.assertIn(ptcpts[i],[participant.text for participant in participants])
            self.assertIn(amnts[i],[amount.text for amount in amounts])

             