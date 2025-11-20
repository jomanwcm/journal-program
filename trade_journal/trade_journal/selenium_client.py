from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

CHART_URL = "https://www.tradingview.com/chart/DewgUjZm/"

def open_tradingview_and_click_login():
    driver = webdriver.Chrome()
    driver.get("https://www.tradingview.com")
    driver.maximize_window()

    wait = WebDriverWait(driver, 20)

    # 1. Click the anonymous user-menu button
    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[aria-label='Open user menu']")
        )
    )
    login_button.click()
    print("Clicked: user menu button")

    # 2. Click “Sign in”
    dropdown_sign_in = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-name='header-user-menu-sign-in']")
        )
    )
    dropdown_sign_in.click()
    print("Clicked: Sign in")

    # 3. Click “Email” login option
    email_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[name='Email']")
        )
    )
    email_button.click()
    print("Clicked: Email login")

    # ------------------------------------------------
    # 4. Enter Email
    # ------------------------------------------------
    email_input = wait.until(
        EC.presence_of_element_located((By.ID, "id_username"))
    )
    email_input.clear()
    email_input.send_keys("cryto.tracy@gmail.com")
    print("Entered email")

    # ------------------------------------------------
    # 5. Enter Password
    # ------------------------------------------------
    password_input = wait.until(
        EC.presence_of_element_located((By.ID, "id_password"))
    )
    password_input.clear()
    password_input.send_keys("!!Jojo1234")
    print("Entered password")

    # ------------------------------------------------
    # 6. Click the final Sign in button
    # ------------------------------------------------
    final_sign_in = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[text()='Sign in']]")
        )
    )
    final_sign_in.click()
    print("Clicked: Final Sign in")

    wait.until(EC.invisibility_of_element_located((By.ID, "id_username")))

    print("Sign-in page finished loading. Login successful.")


    driver.get("https://www.tradingview.com/chart/DewgUjZm/")
    print("Redirected to chart page.")


    dont_need_button = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-overflow-tooltip-text=\"Don't need\"]")
    )
    )
    dont_need_button.click()
    print("Clicked: Don't need")

    return driver


def goto_chart_and_dismiss_popup(driver, chart_url: str = CHART_URL):
    """
    Reuse an existing Selenium driver:
    - navigate to the chart URL
    - click 'Don't need' if that popup appears.
    """
    

    if driver is None:
        raise ValueError("driver is None – Selenium is not running")

    wait = WebDriverWait(driver, 20)

    # Navigate to the chart
    driver.get(chart_url)
    print(f"Redirected to chart page: {chart_url}")

    # Try to click "Don't need" popup; ignore if it doesn't appear
    try:
        dont_need_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-overflow-tooltip-text=\"Don't need\"]")
            )
        )
        dont_need_button.click()
        print("Clicked: Don't need")
    except TimeoutException:
        print("No 'Don't need' button appeared.")


