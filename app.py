"""
<<<<<<< HEAD
    WEATHER SHOPPER AUTOMATION

=======
=============================================================================
                        WEATHER SHOPPER AUTOMATION
=============================================================================
>>>>>>> 041527a9b270d3494536d3b90a380293f61058fa
This script automates the process of buying products from weathershopper.pythonanywhere.com
based on the current temperature displayed on the website.

Logic:
- If temperature > 30°C: Buy sunscreens
- If temperature ≤ 30°C: Buy moisturizers
- Always selects the cheapest and most expensive products
<<<<<<< HEAD

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
=======
=============================================================================
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
>>>>>>> 041527a9b270d3494536d3b90a380293f61058fa

# Import all configurations from config file
from config import (
    # Application settings
    TEMP_THRESHOLD,
    BASE_URL,
<<<<<<< HEAD
=======
    
>>>>>>> 041527a9b270d3494536d3b90a380293f61058fa
    # XPath selectors
    BUY_SUNSCREENS_BTN,
    BUY_MOISTURIZERS_BTN,
    CART_BTN,
    STRIPE_PAY_BTN,
    SUCCESS_MSG,
    PRODUCT_CONTAINER,
    PRODUCT_PRICE,
    PRODUCT_NAME,
<<<<<<< HEAD
    # CSS selectors
    STRIPE_BTN,
    STRIPE_IFRAME,
    # Element locators
    TEMPERATURE_ID,    
=======
    
    # CSS selectors
    STRIPE_BTN,
    STRIPE_IFRAME,
    
    # Element locators
    TEMPERATURE_ID,
    HEADING_TAG,
    
>>>>>>> 041527a9b270d3494536d3b90a380293f61058fa
    # Test data
    EMAIL,
    CARD_NUMBER,
    EXPIRY,
    CVC,
<<<<<<< HEAD
=======
    
>>>>>>> 041527a9b270d3494536d3b90a380293f61058fa
    # Timeout settings
    IMPLICIT_WAIT,
    PAGE_LOAD_WAIT,
    ELEMENT_INTERACTION_WAIT,
    CLEANUP_WAIT
)

<<<<<<< HEAD

#           BROWSER SETUP SECTION


def setup_browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(IMPLICIT_WAIT)
    print("Browser setup complete")
    return driver

#     TEMPERATURE READING SECTION
=======
# =============================================================================
#                            BROWSER SETUP SECTION
# =============================================================================

def setup_browser():
    """
    Set up Chrome browser with optimal settings using config timeouts
    
    Returns:
        webdriver: Configured Chrome WebDriver instance
    """
    print("🔧 Setting up browser...")
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(IMPLICIT_WAIT)
    print("✅ Browser setup complete")
    return driver

# =============================================================================
#                         TEMPERATURE READING SECTION
# =============================================================================
>>>>>>> 041527a9b270d3494536d3b90a380293f61058fa

def check_temperature(driver):
    """
    Check the current temperature displayed on the homepage
    
<<<<<<< HEAD
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
=======
    Args:
        driver: WebDriver instance
        
    Returns:
        int: Temperature in Celsius, or None if error
    """
    print("\n🌡️ CHECKING TEMPERATURE...")
    print("=" * 50)
    
    try:
        # Find temperature element using config
        temp_element = driver.find_element(By.ID, TEMPERATURE_ID)
        temp_text = temp_element.text  # Gets "38°C"
        
        # Extract just the number (remove °C)
        temperature = int(temp_text.replace("°C", "").strip())
        
        print(f"🌡️ Current temperature: {temperature}°C")
        return temperature
        
    except Exception as e:
        print(f"❌ Could not read temperature: {e}")
>>>>>>> 041527a9b270d3494536d3b90a380293f61058fa
        return None

# =============================================================================
#                       PRODUCT DECISION LOGIC SECTION
# =============================================================================

def decide_product_type(temperature):
    """
    Decide whether to buy sunscreens or moisturizers based on temperature
    
<<<<<<< HEAD
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
=======
    Args:
        temperature (int): Current temperature in Celsius
        
    Returns:
        tuple: (product_type, button_text) for navigation
    """
    print("\n🤔 MAKING PRODUCT DECISION...")
    print("=" * 50)
    
    if temperature is None:
        print("⚠️ Cannot determine temperature, defaulting to moisturizers")
        return "moisturizer", BUY_MOISTURIZERS_BTN
    
    if temperature > TEMP_THRESHOLD:
        print(f"🌞 Temperature {temperature}°C is HOT (>{TEMP_THRESHOLD}°C) - Going for SUNSCREENS!")
        return "sunscreen", BUY_SUNSCREENS_BTN
    else:
        print(f"❄️ Temperature {temperature}°C is COOL (≤{TEMP_THRESHOLD}°C) - Going for MOISTURIZERS!")
        return "moisturizer", BUY_MOISTURIZERS_BTN

# =============================================================================
#                          PRODUCT SELECTION SECTION
# =============================================================================
>>>>>>> 041527a9b270d3494536d3b90a380293f61058fa

def find_and_add_cheapest_and_most_expensive(driver, product_type):
    """
    Find the cheapest and most expensive products and add only those to cart
