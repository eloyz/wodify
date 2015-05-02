import logging
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import settings


logger = logging.getLogger(__name__)


class WeightDownload(object):
    """Downloads weight information from wodify.com"""

    def __init__(self, driver):
        """Initialize

        :param driver: the initialized selenium driver
        :param dict params: the params sent from the command line
        """
        self.driver = driver
        self.log = logger

    def log_in(self):
        """Log in user
        """
        self.driver.get("http://login.wodify.com/")

        username_field = self.driver.find_element_by_id('wt35_wtMainContent_wtUserNameInput')
        password_field = self.driver.find_element_by_id('wt35_wtMainContent_wtPasswordInput')
        remember_field = self.driver.find_element_by_id('wt35_wtMainContent_wt16')
        login_button = self.driver.find_element_by_id('wt35_wtMainContent_wt21')

        username_field.send_keys(settings.EMAIL)
        password_field.send_keys(settings.PASSWORD)
        login_button.send_keys(Keys.RETURN)


    def run(self):
        """Run the script
        """
        self.log_in()

        # Performance link
        performance_link = self.driver.find_element_by_id('WodifyUI_wt33_block_wtMenu_wodify_wt53_block_wt21')
        performance_link.click()

        # Weightlifting link
        weightlifting_link = self.driver.find_element_by_id('WodifyUI_wt18_block_wtSubNavigation_wt5_wt12')
        weightlifting_link.click()

        # Go to athlete performance > weightlifting
        # self.driver.get('https://app.wodify.com/PerformanceTracking/AthletePerformance_Weightlifting.aspx')
        dropdown = self.driver.find_element_by_id('WodifyUI_wt16_block_wtMainContent_wtAthleteDropDown_chosen')
        dropdown.click()

        athlete_ul = self.driver.find_element_by_class_name('chosen-results')
        athlete_li = athlete_ul.find_elements_by_tag_name('li')

        # Remove initial "select" option from list
        athlete_length = len(athlete_li)
        dropdown.click()

        main_content = self.driver.find_element_by_id('WodifyUI_wt16_block_wtMainContent_wtUserIf')

        for idx in range(1, athlete_length):

            dropdown = self.driver.find_element_by_id('WodifyUI_wt16_block_wtMainContent_wtAthleteDropDown_chosen')
            dropdown.click()

            athlete_ul = self.driver.find_element_by_class_name('chosen-results')
            athlete_list = athlete_ul.find_elements_by_tag_name('li')
            athlete_list[idx].click()

            time.sleep(5) # delays for 5 seconds

            # wait = WebDriverWait(self.driver, 10)
            # element = wait.until(EC.staleness_of(main_content))

            export_link = self.driver.find_element_by_id('WodifyUI_wt16_block_wtMainContent_wtPCard_wtExport2')
            export_link.click()

