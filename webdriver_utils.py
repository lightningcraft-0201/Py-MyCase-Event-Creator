from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

def setup_webdriver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--window-size=1920,1080")  # Set a window size
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  # This may be necessary if you're running on Windows.
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def drive_init():
    driver = setup_webdriver()
    driver.get('https://www.mycase.com/login/')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_session_email')))
    username_field = driver.find_element(By.ID, 'login_session_email')
    password_field = driver.find_element(By.ID, 'login_session_password')
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

    username_field.send_keys(os.getenv("USER_NAME"))
    password_field.send_keys(os.getenv("USER_PASS"))
    submit_button.click()

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.modal-title")))
        cancel_button = driver.find_element(By.CSS_SELECTOR, "button.cancel-button.btn-link.btn.btn-link")
        cancel_button.click()
    except TimeoutException:
        print("The element 'Upcoming Reminders' was not found.")
    return driver

def create_event(case_number, event_name, start_date, start_time, hearing_type, location, subject, msg_id, received_date):
    driver = drive_init()
    
    try: 
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".dashboard-add-item-section.d-flex"))
        )

        # Navigate to the add event section
        element = driver.find_element(By.CSS_SELECTOR, ".dashboard-event.test-add-event.pendo-add-event.pendo-exp2-add-event")
        element.click()

        # Wait until the case input field is visible and interact with it
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-activedescendant="react-select-2--option-0"]'))
        )
        input_case = driver.find_element(By.CSS_SELECTOR, 'input[aria-activedescendant="react-select-2--option-0"]')
        input_case.send_keys(case_number)
        time.sleep(1.5)  # Wait for dropdown to populate

        # If case number is not found, append to log or handle as needed
        if "results" in driver.find_element(By.CSS_SELECTOR, ".Select-menu-outer").text:
            print("No case found for:", case_number)
            return

        input_case.send_keys(Keys.ENTER)

        # Enter the event name
        input_name = driver.find_element(By.ID, "name")
        input_name.clear()
        input_name.send_keys(event_name)

        # Set the event color/category, if applicable
        color_element = driver.find_element(By.ID, "chosen-category")
        color_element.click()
        # Selecting a specific category item
        color_item = driver.find_element(By.ID, "item_category_2085055")
        color_item.click()

        # Set start date and time
        input_start_date = driver.find_element(By.ID, "appointment_rule_start_date")
        input_start_date.clear()
        input_start_date.send_keys(start_date)
        input_start_date.send_keys(Keys.ENTER)

        input_start_time = driver.find_element(By.ID, "appointment_rule_start_time")
        input_start_time.clear()
        input_start_time.send_keys(start_time)
        input_start_time.send_keys(Keys.ENTER)

        # Set location
        location_element = driver.find_element(By.CSS_SELECTOR, ".col-sm-8")
        location_element.click()
        input_location = driver.find_element(By.CSS_SELECTOR, 'input[aria-activedescendant="react-select-3--option-0"]')
        input_location.send_keys(location)
        input_location.send_keys(Keys.ENTER)

        # Check and click on sharing and attending checkboxes
        checkbox_share = driver.find_element(By.NAME, "client-share-all")
        if not checkbox_share.is_selected():
            checkbox_share.click()

        checkbox_attend = driver.find_element(By.NAME, "client-attend-all")
        if not checkbox_attend.is_selected():
            checkbox_attend.click()

        # Click the create button to finalize the event
        create_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-cta-primary")
        create_button.click()

        print("Event created successfully:", event_name)
        time.sleep(2)  # Wait for the event to be processed
        driver.quit()
    except Exception as e:
        driver.quit()
        time.sleep(2)
        create_event()
