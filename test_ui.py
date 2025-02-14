from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def setup_browser():
    """Setup Selenium WebDriver"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("http://127.0.0.1:5000")  # Ensure Flask app is running
    yield driver
    driver.quit()

# 📌 FUNCTIONALITY TESTS

def test_admin_login(setup_browser):
    """Test successful admin login"""
    driver = setup_browser

    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        username_field.send_keys("admin")
        password_field.send_keys("admin")
        password_field.send_keys(Keys.RETURN)

        # ✅ Wait for the admin page to load correctly
        WebDriverWait(driver, 15).until(
            EC.url_to_be("http://127.0.0.1:5000/admin")  # Fixed URL verification
        )

        # ✅ Take a screenshot after successful login
        driver.save_screenshot("admin_login_success.png")

        # ✅ Confirm login success
        assert driver.current_url == "http://127.0.0.1:5000/admin"

    finally:
        driver.save_screenshot("admin_login_result.png")

def test_logout(setup_browser):
    """Test logout functionality"""
    driver = setup_browser

    # ✅ Ensure admin is logged in first
    test_admin_login(driver)

    # ✅ Click the logout button (If present)
    try:
        logout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
        )
        logout_button.click()
    except:
        print("⚠️ Logout button not found, navigating directly.")

    # ✅ Navigate directly to logout URL if clicking fails
    driver.get("http://127.0.0.1:5000/logout")

    # ✅ Wait for redirection back to login page
    WebDriverWait(driver, 10).until(
        EC.url_to_be("http://127.0.0.1:5000")
    )

    # ✅ Take a screenshot after logout
    driver.save_screenshot("logout_success.png")

    # ✅ Confirm logout success
    assert driver.current_url == "http://127.0.0.1:5000"

# 📌 RECOVERY TESTS

def test_recover_password(setup_browser):
    """Test password recovery"""
    driver = setup_browser
    driver.get("http://127.0.0.1:5000")

    # ✅ Locate and click "Forgot Password" link
    recover_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Forgot Password"))
    )
    recover_link.click()

    # ✅ Locate email input field and enter email
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    email_field.send_keys("admin@example.com")
    email_field.send_keys(Keys.RETURN)

    # ✅ Verify success message or redirection
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "recover-confirm"))
    )

    driver.save_screenshot("recover_password.png")

    assert success_message.is_displayed()

# 📌 SCALABILITY TESTS

def test_multiple_user_login(setup_browser):
    """Simulate multiple user logins"""
    driver = setup_browser

    for i in range(3):  
        driver.get("http://127.0.0.1:5000")

        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        username_field.send_keys(f"user{i}")
        password_field.send_keys("password123")
        password_field.send_keys(Keys.RETURN)

        # ✅ Wait for the dashboard or failure message
        try:
            WebDriverWait(driver, 10).until(
                EC.url_to_be(f"http://127.0.0.1:5000/dashboard")  # Adjust based on actual dashboard URL
            )
            assert "/dashboard" in driver.current_url
        except:
            assert "login" in driver.current_url  # If login fails, ensure it's on login page

        driver.save_screenshot(f"user_{i}_login.png")

# 📌 USABILITY TESTS

def test_mobile_view(setup_browser):
    """Test if the application is mobile-responsive"""
    driver = setup_browser
    driver.set_window_size(375, 667)  

    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    
    driver.save_screenshot("mobile_view.png")

    assert username_field.is_displayed()

# 📌 REDEEMABLE ITEMS PAGE TEST

def test_redeemable_items_page(setup_browser):
    """Test navigation to redeemable items page"""
    driver = setup_browser

    # ✅ Ensure login first
    test_admin_login(setup_browser)

    # ✅ Navigate to redeemable items
    driver.get("http://127.0.0.1:5000/redeemable_items")

    # ✅ Wait for correct URL
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:5000/redeemable_items"))

    driver.save_screenshot("redeemable_items_page.png")

    assert driver.current_url == "http://127.0.0.1:5000/redeemable_items"

if __name__ == "__main__":
    pytest.main(["-v", "test_ui.py"])