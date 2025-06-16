"""
    WEATHER SHOPPER AUTOMATION

This script automates the process of buying products from weathershopper.pythonanywhere.com
based on the current temperature displayed on the website.

Logic:
- If temperature > 30°C: Buy sunscreens
- If temperature ≤ 30°C: Buy moisturizers
- Always selects the cheapest and most expensive products

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Import all configurations from config file
from config import (
    # Application settings
    TEMP_THRESHOLD,
    BASE_URL,
    # XPath selectors
    BUY_SUNSCREENS_BTN,
    BUY_MOISTURIZERS_BTN,
    CART_BTN,
    STRIPE_PAY_BTN,
    SUCCESS_MSG,
    PRODUCT_CONTAINER,
    PRODUCT_PRICE,
    PRODUCT_NAME,
    # CSS selectors
    STRIPE_BTN,
    STRIPE_IFRAME,
    # Element locators
    TEMPERATURE_ID,    
    # Test data
    EMAIL,
    CARD_NUMBER,
    EXPIRY,
    CVC,
    # Timeout settings
    IMPLICIT_WAIT,
    PAGE_LOAD_WAIT,
    ELEMENT_INTERACTION_WAIT,
    CLEANUP_WAIT
)


#           BROWSER SETUP SECTION


def setup_browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(IMPLICIT_WAIT)
    print("Browser setup complete")
    return driver

#     TEMPERATURE READING SECTION

def check_temperature(driver):
    """
    Check the current temperature displayed on the homepage
    
    """    
    try:
        wait = WebDriverWait(driver, PAGE_LOAD_WAIT)
        temp_element = wait.until(EC.presence_of_element_located((By.ID, TEMPERATURE_ID)))
        temp_text = temp_element.text

        temperature = int(temp_text.replace("°C", "").strip())
        print(f"Current temperature: {temperature}°C")
        return temperature

    except (TimeoutException, ValueError) as e:
        print(f"Could not read temperature: {e}")
        return None

# =============================================================================
#                       PRODUCT DECISION LOGIC SECTION
# =============================================================================

def decide_product_type(temperature):
    """
    Decide whether to buy sunscreens or moisturizers based on temperature
    
    """
    if temperature is None:
        return "moisturizer", BUY_MOISTURIZERS_BTN

    if temperature > TEMP_THRESHOLD:
        print(f"Temperature {temperature}°C > {TEMP_THRESHOLD}°C - Selecting sunscreens")
        return "sunscreen", BUY_SUNSCREENS_BTN
    else:
        print(f"Temperature {temperature}°C ≤ {TEMP_THRESHOLD}°C - Selecting moisturizers")
        return "moisturizer", BUY_MOISTURIZERS_BTN

#        PRODUCT SELECTION SECTION

def find_and_add_cheapest_and_most_expensive(driver, product_type):
    """
    Find the cheapest and most expensive products and add only those to cart

    """
    print(f"Finding {product_type} products...")

    try:
        wait = WebDriverWait(driver, PAGE_LOAD_WAIT)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, PRODUCT_CONTAINER)))
        
        product_containers = driver.find_elements(By.XPATH, PRODUCT_CONTAINER)
        print(f"Found {len(product_containers)} products")

        products = []

        for container in product_containers:
            try:
                name_element = container.find_element(By.XPATH, PRODUCT_NAME)
                product_name = name_element.text.strip()
                
                price_element = container.find_element(By.XPATH, PRODUCT_PRICE)
                price_text = price_element.text.replace("Price: ", "").replace("₹", "").strip()
                price = int(price_text)
                
                add_button = container.find_element(By.TAG_NAME, "button")
                products.append((product_name, price, add_button))
                    
            except Exception as e:
                print(f"Couldn't process one product: {e}")
                continue

        if len(products) == 0:
            print("No products found!")
            return 0

        cheapest_product = min(products, key=lambda x: x[1])
        most_expensive_product = max(products, key=lambda x: x[1])

        print(f"Cheapest: {cheapest_product[0]} - ₹{cheapest_product[1]}")
        print(f"Most expensive: {most_expensive_product[0]} - ₹{most_expensive_product[1]}")

        items_added = 0

        # Add cheapest product
        wait.until(EC.element_to_be_clickable(cheapest_product[2]))
        cheapest_product[2].click()
        items_added += 1
        print(f"Added: {cheapest_product[0]}")

        # Add most expensive product if different
        if cheapest_product[0] != most_expensive_product[0]:
            wait.until(EC.element_to_be_clickable(most_expensive_product[2]))
            most_expensive_product[2].click()
            items_added += 1
            print(f"Added: {most_expensive_product[0]}")
        else:
            print("Cheapest and most expensive are the same - added once")

        return items_added

    except Exception as e:
        print(f"Error finding {product_type} products: {e}")
        return 0

# =============================================================================
#                         CART VERIFICATION SECTION
# =============================================================================

def verify_cart_items(driver):
    """
    Verify that items are present in the cart before proceeding to checkout

    """
    try:
        wait = WebDriverWait(driver, PAGE_LOAD_WAIT)
        
        # Check if cart has items by looking for cart content
        cart_items = driver.find_elements(By.CSS_SELECTOR, ".table tbody tr, .cart-item, [class*='item']")
        
        if len(cart_items) > 0:
            return True
        else:
            # Alternative check - look for empty cart message or checkout button availability
            try:
                checkout_button = driver.find_element(By.CSS_SELECTOR, STRIPE_BTN)
                if checkout_button.is_enabled():
                    
                    return True
            except NoSuchElementException:
                pass
            
            print("Cart verification: No items found in cart")
            return False
            
    except Exception as e:
        print(f"Error verifying cart: {e}")
        return False

# =============================================================================
#                         CART AND CHECKOUT SECTION
# =============================================================================

def go_to_cart_and_checkout(driver):
    """
    Navigate to cart and proceed with checkout process

    """
    try:
        wait = WebDriverWait(driver, PAGE_LOAD_WAIT)
        
        # Click cart button
        cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, CART_BTN)))
        cart_button.click()
        print("Navigated to cart")

        # Verify cart has items before proceeding
        if not verify_cart_items(driver):
            print("Cart is empty - cannot proceed with checkout")
            return False

        # Click Stripe button
        stripe_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, STRIPE_BTN)))
        stripe_button.click()
        print("Selected 'Pay with Card'")

        # Fill payment details
        print("Filling payment details...")
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, STRIPE_IFRAME)))
        driver.switch_to.frame(iframe)

        # Wait for form elements and fill them
        wait.until(EC.presence_of_element_located((By.ID, "email")))
        driver.find_element(By.ID, "email").send_keys(EMAIL)
        
        driver.execute_script(f"""
        document.querySelector("input#card_number").value = "{CARD_NUMBER}";
        document.querySelector("input#cc-exp").value = "{EXPIRY}";
        document.querySelector("input#cc-csc").value = "{CVC}";""")
        
        print("Payment details filled")

        # Submit payment
        pay_button = wait.until(EC.element_to_be_clickable((By.XPATH, STRIPE_PAY_BTN)))
        pay_button.click()
        driver.switch_to.default_content()

        # Verify success
        success_element = wait.until(EC.presence_of_element_located((By.XPATH, SUCCESS_MSG)))
        success_msg = success_element.text
        print(f"Payment successful: {success_msg.strip()}")
        return True
        
    except TimeoutException as e:
        print(f"Timeout during checkout: {e}")
        return False
    except Exception as e:
        print(f"Error during checkout: {e}")
        print(f"Current page: {driver.current_url}")
        return False

#  MAIN EXECUTION SECTION

def main():
    driver = setup_browser()
    
    try:
        # Navigate to homepage
        print("Loading homepage...")
        driver.get(BASE_URL)
        
        # Check temperature and decide product type
        temperature = check_temperature(driver)
        product_type, button_xpath = decide_product_type(temperature)
        
        # Navigate to product category
        print(f"Navigating to {product_type}s page...")
        wait = WebDriverWait(driver, PAGE_LOAD_WAIT)
        product_button = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
        product_button.click()
        print(f"On {product_type}s page")
        
        # Add products to cart
        items_added = find_and_add_cheapest_and_most_expensive(driver, product_type)
        
        if items_added > 0:
            print(f"Successfully added {items_added} {product_type}(s) to cart")
            
            # Proceed with checkout
            checkout_success = go_to_cart_and_checkout(driver)
            
            if checkout_success:
                print("Automation completed successfully!")
            else:
                print("Checkout failed")
        else:
            print("No items added - automation failed")
            
    except Exception as e:
        print(f"Critical error: {e}")
        
    finally:
        driver.quit()

#Starting Point

if __name__ == "__main__":
    main()