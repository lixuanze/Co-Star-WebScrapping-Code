from time import sleep
import pandas as pd
import glob
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

pd.set_option('display.max_columns', None)

# User config:
city_to_scrape = ''

# Wrong Cities
# 1, 4


min_max_ranges = [
    [0, 499],
    [500, 999],
    [1000, 1599],
    [1600, 2749],
    [2750, 5199],
    [5200, 18499],
    [18500, 0],
]
start_city = 41
#Start scraping from this page number
start_city_page = 133
start_range = 2

# Create csv after scraping these many number of pages
save_page_interval = 3

skip_cities = [7, 65, 253]

scroll_right_enable = False
scroll_rights = [123, 126]
column_indexes = [16, 24]

# manual_adjust_columns = True

class Driver:
    """
    options: list of web driver options
    browser: Browser Type: Chrome, Firefox
    This creates a webdriver object with options.
    """

    def __init__(self, options=(), browser='chrome'):
        self.options = options
        self.browser = browser
        if self.browser == "firefox":
            web_driver_path = 'drivers\FirefoxDriver\geckodriver\geckodriver.exe'
            self.driver = webdriver.Firefox(executable_path=web_driver_path)
        elif self.browser == "chrome":
            web_driver_path = 'drivers\ChromeDriver\chromedriver_win32\chromedriver.exe'
            self.driver = webdriver.Chrome(executable_path=web_driver_path)

    def set_zoom_value(self, zoom_value):
        # Zoom In and Out
        self.driver.execute_script("document.body.style.zoom='" + str(zoom_value) + "%'")
        sleep(1)
        self.driver.set_window_size(1980, 1200)
        sleep(1)
        self.driver.maximize_window()
        sleep(10)

    def send_keys(self, tag_value, key_value):
        """Finds the element using xpath. If found, send_keys it."""
        elements = self.driver.find_elements_by_xpath(tag_value)
        if len(elements) > 0:
            elements[0].clear()
            elements[0].send_keys(key_value)

    def clear_keys(self, tag_value):
        """Finds the element using xpath. If found, send_keys it."""
        elements = self.driver.find_elements_by_xpath(tag_value)
        if len(elements) > 0:
            elements[0].clear()

    def click_button_xpath_with_script(self, tag_value):
        """Finds the element using xpath. If found, clicks it."""
        buttons = self.driver.find_elements_by_xpath(tag_value)
        if len(buttons) > 0:
            self.driver.execute_script("arguments[0].click();", buttons[0])

    def click_button_xpath(self, tag_value):
        """Finds the element using xpath. If found, clicks it."""
        buttons = self.driver.find_elements_by_xpath(tag_value)
        if len(buttons) > 0:
            buttons[0].click()

    def get_element_list(self, tag_value):
        """Get a list of elements from an xpath"""
        return self.driver.find_elements_by_xpath(tag_value)

    def execute_script(self, code, element):
        """Executes script"""
        return self.driver.execute_script(code, element)

    def current_url(self):
        """Gets current URL"""
        return self.driver.current_url

    def page_source(self):
        """Gets page source"""
        return self.driver.page_source

    def back(self):
        """Takes the driver 1 page back"""
        return self.driver.back()

    def close(self):
        """closes the driver"""
        return self.driver.close()

driver_options = ('--ignore-certificate-errors'
                    # '--kiosk',
                    # '--incognito',
                    # '--headless'
                  )
driver = Driver(driver_options, 'chrome')
#driver = Driver(driver_options, 'firefox')

username = ''
password = ''

# Costar Login
driver.driver.get('https://product.costar.com')
driver.driver.maximize_window()
sleep(3)
driver.send_keys("//input[@id='username']", username)
driver.send_keys("//input[@id='password']", password)
driver.click_button_xpath("//span[@class='login-footer-remember-me']")
driver.click_button_xpath("//button[@id='loginButton']")

sleep(30)

# USA Menu Click
driver.driver.find_element_by_css_selector("ul.navigation-container > li:nth-child(5)").click()
driver.driver.find_element_by_css_selector("ul.navigation-container > li:nth-child(5) .subMenuContainer").click()
driver.driver.find_element_by_css_selector("ul.navigation-container > li:nth-child(5) .subMenuContainer .country-container > li:first-child").click()
sleep(10)

driver.click_button_xpath("//span[text()='Market']")
sleep(5)

# Market Type Select
market_types = driver.driver.find_element_by_xpath("//select[@id='market-type']").find_elements_by_xpath(".//option")
market_types[0].click()
sleep(1)

if not os.path.exists(f'leasecomps_sf'):
    os.makedirs(f'leasecomps_sf')

