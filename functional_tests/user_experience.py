import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Click():
    """
    Class of methods used in functional_tests to simulate the user experience.
    """
    def __init__(self,browser,live_server_url) -> None:
        self.browser = browser
        self.live_server_url = live_server_url

    def register_someone(self,username,email,password):
        """
        Function for registering a new user.
        
        Inputs : 
            - username (str)
            - email (str)
            - password (str)
        """
        user,mail,pwd = self.find_multiple_elements(By.NAME,"username","email","password")
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
 
        user,pwd = self.find_multiple_elements(By.NAME,"username","password")
        submit = self.browser.find_element(By.CLASS_NAME, "submit")

        user.send_keys(username) 
        pwd.send_keys(password)
        submit.send_keys(Keys.ENTER)
        time.sleep(2)

    def register_and_login_someone(self, username, email, password):
        """
        Function which register someone and log in him

        Inputs : 
            - username (str) 
            - email (str)
            - password (str)
        """
        url = self.live_server_url  
        self.browser.get(url)
        self.register_someone(username, email, password)   

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

        Inputs : 
           - literal : the html attribute to find the element.
           - name : the name of the attribute.
        """
        link = self.browser.find_element(literal,name)  
        link.send_keys(Keys.ENTER)
        time.sleep(2) 

    def click_on_successive_links(self, literal, *names):
        """
        Function which clicks on several links

        Inputs : 
            - literal (object): the html attribute to find the element.
            - names (list[str]) : the names of the attribute.
        """
        for name in names:
            self.click_on_a_link(literal, name)
    
    def find_multiple_elements(self, literal, *names):
        """
        Function which return multiple elements given by their names

        Inputs : 
            - literal (object): the attribute to get the element (example : By.NAME) 
            - names (list[str]): a sequences of names associated with the literal            
        
        Outputs : 
            - elemnts (tuple[object]) : the tuple containing the elements.
        """
        elements = []
        for name in names:
            elements.append(self.browser.find_element(literal, name))
        return tuple(elements)

    def add_participants(self,*participants):
        """
        Function which adds participants when we try to create a new tricount.

        Inputs : 
            - participants (list[str])
        """
        for participant in participants:
            participantbox = self.browser.find_element(By.NAME,"new_participant")
            buttonbox = self.browser.find_element(By.CLASS_NAME,"add_participant") 
            participantbox.send_keys(participant)
            buttonbox.send_keys(Keys.ENTER)
            time.sleep(2)

    def add_tricount_characteristics(self,title,password,description,currency,category):
        """
        Function which adds tricount characteristics when we try to create a new tricount.

        Inputs : 
            - title (str)
            - password (str)
            - description (str)
            - currency (str)
            - category (str)
        """
 
        self.click_on_successive_links(By.CLASS_NAME,"choose-currency",currency)
        titlebox,passwordbox,descriptionbox,submitbox = self.find_multiple_elements(By.NAME,
                                                                                    "newtricount_title",
                                                                                    "newtricount_pwd",
                                                                                    "newtricount_description",
                                                                                    "submit")
        categorybox = self.browser.find_element(By.ID,f"{category}")  

        titlebox.send_keys(title)
        descriptionbox.send_keys(description) 
        passwordbox.send_keys(password)  
  
        categorybox.click()

        #He chooses to go on the currency page: 
        submitbox.send_keys(Keys.ENTER)
        time.sleep(2)

    def create_a_tricount(self,title, password, description, currency, category,*participants):
        """
        Function which creates a new tricount.

        Inputs : 
            - title (str)
            - password (str)
            - description (str)
            - currency (str)
            - category (str)
            - participants (list[str])
        """

        #Clicks to add a tricount  
        self.click_on_successive_links(By.ID,'id_newcount','countfromzero')

        #Enter the participants 
        self.add_participants(*participants) 

        #Enter  the other characteristics and click to validate
        self.add_tricount_characteristics(title, password, description, currency, category)

    def clone_a_tricount(self,title,password):
        """
        Function used to clone an existing tricount.

        Input :
            - title (str) of the tricount
            - password (str) 
        """
        self.click_on_a_link(By.ID,'id_newcount')  
        self.click_on_a_link(By.CLASS_NAME,"clonecount")  
        tricount_title,pwd,submit = self.find_multiple_elements(By.CLASS_NAME,"tricount-title","password","pwdsubmit")
        tricount_title.send_keys(title)
        pwd.send_keys(password)
        submit.send_keys(Keys.ENTER)
        time.sleep(3)

    def click_on_an_existing_tricount(self,tricount_number):
        link = self.browser.find_element(By.ID,"link-tricount-" + str(tricount_number))
        link.send_keys(Keys.ENTER)
        time.sleep(2) 

    def modify_a_tricount(self,modified_elements = {}, participants_to_add = [], participants_to_delete = []):
        """
        Function aiming at modifying a tricount.

        Inputs : 
            - modified_elements (dict) : dictionnary whose keys are class names of input text elements (except receivers) we want to modify and whose values are the value to enter
                Example : {'title':'Nouveau titre, "description":'blabla'}
            - participants_to_add (list)
            - participants_to_delete (list)
        """ 

        #Modification of the input text elements
        for classname in modified_elements.keys():
            element = self.browser.find_element(By.CLASS_NAME, classname)
            self.clear_registration_inputs(element)
            element.send_keys(modified_elements[classname])
        
        #Modification of participants: 
        for participant in participants_to_add:
            self.add_participants(participant)

        for participant in participants_to_delete:
            self.click_on_a_link(By.CSS_SELECTOR, f"button[name = {participant}]") 

        self.click_on_a_link(By.CLASS_NAME,'submittricount')


    def click_on_create_spending(self):
        link_spending = self.browser.find_element(By.CLASS_NAME,'new-spending')
        link_spending.send_keys(Keys.ENTER)
        time.sleep(2)


    def create_a_spending(self,title,amount,payer,receivers,currency):
        """
        Function creating a new spending

        Inputs : 
            - title (str)
            - amount (float)
            - payer (str)
            - receivers (list[str])
        
        """ 
        self.click_on_successive_links(By.CLASS_NAME,'choose-currency',currency) 
        titlebox,amountbox,spenderbox,submitbox = self.find_multiple_elements(By.NAME,
                                                                                          'title',
                                                                                          'amount',
                                                                                          'spender',
                                                                                         'submit')  
        receiverbox = self.browser.find_elements(By.NAME,'receiver')
        titlebox.send_keys(title)
        amountbox.send_keys(amount)
        spenderbox.send_keys(payer)  

        for receiver in receiverbox:
            if receiver.get_attribute("value") not in receivers:
                receiver.click()

        submitbox.send_keys(Keys.ENTER)
        time.sleep(2)

    def click_and_create_a_spending(self,title,amount,payer,receivers,currency):
        self.click_on_a_link(By.CLASS_NAME,'new-spending')
        self.create_a_spending(title,amount,payer,receivers,currency)

    def modify_a_spending(self,modified_elements,*receivers):
        """
        Function modifying a spending

        Inputs : 
            - modified_elements (dict) : dictionnary whose keys are class names of input text elements (except receivers) we want to modify and whose values are the value to enter
                Example : {'title':'Nouveau titre,'amount':10, "spender":'Joe', "choose-currency":"EUR"}
            - receivers (list) : list of participants we want to receive the spending.
        """ 

        for classname in modified_elements.keys():
            element = self.browser.find_element(By.CLASS_NAME, classname)
            if element.tag_name == 'input':
                self.clear_registration_inputs(element)
            element.send_keys(modified_elements[classname])
        
        receiverbox = self.browser.find_elements(By.NAME, 'receiver') 

        #We check all participants if they are not all checked and we then unckeck all participants who are not in receivers
        if any([not receiver.is_selected() for receiver in receiverbox]):
            toggle_box = self.browser.find_element(By.CLASS_NAME,"toggle-checkboxes") 
            toggle_box.click()
        for receiver in receiverbox:
            if receiver.get_attribute("value") not in receivers:
                receiver.click()

        submitbox = self.browser.find_element(By.NAME,'submit')  
        submitbox.send_keys(Keys.ENTER)
        time.sleep(2)        


    def click_on_an_existing_spending(self,spending_number): 
        link = self.browser.find_element(By.ID,"spending-" + str(spending_number))
        link.send_keys(Keys.ENTER)
        time.sleep(2) 


class Check():
    """
    Class containing methods to check that some JS actions work
    """
    def __init__(self,browser) -> None:
        self.browser = browser 

    def check_if_popup_displayed(self,classname,bool):
        """
        Function which checks if a given popup appeared.

        Inputs : 
            classname : name of the class of the html elt
            bool : True or False to see if the popup is displayed or not.
        """
        popup = self.browser.find_element(By.CLASS_NAME, classname)
        self.assertEqual(popup.is_displayed(),bool) 

    def check_informations_of_a_spending(self,titre,prix,payeur,ptcpts,amnts):
        """
        Function which checks that a spending has been correctly registered.

        Inputs : 
            - titre (str)
            - prix (str)
            - payeur (str)
            - ptcpts (list[str])
            - amnts (list[float])
        """

        title = self.browser.find_element(By.CLASS_NAME,"title-spending")
        price = self.browser.find_element(By.CLASS_NAME,"price-spending")
        payer = self.browser.find_element(By.CLASS_NAME,"payer")
        participants = self.browser.find_elements(By.CLASS_NAME,"participant-name")
        amounts = self.browser.find_elements(By.CLASS_NAME,"participant-amount") 
 
        self.assertEqual(title.text.lower(), titre)
        self.assertEqual(price.text, prix)
        self.assertEqual(payer.text, payeur)

        for i in range(len(ptcpts)):
            self.assertIn(ptcpts[i], [participant.text for participant in participants])
            self.assertIn(amnts[i], [amount.text for amount in amounts])

             