import os
import pandas as pd
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

logging.basicConfig(level=logging.INFO)

class SeleniumWebDriverContextManager:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

def extract_pie_data(driver):
    slices = driver.find_elements(By.CSS_SELECTOR, '.pielayer .slice')
    if len(slices) > 0:
        data = []
        for slice_elem in slices:
            try:
                tspans = slice_elem.find_elements(By.TAG_NAME, 'tspan')
                if len(tspans) > 0:
                    line1 = tspans[0].text if len(tspans) > 0 else ''
                    line2 = tspans[1].text if len(tspans) > 1 else ''
                    data.append({'Facility Type': line1, 'Min Average Time Spent': line2})
            except Exception as e:
                logging.warning(f"Error extracting slice text: {e}")
        return pd.DataFrame(data)
    return None


def extract_columns_data(driver, wait):
    y_columns = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.y-column')))
    columns_data = []
    for col in y_columns:
        cell_texts = col.find_elements(By.CSS_SELECTOR, '.cell-text')
        columns_data.append([t.text for t in cell_texts])
    return columns_data

def save_screenshot_and_data(driver, idx, data_extractor, prefix="doughnut"):
    screenshot_file = f"screenshot{idx}.png"
    data_file = f"{prefix}{idx}.csv"
    driver.save_screenshot(screenshot_file)
    logging.info(f"Saved {screenshot_file}")
    df = data_extractor(driver)
    if not df.empty:
        df.to_csv(data_file, index=False)
        logging.info(f"Saved {data_file}")

if __name__ == "__main__":
    FILE_PATH = "report.html"
    TABLE_DATA = "table.csv"
    TIMEOUT = 10

    with SeleniumWebDriverContextManager() as driver:
        driver.get("file://" + os.path.abspath(FILE_PATH))
        wait = WebDriverWait(driver, TIMEOUT)

        # Extract columns data
        try:
            columns_data = extract_columns_data(driver, wait)
            if len(columns_data) == 3:
                facility_type = columns_data[0][:-1]
                visit_date = columns_data[1][:-1]
                avg_time_spent = columns_data[2][:-1]
                df = pd.DataFrame({
                    columns_data[0][-1]: facility_type,
                    columns_data[1][-1]: visit_date,
                    columns_data[2][-1]: avg_time_spent
                })
                df.to_csv(TABLE_DATA, index=False)
                logging.info(f"Saved columns data to {TABLE_DATA}")
            else:
                logging.warning(f"Could not find all columns. Found: {len(columns_data)}")
                for i, col in enumerate(columns_data):
                    logging.warning(f"Column {i} length: {len(col)} | Data: {col}")
        except TimeoutException:
            logging.error("Timeout while extracting columns data.")

        # Wait for filters and pie chart
        try:
            filters = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.groups .traces')))
            pie_layer = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.pielayer')))
        except TimeoutException:
            logging.error("Filters or pie chart not found.")
            exit(1)

        screenshot_idx = 0
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        save_screenshot_and_data(driver, screenshot_idx, extract_pie_data)
        screenshot_idx += 1

        # Iterate through each filter
        for i, filter_elem in enumerate(filters):
            try:
                opacity = filter_elem.value_of_css_property('opacity')
                if opacity == '1':
                    filter_elem.click()
                    wait.until(lambda d: filter_elem.value_of_css_property('opacity') == '0.5')
                    save_screenshot_and_data(driver, screenshot_idx, extract_pie_data)
                    screenshot_idx += 1

                    # Click again to return to initial state
                    filter_elem.click()
                    wait.until(lambda d: filter_elem.value_of_css_property('opacity') == '1')
            except (TimeoutException, ElementClickInterceptedException, NoSuchElementException) as e:
                logging.warning(f"Error with filter {i}: {e}")

        # Edge case: all filters unselected (no chart)
        try:
            for filter_elem in filters:
                opacity = filter_elem.value_of_css_property('opacity')
                if opacity == '1':
                    filter_elem.click()
                    wait.until(lambda d: filter_elem.value_of_css_property('opacity') == '0.5')
            logging.info(f"Filtered out {len(filters)} filters.")
            save_screenshot_and_data(driver, screenshot_idx, extract_pie_data)
        except Exception as e:
            logging.error(f"Edge case (all filters off) not handled: {e}")
