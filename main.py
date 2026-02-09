import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait



# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


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
    add_card_button = (By.ID, 'link')
    card_number_field = (By.ID, 'number')
    card_code_field = (By.ID, 'code')

    message_field = (By.ID, 'comment')

    blanket_and_napkins_checkbox = (By.ID, 'blanket_and_napkins')

    ice_cream_plus = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]")

    order_taxi_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')

    searching_modal = (By.CLASS_NAME, 'searching')
    driver_info_modal = (By.CLASS_NAME, 'driver-info')

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
        code = retrieve_phone_code(self.driver)
        self.driver.find_element(*self.phone_code_field).send_keys(code)
        self.driver.find_element(*self.phone_confirm).click()


    def add_credit_card(self, card_number, card_code):
        self.wait.until(expected_conditions.element_to_be_clickable(self.open_card)).click()
        self.driver.find_element(*self.add_card_button).click()
        self.driver.find_element(*self.card_number_field).send_keys(card_number)
        cvv = self.driver.find_element(*self.card_code_field)
        cvv.send_keys(card_code)
        cvv.send_keys(Keys.TAB)

    def write_message(self, message_for_driver):
        self.driver.find_element(*self.message_field).send_keys(message_for_driver)

    def request_blanket_and_napkins(self):
        self.driver.find_element(*self.blanket_and_napkins_checkbox).click()


    def order_ice_cream(self, quantity=2):
        for _ in range(quantity):
            self.driver.find_element(*self.ice_cream_plus).click()

    def order_taxi(self):
        self.wait.until(expected_conditions.element_to_be_clickable(self.order_taxi_button)).click()
    def wait_searching_modal(self):
        self.wait.until(expected_conditions.visibility_of_element_located(self.searching_modal))

    def wait_driver_info(self):
        self.wait.until(expected_conditions.visibility_of_element_located(self.driver_info_modal))





class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import EdgeOptions
        options = EdgeOptions()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Edge(options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        routes_page.order_taxi()
        routes_page.select_comfort()
        routes_page.fill_phone_number(data.phone_number)
        routes_page.fill_phone_code()
        routes_page.add_credit_card(data.card_number, data.card_code)
        routes_page.write_message(data.message_for_driver)
        routes_page.request_blanket_and_napkins()
        routes_page.order_ice_cream(2)
        routes_page.order_taxi()
        routes_page.wait_searching_modal()
        routes_page.wait_driver_info()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
