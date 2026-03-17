import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time
import helpers as helpers





class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    comfort_tariff = (By.XPATH, "//div[contains(text(),'Comfort')]")

    add_phone_number = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[1]")
    phone_field = (By.ID, 'phone')
    phone_code_field = (By.ID, 'code')
    click_submit_button = (By.XPATH, "//*[@id='root']/div/div[1]/div[2]/div[1]/form/div[2]/button")
    phone_confirm = (By.XPATH, "//*[@id='root']/div/div[1]/div[2]/div[2]/form/div[2]/button[1]")
    open_card = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[2]")
    add_card_button = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]")
    card_number_field = (By.ID, 'number')
    card_code_field = (By.XPATH,"/html/body/div/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/div[2]/div[2]/input")
    close_card_field= (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[1]/button")
    submit_card_button = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[2]/form/div[3]/button[1]")
    message_field = (By.ID, 'comment')

    blanket_and_napkins_checkbox = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span")

    ice_cream_plus = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]")

    order_taxi_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')

    submit_order = (By.XPATH,"//*[@id='root']/div/div[3]/div[4]/button/span[1]")

    searching_modal = (By.CLASS_NAME, 'order-body')
    driver_info_modal = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]/div[2]/div[1]/div[3]/button/img')
    display_drive_info = (By.XPATH, "/html/body/div/div/div[5]/div[2]/div[2]/div[1]/div[3]/button")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver,20)

    def set_from(self, from_address):
        self.wait.until(expected_conditions.visibility_of_element_located(self.from_field)).send_keys(from_address)
        self.driver.find_element(*self.from_field).send_keys(Keys.TAB)

    def set_to(self, to_address):
        self.wait.until(expected_conditions.visibility_of_element_located(self.to_field)).send_keys(to_address)
        self.driver.find_element(*self.to_field).send_keys(Keys.TAB)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def select_comfort(self):
        self.wait.until(expected_conditions.element_to_be_clickable(self.comfort_tariff)).click()


    def fill_phone_number(self, phone_number):
        self.wait.until(expected_conditions.visibility_of_element_located(self.add_phone_number)).click()
        self.driver.find_element(*self.phone_field).send_keys(phone_number)
        self.driver.find_element(*self.click_submit_button).click()

    def fill_phone_code(self):
        code = helpers.retrieve_phone_code(self.driver)
        self.driver.find_element(*self.phone_code_field).send_keys(code)
        self.driver.find_element(*self.phone_confirm).click()


    def add_credit_card(self, card_number):
        self.wait.until(expected_conditions.element_to_be_clickable(self.open_card)).click()
        self.driver.find_element(*self.add_card_button).click()
        self.driver.find_element(*self.card_number_field).send_keys(card_number)

    def add_credit_card_code(self, card_code):
       cvv=self.wait.until(expected_conditions.visibility_of_element_located(self.card_code_field))
       cvv.send_keys(card_code)
       cvv.send_keys(Keys.TAB)
       self.wait.until(expected_conditions.element_to_be_clickable(self.submit_card_button)).click()
       time.sleep(2)
       self.driver.find_element(*self.close_card_field).click()


    def write_message(self, message_for_driver):
        self.wait.until(expected_conditions.visibility_of_element_located(self.message_field)).send_keys(message_for_driver)

    def request_blanket_and_napkins(self):
        self.driver.find_element(*self.blanket_and_napkins_checkbox).click()


    def order_ice_cream(self, quantity=2):
        for _ in range(quantity):
            self.driver.find_element(*self.ice_cream_plus).click()

    def order_taxi(self):
        self.wait.until(expected_conditions.element_to_be_clickable(self.order_taxi_button)).click()

    def submit(self):
        self.wait.until(expected_conditions.visibility_of_element_located(self.submit_order)).click()

    def wait_searching_modal(self):
        self.wait.until(expected_conditions.visibility_of_element_located(self.searching_modal))
        time.sleep(3)

    def wait_driver_info(self):
        self.wait.until(expected_conditions.visibility_of_element_located(self.driver_info_modal))
        self.driver.find_element(*self.display_drive_info).click()
        time.sleep(1)






class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import ChromeOptions
        options = ChromeOptions()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)


    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to
    def test_select_comfort(self):
        self.routes_page.order_taxi()
        self.routes_page.select_comfort()
        comfort_element=  self.driver.find_element(*self.routes_page.select_comfort())
        assert comfort_element.is_displayed()
    def test_fill_phone_number(self):
        self.routes_page.fill_phone_number(data.phone_number)
        self.routes_page.fill_phone_code()
    def test_fill_phone_code(self):
        self.routes_page.add_credit_card(data.card_number)
        self.routes_page.add_credit_card_code(data.card_code)
    def write_message(self, message_for_driver):
        self.routes_page.write_message(data.message_for_driver)
    def request_blanket_and_napkins(self):
        self.routes_page.request_blanket_and_napkins()
        checkbox=self.driver.find_element(*self.routes_page.blanket_and_napkins_checkbox)
        assert checkbox.is_selected()
    def order_ice_cream(self):
        self.routes_page.order_ice_cream(2)
        counter=self.driver.find_element(*self.routes_page.order_ice_cream_counter)
        assert counter.text==2
    def order_taxi(self):
        self.routes_page.submit()
        self.routes_page.wait_searching_modal()
        self.routes_page.wait_driver_info()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
