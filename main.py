from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import data
import helpers
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes.")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

    def setup_method(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)
        self.page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)


    def open_comfort_flow(self):
        self.page.open_options_after_addresses()


        self.page.choose_comfort_plan()


    def open_comfort_flow_with_phone(self):
        self.open_comfort_flow()

        self.page.fill_phone_number(data.PHONE_NUMBER)


    def open_comfort_flow_with_phone_and_card(self):
        self.open_comfort_flow_with_phone()

        self.page.add_payment_card(data.CARD_NUMBER, data.CARD_CODE)

    def test_set_route(self):


        assert self.page.get_from_location() == data.ADDRESS_FROM
        assert self.page.get_to_location() == data.ADDRESS_TO

    def test_select_plan(self):
        self.open_comfort_flow()


        assert self.page.get_selected_tariff() == "Comfort"

    def test_fill_phone_number(self):
        self.open_comfort_flow()

        self.page.fill_phone_number(data.PHONE_NUMBER)


        assert self.page.get_confirmed_phone_number() == data.PHONE_NUMBER

    def test_fill_card(self):
        self.open_comfort_flow_with_phone()


        self.page.add_payment_card(data.CARD_NUMBER, data.CARD_CODE)


        assert "Cartão" in self.page.get_payment_method() or "Card" in self.page.get_payment_method()

    def test_comment_for_driver(self):
        self.open_comfort_flow()

        self.page.write_driver_comment(data.MESSAGE_FOR_DRIVER)


        assert self.page.get_driver_comment() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        self.open_comfort_flow()

        self.page.select_blanket_and_handkerchiefs()


        assert self.page.is_blanket_and_handkerchiefs_selected()

    def test_order_2_ice_creams(self):
        self.open_comfort_flow()

        self.page.add_ice_creams(2)


        assert self.page.get_ice_cream_count() == 2

    def test_car_search_model_appears(self):
        self.open_comfort_flow()

        self.page.fill_phone_number(data.PHONE_NUMBER)


        self.page.add_payment_card(data.CARD_NUMBER, data.CARD_CODE)


        self.page.write_driver_comment(data.MESSAGE_FOR_DRIVER)


        self.page.request_taxi()


        assert self.page.is_searching_car_modal_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()