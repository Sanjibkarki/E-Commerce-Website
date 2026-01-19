import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import time

class ECommerceTest(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.base_url = "http://localhost:8000"

    def test_login_and_add_to_cart(self):

        driver = self.driver
        # Login Test
        driver.get(f"{self.base_url}/accounts/login") 
        driver.find_element(By.ID, "exampleInputEmail1").send_keys("admin123@gmail.com")
        driver.find_element(By.ID, "exampleInputPassword1").send_keys("admin123")
        driver.find_element(By.ID, "login-btn").click()
        time.sleep(2)
        self.assertIn("", driver.current_url, "Login Failed")

        # Add to Cart Test
        driver.get(f"{self.base_url}") 
        driver.execute_script("showProductDetail('4aadcc7f-ac95-45f8-ac66-83593c5ee524');")
        time.sleep(2)

        qty_input = driver.find_element(By.ID, "product-qty")
        

        add_to_cart_btn = driver.find_element(By.ID, "add-to-cart-btn")
        driver.execute_script("arguments[0].click();", add_to_cart_btn)
        time.sleep(2)
        
        driver.execute_script("closeProductModal();")
        time.sleep(1)
        self.assertFalse(driver.find_element(By.CLASS_NAME, "modal").is_displayed(), "Modal did not close")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
