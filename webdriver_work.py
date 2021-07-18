from selenium import webdriver
import os, traceback, selenium
import shutil, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


class GosUslugi:

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.gos_url = "https://www.gosuslugi.ru/"

    def check_elemnt_on_page(self, driver, xpath_elem):
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath_elem)))
        except selenium.common.exceptions.TimeoutException:
            print('ERROR :\n', traceback.format_exc())
            return False
        else:
            return True

    def create_driver(self):
        path_curr_dir = os.path.dirname(os.path.abspath(__file__))
        options = Options()
        options.headless = True
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.dir", self.curr_dir)
        fp.set_preference("browser.preferences.instantApply", True)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        fp.set_preference("browser.helperApps.alwaysAsk.force", False)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("pdfjs.disabled", True)
        fp.set_preference("dom.disable_beforeunload", True)
        driver = webdriver.Firefox(options=options,
                                   firefox_profile=fp,
                                   executable_path=f'{path_curr_dir}/geckodriver_linux')
        return driver

    def sigh_in(self, driver, login_sigh_in, password_sigh_in):
        driver.get(self.gos_url)
        driver.find_element_by_xpath('//*[@class="lk-enter"]').click()
        xpath_login = '//*[@id="login"]'

        check = self.check_elemnt_on_page(driver, xpath_login)
        if check:
            driver.find_element_by_xpath('//*[@id="login"]').send_keys(login_sigh_in)
            driver.find_element_by_xpath('//*[@id="password"]').send_keys(password_sigh_in)
            driver.find_element_by_xpath('//*[@id="loginByPwdButton"]').click()

            xpath_to_data = '/html/body/lk-root/main/div/lib-tabs/nav/div/ul/li[3]/a/span'  # xpath Documents and Data
            check = self.check_elemnt_on_page(driver,xpath_to_data)
            if check:
                driver.get('https://lk.gosuslugi.ru/profile/personal')
                return True
            else:
                return False
        else:
            return False

    def save_data(self, driver):

        xpath_passport_number = '/html/body/lk-root/main/lk-profile/div/div/div[2]/lk-personal/div[2]/' \
                                'lk-rf-passport-card/lk-doc-card/section/a/div[2]/lk-doc-card-row[1]/h5'
        xpath_release = '/html/body/lk-root/main/lk-profile/div/div/div[2]/lk-personal/div[2]/' \
                        'lk-rf-passport-card/lk-doc-card/section/a/div[2]/lk-doc-card-row[2]/div/div[2]'
        xpath_code_number = '/html/body/lk-root/main/lk-profile/div/div/div[2]/lk-personal/div[2]/lk-rf-passport-card/' \
                            'lk-doc-card/section/a/div[2]/lk-doc-card-row[3]/div/div[2]'
        xpath_date = '/html/body/lk-root/main/lk-profile/div/div/div[2]/lk-personal/div[2]/lk-rf-passport-card/' \
                     'lk-doc-card/section/a/div[2]/lk-doc-card-row[4]/div/div[2]'
        # create dir for save file with data
        dir_name = 'myData'
        try:
            shutil.rmtree(f'{self.curr_dir}/{dir_name}')
        except Exception:
            os.mkdir(f'{self.curr_dir}/{dir_name}')
        else:
            os.mkdir(f'{self.curr_dir}/{dir_name}')

        check = self.check_elemnt_on_page(driver, xpath_passport_number)
        if check:
            data_for_file = {}
            data_for_file['passport number'] = driver.find_element_by_xpath(xpath_passport_number).text
            data_for_file['who release'] = driver.find_element_by_xpath(xpath_release).text
            data_for_file['code number'] = driver.find_element_by_xpath(xpath_code_number).text
            data_for_file['date release'] = driver.find_element_by_xpath(xpath_date).text
            with open(f'{self.curr_dir}/{dir_name}/data.txt', 'a+') as f:
                for k, v in data_for_file.items():
                    f.write(f"{k} - {v}\n")
        else:
            pass

    def order_in_work_or_not(self, driver):
        xpath_text = '/html/body/lk-root/main/lk-overview/div/div/div/div[2]/div/lib-feeds/a[1]/div/div[1]/div/div/div/h4'
        check_text = 'справки о размере пенсии и иных социальных выплат'
        driver.get('https://lk.gosuslugi.ru/overview')
        check = self.check_elemnt_on_page(driver, xpath_text)
        if check:
            order_text = driver.find_element_by_xpath(xpath_text).text
            if check_text in order_text:
                return True
            else:
                return False
        else:
            return False

    def get_reference(self, driver):
        xpath_get_button = '/html/body/portal-root/main/portal-select-player/portal-new-sf-player/' \
                           'epgu-constructor-form-player/epgu-cf-ui-main-container/epgu-constructor-screen-resolver/' \
                           'epgu-constructor-info-screen/epgu-cf-ui-screen-container/div/' \
                           'epgu-cf-ui-constructor-screen-pad/epgu-constructor-screen-buttons/lib-button/div'
        xpath_last_order = '/html/body/lk-root/main/lk-overview/div/div/div/div[2]/div/lib-feeds/a[1]'
        xpath_download = '/html/body/lk-root/main/lk-order-details/div/div/div[1]/div[1]/div[2]/div/lk-files/' \
                         'div/div/div[2]/div[2]/div/div/a'

        check_order = self.order_in_work_or_not(driver)
        if check_order:
            # DOWNLOAD
            driver.get('https://lk.gosuslugi.ru/overview')
            check = self.check_elemnt_on_page(driver, xpath_last_order)
            if check:
                driver.implicitly_wait(10)
                driver.find_element_by_xpath(xpath_last_order).click()
                driver.find_element_by_xpath(xpath_download).click()
        else:
            # ORDER
            driver.get('https://www.gosuslugi.ru/600113/1/form')
            check = self.check_elemnt_on_page(driver, xpath_get_button)
            if check:
                driver.find_element_by_xpath(xpath_get_button).click()

    def run(self):
        driver = self.create_driver()
        try:
            sign_in = self.sigh_in(driver, self.login, self.password)
            if sign_in:
                self.save_data(driver)
                self.get_reference(driver)
        except Exception:
            print('ERROR :\n', traceback.format_exc())
        finally:
            time.sleep(7)
            driver.quit()