if not os.path.exists(f'leasecomps_sf_medium'):
    os.makedirs(f'leasecomps_sf_medium')

# Column Names
column_names_fetch = False
column_names = []

# Cities Loop
cities_text = []
cities_elements = driver.driver.find_element_by_xpath("//select[@id='marketList']").find_elements_by_xpath(".//option")
for city_index in range(len(cities_elements)):
    if cities_elements[city_index].text:
        cities_text.append(cities_elements[city_index].text)

for city_index in range(len(cities_text)):
    if city_index >= start_city:
        if city_index in skip_cities:
            continue

        city_to_scrape = cities_text[city_index]
        city_to_scrape_file_name = cities_text[city_index].lower().replace(" ", "_").replace(".", "-").replace("-", "").replace("__", "_")

        if not os.path.exists(f'leasecomps_sf_medium/{city_to_scrape_file_name}'):
            os.makedirs(f'leasecomps_sf_medium/{city_to_scrape_file_name}')
            
        for min_max_range_index in range(len(min_max_ranges)):
            if city_index == start_city and min_max_range_index < start_range:
                continue
            min_sf = min_max_ranges[min_max_range_index][0]
            max_sf = min_max_ranges[min_max_range_index][1]
            if max_sf == 0:
                max_sf = 'max'

            if not os.path.exists(f'leasecomps_sf_medium/{city_to_scrape_file_name}/{min_sf}_{max_sf}'):
                os.makedirs(f'leasecomps_sf_medium/{city_to_scrape_file_name}/{min_sf}_{max_sf}')

            driver.send_keys("//input[@id='geographySearchFilter']", city_to_scrape)
            sleep(1)
            driver.click_button_xpath("//a[@id='addAllGeography']")
            sleep(1)
            driver.click_button_xpath("//a[@id='applyGeographySelection']")
            sleep(10)
            driver.click_button_xpath("//input[@id='AreaLeasedRangemin-clone']")
            sleep(1)
            driver.clear_keys("//input[@id='AreaLeasedRangemin']")
            sleep(2)
            driver.click_button_xpath("//input[@id='AreaLeasedRangemax-clone']")
            sleep(1)
            driver.clear_keys("//input[@id='AreaLeasedRangemax']")
            sleep(2)
            driver.click_button_xpath("//input[@id='AreaLeasedRangemin-clone']")
            sleep(1)
            driver.send_keys("//input[@id='AreaLeasedRangemin']", min_sf)
            sleep(2)
            driver.click_button_xpath("//input[@id='AreaLeasedRangemax-clone']")
            sleep(1)
            if str(max_sf) != 'max':
                driver.send_keys("//input[@id='AreaLeasedRangemax']", max_sf)
            sleep(1)
            driver.click_button_xpath("//a[@id='view-results-top']")
            sleep(15)

            if not column_names_fetch:
                driver.set_zoom_value(40)

                column_elements = driver.driver.find_element_by_xpath("//div[@id='contentleaseCompsGrid']").find_element_by_xpath(
                    ".//div[@id='columntableleaseCompsGrid']").find_elements_by_xpath(".//div[@role='columnheader']")
                for i in range(len(column_elements)):
                    if i > 0:
                        column_name = column_elements[i].find_element_by_xpath(".//span").text
                        if column_name == "Address":
                            column_names.append(column_name)
                for i in range(len(column_elements)):
                    if i > 0:
                        column_name = column_elements[i].find_element_by_xpath(".//span").text
                        if column_name and column_name != "Address":
                            column_names.append(column_name)

            df = pd.DataFrame(columns=column_names)
            
            num_of_pages_text = driver.get_element_list("//span[@class='label pages']")[0].text
            if num_of_pages_text:
                num_of_pages = int(driver.get_element_list("//span[@class='label pages']")[0].text)
            else:
                num_of_pages = 1

            if not column_names_fetch:
                driver.set_zoom_value(100)
                column_names_fetch = True

            csv_count = 0
            start_page = 1
            if city_index == start_city and min_max_range_index == start_range:
                start_page = start_city_page
            if start_page != 1:
                driver.get_element_list("//input[@class='page' and @type='text']")[0].clear()
                driver.send_keys("//input[@class='page' and @type='text']", start_page)
                driver.click_button_xpath("//button[@class='jump']")
                sleep(10)

            # Manually Resize the Column
            if not scroll_right_enable:
                print("Please resize column width manually!!!")
                sleep(150)
            else:
                sleep(6)

            # Page Loop
            for page_count in range((num_of_pages - (start_page - 1)) + 1):
                if page_count > 0:
                    prev_entries = {}
                    scroll_right_up_need = True
                    for scroll_down_index in range(5):
                        scroll_down_need = True
                        entries = {}
                        if scroll_right_enable:
                            for scroll_right_index in range(3):
                                rows = driver.driver.find_elements_by_xpath(".//div[contains(@id,'row') and contains(@id,'leaseCompsGrid')]")
                                    
                                for row_index in range(len(rows) - 3):
                                    row_id = 'row' + str(row_index) + 'leaseCompsGrid'
                                    cell_contents = rows[row_index].find_elements_by_xpath(".//div[contains(@class,'cellContent')]")
                                    if scroll_right_index == 0:
                                        entries[row_index] = {}

                                    if len(cell_contents) == 0:
                                        scroll_down_index = 4
                                        scroll_down_need = False
                                    else:
                                        diff_column_counts = len(cell_contents) + column_indexes[scroll_right_index - 1] - len(column_names)
                                        #print("Diff Column Counts: " + str(len(column_names)) + " : " + str(len(cell_contents)) + " : "  + str(column_indexes[scroll_right_index - 1]) + " : " +  str(diff_column_counts))
                                        if len(cell_contents) == 0:
                                            scroll_down_index = 4
                                            scroll_down_need = False
                                        for column_index in range(len(cell_contents)):
                                            column_name_index = column_index
                                            if scroll_right_index == 0:
                                                if column_index == 0:
                                                    column_name_index = 1
                                                if column_index == 1:
                                                    column_name_index = 2
                                                if column_index == 2:
                                                    column_name_index = 0
                                            if scroll_right_index == 1:
                                                if column_index < 4:
                                                    continue
                                                column_name_index = column_indexes[scroll_right_index - 1] + column_index - 4
                                            if scroll_right_index == 2:
                                                #print("Row Column Name Index: " + str(column_index) + " : " + str(diff_column_counts))
                                                if column_index < diff_column_counts:
                                                    continue
                                                column_name_index = column_indexes[scroll_right_index - 1] + column_index - diff_column_counts
                                                #print("Row Column Name Index: " + str(column_name_index))
                                            #print("Row Column: " + str(scroll_down_index) + " : "  + str(scroll_right_index) + " : " +  str(row_index) + " : " + str(column_name_index) + " : " + column_names[column_name_index] + " : " + cell_contents[column_index].text)
                                            if column_name_index < len(column_names):
                                                entries[row_index][column_names[column_name_index]] = cell_contents[column_index].text
                                
                                if scroll_right_index == 2:
                                    break

                                sroll_right_button = driver.driver.find_elements_by_xpath("//div[@id='jqxScrollBtnDownhorizontalScrollBarleaseCompsGrid']")[0]
                                if EC.element_to_be_clickable((By.ID, "jqxScrollBtnDownhorizontalScrollBarleaseCompsGrid")):
                                    for scroll_right_step in range(scroll_rights[scroll_right_index]):
                                        sroll_right_button.click()
                                        sleep(0.1)
                            
                            scroll_left_button = driver.driver.find_elements_by_xpath("//div[@id='jqxScrollBtnUphorizontalScrollBarleaseCompsGrid']")[0]
                            if EC.element_to_be_clickable((By.ID, "jqxScrollBtnUphorizontalScrollBarleaseCompsGrid")):
                                for scroll_left_index in range(2):
                                    for scroll_left_step in range(scroll_rights[scroll_left_index]):
                                        scroll_left_button.click()
                                        sleep(0.1)
                        else:
                            rows = driver.driver.find_elements_by_xpath(".//div[contains(@id,'row') and contains(@id,'leaseCompsGrid')]")
                            for row_index in range(len(rows) - 3):
                                entries[row_index] = {}
                                cell_contents = rows[row_index].find_elements_by_xpath(".//div[contains(@class,'cellContent')]")
                                if len(cell_contents) == 0:
                                    if scroll_down_index == 0:
                                        scroll_right_up_need = False
                                    scroll_down_index = 4
                                    scroll_down_need = False
                                for column_index in range(len(cell_contents)):
                                    column_name_index = column_index
                                    if column_index == 0:
                                        column_name_index = 1
                                    if column_index == 1:
                                        column_name_index = 2
                                    if column_index == 2:
                                        column_name_index = 0
                                    #print("Row Index: " + str(row_index) + ", Column Names Counts: " + str(len(column_names)) + ", Cell Counts: " + str(len(cell_contents)) + ", Column Index: " + str(column_index))
                                    entries[row_index][column_names[column_name_index]] = cell_contents[column_index].text

                        if prev_entries == entries:
                            scroll_down_index = 4
                            scroll_down_need = False
                        else:
                            prev_entries = entries
                            for entry_index in range(len(entries)):
                                df = df.append(entries[entry_index], ignore_index=True)

                        if scroll_down_index == 4:
                            break

                        if scroll_down_need:
                            scroll_down_button = driver.driver.find_elements_by_xpath("//div[@id='jqxScrollBtnDownverticalScrollBarleaseCompsGrid']")[0]
                            if EC.element_to_be_clickable((By.ID, "jqxScrollBtnDownverticalScrollBarleaseCompsGrid")):
                                for scroll_down_step in range(20):
                                    scroll_down_button.click()
                                    sleep(0.01)

                    if not scroll_right_enable and scroll_right_up_need:
                        # For safety scroll back up fully, before scraping that page.
                        scroll_up_button = driver.get_element_list("//div[@id='jqxScrollBtnUpverticalScrollBarleaseCompsGrid']")[0]
                        for scroll_up_step in range(105):
                            scroll_up_button.click()
                            sleep(0.1)

                    # Move to next page
                    if page_count % save_page_interval == 0:
                        df.drop_duplicates().to_csv(f'leasecomps_sf_medium/{city_to_scrape_file_name}/{min_sf}_{max_sf}/leasecomps_{start_page + (csv_count * save_page_interval)}_{(page_count - 1) + start_page}.csv', index=False)
                        df = df[0:0]  # Empty dataframe
                        csv_count = csv_count + 1

                    if page_count == num_of_pages - (start_page - 1):
                        if page_count % save_page_interval != 0:
                            df.drop_duplicates().to_csv(f'leasecomps_sf_medium/{city_to_scrape_file_name}/{min_sf}_{max_sf}/leasecomps_{start_page + (csv_count * save_page_interval)}_{(page_count - 1) + start_page}.csv', index=False)
                            df = df[0:0]
                        break

                    driver.get_element_list("//input[@class='page' and @type='text']")[0].clear()
                    driver.send_keys("//input[@class='page' and @type='text']", page_count + start_page)
                    driver.click_button_xpath("//button[@class='jump']")
                    sleep(10)

            path = f'leasecomps_sf_medium/{city_to_scrape_file_name}/{min_sf}_{max_sf}/'
            all_files = glob.glob(path + "/*.csv")

            li = []
            for filename in all_files:
                df = pd.read_csv(filename, usecols=column_names)
                li.append(df)

            if not os.path.exists(f'leasecomps_sf/{city_to_scrape_file_name}'):
                os.makedirs(f'leasecomps_sf/{city_to_scrape_file_name}')

            frame = pd.concat(li, axis=0)
            frame.drop_duplicates().set_index(column_names[0]).sort_index().to_csv(f'leasecomps_sf/{city_to_scrape_file_name}/final_{city_to_scrape_file_name}_{min_sf}_{max_sf}.csv')

            if min_max_range_index == len(min_max_ranges) - 1:
                path = f'leasecomps_sf/{city_to_scrape_file_name}/'
                all_files = glob.glob(path + "/*.csv")

                lli = []
                for filename in all_files:
                    df = pd.read_csv(filename, usecols=column_names)
                    lli.append(df)

                pd.concat(lli, axis=0).drop_duplicates().set_index(column_names[0]).sort_index().to_csv(f'leasecomps_sf/{city_to_scrape_file_name}/final_{city_to_scrape_file_name}.csv')

                if not os.path.exists(f'leasecomps_sf/{city_to_scrape_file_name}/sorted'):
                    os.makedirs(f'leasecomps_sf/{city_to_scrape_file_name}/sorted')
                    
                all_files = glob.glob(path + "/*.csv")
                for filename in all_files:
                    df = pd.read_csv(filename, usecols=column_names)
                    dfc = df.copy()
                    df_row_address = ""
                    for df_index, df_row in df.iterrows():
                        if df_row_address == df_row[column_names[0]]:
                            dfc.loc[df_index, column_names[0]] = ""
                        else:
                            df_row_address = df_row[column_names[0]]

                    dfc.to_csv(f'leasecomps_sf/{city_to_scrape_file_name}/sorted/{os.path.basename(filename)}', index=False)

            driver.driver.find_element_by_css_selector(".breadcrumbCountSection div.breadcrumb li.bc-2 a").click()
            sleep(8)

            driver.click_button_xpath("//span[text()='Market']")
            sleep(5)
            driver.click_button_xpath("//a[@id='removeAllGeographyTop']")
            sleep(1)
            market_types = driver.driver.find_element_by_xpath("//select[@id='market-type']").find_elements_by_xpath(".//option")
            market_types[0].click()
            sleep(1)

            if scroll_right_enable:
                sleep(5)
