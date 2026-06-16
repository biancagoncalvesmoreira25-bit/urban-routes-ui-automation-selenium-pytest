from html.parser import commentclose

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from helpers import retrieve_phone_code


class UrbanRoutesPage:
 #Localizadores:

    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_taxi_button = (
    By.XPATH,
    '//button[contains(., "Chamar um táxi") or contains(., "Call a taxi")]'
     )

    comfort_plan_card = (By.XPATH, '//div[contains(@class, "tcard")]//div[contains(text(), "Comfort")]')
    selected_plan_title = (By.XPATH, '//div[@class="tcard active"]//div[@class="tcard-title"]')

    phone_number_button = (
        By.XPATH,
        '//div[contains(@class, "np-button") and (contains(., "Número de telefone") or contains(., "Phone number"))]'
    )
    phone_number_input = (By.ID, 'phone')
    phone_next_button = (By.CSS_SELECTOR, '.full')
    phone_code_input = (By.ID, 'code')
    phone_confirm_button = (By.XPATH, '//button[contains(text(), "Confirm")]')
    confirmed_phone_text = (By.CLASS_NAME, 'np-text')


    payment_method_buttons = (By.CLASS_NAME, 'pp-button')

    add_card_button = (
    By.XPATH,
    '//div[contains(@class, "pp-title") and (contains(., "Adicionar cartão") or contains(., "Add a card"))]'
    )

    card_number_input = (By.ID, 'number')
    card_code_input = (By.ID, 'code')
    card_modal_image = (By.CLASS_NAME, 'plc')

    card_add_button = (
    By.XPATH,
    '//button[contains(., "Adicionar") or contains(., "Add")]'
    )

    close_payment_modal_button = (
    By.XPATH,
    '//div[contains(@class, "payment-picker") and contains(@class, "open")]//button[contains(@class, "close-button")]'
    )

    selected_payment_method_text = (By.CLASS_NAME, 'pp-value-text')

    driver_comment_input = (By.ID, 'comment')

    option_switches = (By.CLASS_NAME, 'switch')
    option_switch_inputs = (By.CLASS_NAME, 'switch-input')

    plus_buttons = (By.CLASS_NAME, 'counter-plus')
    counter_values = (By.CLASS_NAME, 'counter-value')

    order_taxi_button = (By.CLASS_NAME, 'smart-button-wrapper')
    car_search_modal = (By.CLASS_NAME, 'order-body')

 #Métodos

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10)

    def _find(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def _wait_for(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def _wait_for_visible(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def _wait_for_clickable(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def _click_first_visible(self, locator, timeout=10):
        elements = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

        for element in elements:
            if element.is_displayed():
              self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
              self.driver.execute_script("arguments[0].click();", element)
              return

        raise Exception("Nenhum elemento visível encontrado para o localizador informado.")

    def _click(self, locator):
        self._wait_for_clickable(locator).click()

    def _type(self, locator, text):
        element = self._wait_for_visible(locator)
        element.clear()
        element.send_keys(text)

    def _get_text(self, locator):
        return self._wait_for_visible(locator).text

    def _get_value(self, locator):
        return self._wait_for(locator).get_property('value')


    def enter_addresses(self, from_address, to_address):
        self._type(self.from_field, from_address)
        self._type(self.to_field, to_address)
        self._wait_for(self.to_field).send_keys(Keys.TAB)


    def open_options_after_addresses(self):
        button = self._wait_for_clickable(self.call_taxi_button, timeout=10)
        self.driver.execute_script("arguments[0].scrollIntoView();", button)
        button.click()

    def open_taxi_options(self, from_address, to_address):
        self.enter_addresses(from_address, to_address)
        self.open_options_after_addresses()

    def get_from_address(self):
        return self._get_value(self.from_field)

    def get_to_address(self):
        return self._get_value(self.to_field)

    def enter_locations(self, from_address, to_address):
        self.enter_addresses(from_address, to_address)

    def get_from_location(self):
        return self.get_from_address()

    def get_to_location(self):
        return self.get_to_address()

    def set_route(self, from_address, to_address):
        self.open_taxi_options(from_address, to_address)

    def get_from(self):
        return self.get_from_address()

    def get_to(self):
        return self.get_to_address()

    def choose_comfort_plan(self):
        try:
            if self.get_selected_tariff() == 'Comfort':
                return
        except Exception:
            pass

        comfort_card = self._wait_for_visible(self.comfort_plan_card)
        self.driver.execute_script("arguments[0].scrollIntoView();", comfort_card)
        comfort_card.click()

    def get_selected_tariff(self):
        return self._wait_for_visible(self.selected_plan_title).text.strip()

    def select_supportive_plan(self):
        self.choose_comfort_plan()

    def get_current_selected_plan(self):
        return self.get_selected_tariff()


    def fill_phone_number(self, phone_number):
        phone_button = self._wait_for_clickable(self.phone_number_button, timeout=10)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", phone_button)
        phone_button.click()

        self._type(self.phone_number_input, phone_number)
        self._click(self.phone_next_button)

        code = retrieve_phone_code(self.driver)

        self._type(self.phone_code_input, code)
        self._click(self.phone_confirm_button)

    def get_confirmed_phone_number(self):
        return self._get_text(self.confirmed_phone_text).strip()

    def set_phone(self, number):
        self.fill_phone_number(number)

    def get_phone(self):
        return self.get_confirmed_phone_number()


    def add_payment_card(self, card_number, card_code):
        self._click_first_visible(self.payment_method_buttons, timeout=10)

        add_card = self._wait_for_visible(self.add_card_button, timeout=10)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_card)
        self.driver.execute_script("arguments[0].click();", add_card)

        card_input = self._wait_for_visible(self.card_number_input, timeout=10)
        card_input.send_keys(card_number + Keys.TAB + card_code)

        self._wait_for_visible(self.card_modal_image, timeout=10).click()

        add_button = self._wait_for_clickable(self.card_add_button, timeout=10)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
        self.driver.execute_script("arguments[0].click();", add_button)

        close_button = self._wait_for_clickable(self.close_payment_modal_button, timeout=10)
        close_button.click()

    def get_payment_method(self):
        return self._get_text(self.selected_payment_method_text).strip()

    def set_card(self, card_number, code):
        self.add_payment_card(card_number, code)

    def get_current_payment_method(self):
        return self.get_payment_method()

    def write_driver_comment(self, message):
        self._type(self.driver_comment_input, message)

    def get_driver_comment(self):
        return self._get_value(self.driver_comment_input)

    def set_message_for_driver(self, message):
        self.write_driver_comment(message)

    def get_message_for_driver(self):
        return self.get_driver_comment()

    def select_blanket_and_handkerchiefs(self):
        switches = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located(self.option_switches)
        )
        switches[0].click()

    def is_blanket_and_handkerchiefs_selected(self):
        switches = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located(self.option_switch_inputs)
        )
        return switches[0].get_property('checked')

    def click_blanket_and_handkerchiefs_option(self):
        self.select_blanket_and_handkerchiefs()

    def get_blanket_and_handkerchiefs_option_checked(self):
        return self.is_blanket_and_handkerchiefs_selected()

    def add_ice_creams(self, amount):
        plus_buttons = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located(self.plus_buttons)
        )

        self.driver.execute_script("arguments[0].scrollIntoView();", plus_buttons[0])

        for _ in range(amount):
            plus_buttons[0].click()

    def get_ice_cream_count(self):
        counters = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located(self.counter_values)
        )
        return int(counters[0].text)

    def add_ice_cream(self, amount):
        self.add_ice_creams(amount)

    def get_amount_of_ice_cream(self):
        return self.get_ice_cream_count()

    def request_taxi(self):
        self._click(self.order_taxi_button)

    def is_searching_car_modal_visible(self):
        return self._wait_for_visible(self.car_search_modal, timeout=10).is_displayed()

    def click_order_taxi_button(self):
        self.request_taxi()

    def wait_order_taxi_popup(self):
        self._wait_for_visible(self.car_search_modal, timeout=10)