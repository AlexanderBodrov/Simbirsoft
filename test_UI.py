import time
from data import login, password, folder, file
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pytest

link = "https://ya.ru/"


@pytest.fixture(scope="class")
def browser():
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(link)
    browser.implicitly_wait(5)
    yield browser
    browser.find_element(By.ID, "/disk").click()
    delete_folder = browser.find_element(By.XPATH, f'//div[@aria-label="{folder}"]')
    action = ActionChains(browser)
    action.context_click(delete_folder).perform()
    browser.find_element(By.CSS_SELECTOR, "body > div.Popup2.Popup2_visible.Popup2_target_anchor.Popup2_view_default.resources-actions-popup.js-prevent-deselect > div > div > div:nth-child(4)").click()
    browser.find_element(By.CLASS_NAME, "PSHeader-User.PSHeader-User_noUserName").click()
    browser.find_element(By.CLASS_NAME, "menu__item.menu__item_type_link.legouser__menu-item.legouser__menu-item_action_exit").click()
    browser.quit()


class Test1:
    def test_enter_login(self, browser):
        browser.find_element(By.CLASS_NAME, "home-link2.headline__personal-enter.home-link2_color_black").click()
        login_field = browser.find_element(By.ID, "passp-field-login")
        login_field.send_keys(login)
        browser.find_element(By.ID, "passp:sign-in").click()

    def test_enter_password(self, browser):
        password_field = browser.find_element(By.ID, "passp-field-passwd")
        password_field.send_keys(password)
        browser.find_element(By.ID, "passp:sign-in").click()
        # browser.find_element(By.CLASS_NAME, "Button2.Button2_size_l.Button2_view_pseudo.Button2_width_max").click()

    def test_enter_to_the_disc(self, browser):
        browser.find_element(By.CLASS_NAME, "home-link2.headline__personal-avatar.usermenu-link-redesign.i-bem.avatar.usermenu-link-redesign_js_inited").click()
        browser.find_element(By.CLASS_NAME, "usermenu-redesign__item-inner.usermenu-redesign__disk-inner").click()
        latest_window = browser.window_handles[1]
        browser.close()
        browser.switch_to.window(latest_window)
        # browser.find_element(By.CLASS_NAME, "Button2.Button2_size_m.Base-Onboarding-Close").click()

    def test_create_folder(self, browser):
        browser.find_element(By.CLASS_NAME, "Button2.Button2_view_raised.Button2_size_m.Button2_width_max").click()
        browser.find_element(By.CLASS_NAME, "file-icon.file-icon_size_m.file-icon_dir_plus.create-resource-button__icon").click()
        folder_name = browser.find_element(By.CSS_SELECTOR, "div.confirmation-dialog__content > div > form > span > input")
        time.sleep(2)
        folder_name.send_keys(Keys.BACKSPACE)
        folder_name.send_keys(folder)
        browser.find_element(By.CSS_SELECTOR, "div.confirmation-dialog__footer > button").click()

    def test_open_folder(self, browser):
        open_folder = browser.find_element(By.XPATH, f'//div[@aria-label="{folder}"]')
        action = ActionChains(browser)
        time.sleep(5)
        action.double_click(open_folder).perform()

    def test_create_text_file(self, browser):
        browser.find_element(By.CLASS_NAME, "Button2.Button2_view_raised.Button2_size_m.Button2_width_max").click()
        browser.find_element(By.CLASS_NAME, "file-icon.file-icon_size_m.file-icon_doc.create-resource-button__icon").click()
        file_name = browser.find_element(By.CSS_SELECTOR, "div.confirmation-dialog__content > div > form > span > input")
        time.sleep(2)
        file_name.send_keys(Keys.BACKSPACE)
        file_name.send_keys(file)
        browser.find_element(By.CSS_SELECTOR, "div.confirmation-dialog__footer > button").click()

    def test_close_file_window(self, browser):
        before_window = browser.window_handles[0]
        latest_window = browser.window_handles[1]
        browser.switch_to.window(latest_window)
        browser.close()
        browser.switch_to.window(before_window)

    def test_check_new_file(self, browser):
        new_file = browser.find_elements(By.CLASS_NAME, "listing-item.listing-item_theme_tile.listing-item_size_m.listing-item_type_file.js-prevent-deselect")
        assert len(new_file) > 0

    def test_check_new_file_name(self, browser):
        name_new_file = browser.find_element(By.CLASS_NAME, "listing-item.listing-item_theme_tile.listing-item_size_m.listing-item_type_file.js-prevent-deselect")
        assert file in name_new_file.text