<<<<<<< HEAD

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
                
=======
    
    Args:
        driver: WebDriver instance
        product_type (str): Type of product (sunscreen/moisturizer)
        
    Returns:
        int: Number of items added to cart
    """
    print(f"\n🛍️ PRODUCT SELECTION - {product_type.upper()}S")
    print("=" * 50)
    print(f"🔍 Finding all {product_type} products to compare prices...")
    
    try:
        # Find all product containers using config XPath
        product_containers = driver.find_elements(By.XPATH, PRODUCT_CONTAINER)
        print(f"🛒 Found {len(product_containers)} products")
        
        products = []  # List to store (name, price, button) tuples
        
        # Collect all product information
        print("\n📦 PRODUCT CATALOG:")
        print("-" * 30)
        for container in product_containers:
            try:
                # Get product name using config XPath
                name_element = container.find_element(By.XPATH, PRODUCT_NAME)
                product_name = name_element.text.strip()
                
                # Get product price using config XPath
>>>>>>> 041527a9b270d3494536d3b90a380293f61058fa
                price_element = container.find_element(By.XPATH, PRODUCT_PRICE)
                price_text = price_element.text.replace("Price: ", "").replace("₹", "").strip()
                price = int(price_text)
                
<<<<<<< HEAD
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
=======
                # Find the Add button within this container
                add_button = container.find_element(By.TAG_NAME, "button")
                
                products.append((product_name, price, add_button))
                print(f"📦 {product_name} - ₹{price}")
                    
            except Exception as e:
                print(f"⚠️  Couldn't process one product: {e}")
                continue
        
        if len(products) == 0:
            print("❌ No products found!")
            return 0
            
        # Find cheapest and most expensive products
        cheapest_product = min(products, key=lambda x: x[1])  # Sort by price (index 1)
        most_expensive_product = max(products, key=lambda x: x[1])
        
        print(f"\n🎯 SELECTION RESULTS:")
        print("-" * 30)
        print(f"💰 Cheapest {product_type}: {cheapest_product[0]} - ₹{cheapest_product[1]}")
        print(f"💎 Most expensive {product_type}: {most_expensive_product[0]} - ₹{most_expensive_product[1]}")
        
        items_added = 0
        
        # Add cheapest product
        print(f"\n🛒 Adding cheapest {product_type}...")
        cheapest_product[2].click()  # Click the button (index 2)
        items_added += 1
        print(f"✅ Added: {cheapest_product[0]} (₹{cheapest_product[1]})")
        time.sleep(ELEMENT_INTERACTION_WAIT)
        
        # Add most expensive product (if it's different from cheapest)
        if cheapest_product[0] != most_expensive_product[0]:
            print(f"🛒 Adding most expensive {product_type}...")
            most_expensive_product[2].click()  # Click the button
            items_added += 1
            print(f"✅ Added: {most_expensive_product[0]} (₹{most_expensive_product[1]})")
            time.sleep(ELEMENT_INTERACTION_WAIT)
        else:
            print("ℹ️  Cheapest and most expensive are the same product - only added once")
            
        return items_added
        
    except Exception as e:
        print(f"❌ Error finding {product_type} products: {e}")
        return 0

# =============================================================================
>>>>>>> 041527a9b270d3494536d3b90a380293f61058fa
#                         CART AND CHECKOUT SECTION
# =============================================================================

def go_to_cart_and_checkout(driver):
    """
    Navigate to cart and proceed with checkout process
<<<<<<< HEAD

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
        
=======
    
    Args:
        driver: WebDriver instance
    """
    print("\n💳 CART AND CHECKOUT PROCESS")
    print("=" * 50)
    print("🛒 Going to cart and checkout...")
    
    try:
        # Click the cart button using config XPath
        cart_button = driver.find_element(By.XPATH, CART_BTN)
        print(f"🛒 Found cart button: {cart_button.text}")
        cart_button.click()
        time.sleep(PAGE_LOAD_WAIT)
        
        print("✅ Successfully navigated to cart!")
        
        # Start payment process using config CSS selector
        print("💳 Starting payment process...")
        
        # Click Stripe button using config selector
        stripe_button = driver.find_element(By.CSS_SELECTOR, STRIPE_BTN)
        stripe_button.click()
        time.sleep(PAGE_LOAD_WAIT)
        print("✅ Selected 'Pay with Card'")
        
        # Fill in payment details using config iframe selector
        print("📝 Filling in payment details...")
        iframe = driver.find_element(By.CSS_SELECTOR, STRIPE_IFRAME)
        driver.switch_to.frame(iframe)
        
        # Enter payment information using config data
        driver.find_element(By.ID, "email").send_keys(EMAIL)
>>>>>>> 041527a9b270d3494536d3b90a380293f61058fa
        driver.execute_script(f"""
        document.querySelector("input#card_number").value = "{CARD_NUMBER}";
        document.querySelector("input#cc-exp").value = "{EXPIRY}";
        document.querySelector("input#cc-csc").value = "{CVC}";""")
        
<<<<<<< HEAD
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
=======
        print("💳 Payment details filled using config data")    
        
        # Click pay button using config XPath
        driver.find_element(By.XPATH, STRIPE_PAY_BTN).click()
        driver.switch_to.default_content()

        # Confirm payment success using config XPath
        success_msg = driver.find_element(By.XPATH, SUCCESS_MSG).text
        print(f"🎉 Payment Confirmation: {success_msg.strip()}")
        print(f"🌐 Final URL: {driver.current_url}")
        print("✅ Payment completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during cart/checkout process: {e}")
        # Print current page URL for debugging
        print(f"🔍 Current page: {driver.current_url}")
        
        # Try to find what elements are available for debugging
        try:
            page_source = driver.page_source
            if "cart" in page_source.lower():
                print("📋 Currently on cart-related page")
            if "checkout" in page_source.lower():
                print("💳 Currently on checkout-related page")
        except:
            pass

# =============================================================================
#                           MAIN EXECUTION SECTION
# =============================================================================

def main():
    """
    Main execution function that orchestrates the entire automation process
    """
    print("🚀 WEATHER SHOPPER AUTOMATION STARTED")
    print("=" * 70)
    
    # Set up browser
    driver = setup_browser()
    
    try:
        # Step 1: Navigate to homepage
        print("\n🏠 STEP 1: HOMEPAGE NAVIGATION")
        print("=" * 50)
        print("🏠 Going to home page...")
        driver.get(BASE_URL)
        time.sleep(PAGE_LOAD_WAIT)
        print("✅ Homepage loaded successfully")
        
        # Step 2: Check temperature and decide what to buy
        temperature = check_temperature(driver)
        product_type, button_xpath = decide_product_type(temperature)
        
        # Step 3: Navigate to product category
        print(f"\n🛒 STEP 2: PRODUCT CATEGORY NAVIGATION")
        print("=" * 50)
        print(f"🛒 Clicking product category button...")
        product_button = driver.find_element(By.XPATH, button_xpath)
        product_button.click()
        time.sleep(PAGE_LOAD_WAIT)
        print(f"✅ Successfully navigated to {product_type}s page")
        
        # Step 4: Add cheapest and most expensive items
        items_added = find_and_add_cheapest_and_most_expensive(driver, product_type)
        
        # Step 5: Verify cart status
        print(f"\n📊 STEP 3: CART VERIFICATION")
        print("=" * 50)
        print("📊 Checking cart...")
        time.sleep(ELEMENT_INTERACTION_WAIT)
        
        cart_button = driver.find_element(By.XPATH, CART_BTN)
        print(f"🛒 Cart status: {cart_button.text}")
        print(f"🎯 Total items added: {items_added}")
        
        # Step 6: Proceed with checkout if items were added
        if items_added > 0:
            print(f"\n🎉 SUCCESS SUMMARY")
            print("=" * 50)
            print(f"✅ Successfully added {product_type}s to cart based on weather!")
            if temperature and temperature > TEMP_THRESHOLD:
                print("☀️ Smart choice! Sunscreens for hot weather!")
            else:
                print("🧴 Smart choice! Moisturizers for cooler weather!")
            
            # Step 7: Complete checkout process
            go_to_cart_and_checkout(driver)
        else:
            print("\n❌ AUTOMATION FAILED")
            print("=" * 50)
            print("😞 No items were added to cart")
            
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR")
        print("=" * 50)
        print(f"💥 Something went wrong: {e}")
        
    finally:
        # Always close the browser
        print(f"\n🔚 CLEANUP")
        print("=" * 50)
        time.sleep(CLEANUP_WAIT)
        driver.quit()
        print("👋 Browser closed!")
        print("🏁 Automation completed!")

# =============================================================================
#                              SCRIPT ENTRY POINT
# =============================================================================
>>>>>>> 041527a9b270d3494536d3b90a380293f61058fa

if __name__ == "__main__":
    main()