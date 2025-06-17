"""
Automated Selenium script to:
- Fetch temperature from the Weather Shopper homepage.
- Navigate to the Sunscreen or Moisturizer page based on temperature.
- Add the lowest priced item to the cart.
- Proceed to checkout using Stripe with dummy test data.
- Confirm the successful payment message after completion.
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import config  # Import the config module

# Use timing configurations from config
IMPLICIT_WAIT = getattr(config, 'IMPLICIT_WAIT', 10)
PAGE_LOAD_WAIT = getattr(config, 'PAGE_LOAD_WAIT', 3)
ELEMENT_INTERACTION_WAIT = getattr(config, 'ELEMENT_INTERACTION_WAIT', 1)
CLEANUP_WAIT = getattr(config, 'CLEANUP_WAIT', 2)

def setup_browser():
    """
    Set up Chrome browser with optimal settings using config timeouts
    
    """
    print("🔧 Setting up browser...")
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(IMPLICIT_WAIT)
    return driver

#        TEMPERATURE READING SECTION

def check_temperature(driver):
    """Check current temperature"""
    try:
        temp_element = driver.find_element(By.ID, config.TEMPERATURE_ID)
        temp_text = temp_element.text
        temperature = int(temp_text.replace("°C", "").strip())
        print(f"🌡️ Current temperature: {temperature}°C")
        return temperature
    except Exception as e:
        print(f"❌ Could not read temperature: {e}")
        return None


#          PRODUCT DECISION LOGIC SECTION

def decide_product_type(temperature):
    """Decide product type based on temperature"""
    if temperature is None:
        print("⚠️ Cannot determine temperature, defaulting to moisturizers")
        return "moisturizer", config.BUY_MOISTURIZERS_BTN

    if temperature > config.TEMP_THRESHOLD:
        print(f"🌞 Temperature {temperature}°C is HOT - Going for SUNSCREENS!")
        return "sunscreen", config.BUY_SUNSCREENS_BTN
    else:
        print(f"❄️ Temperature {temperature}°C is COOL - Going for MOISTURIZERS!")
        return "moisturizer", config.BUY_MOISTURIZERS_BTN

#     PRODUCT SELECTION SECTION

def find_and_add_cheapest_and_most_expensive(driver, product_type):
    """Find and add cheapest and most expensive products"""
    try:
        product_containers = driver.find_elements(By.XPATH, config.PRODUCT_CONTAINER)
        print(f"🛒 Found {len(product_containers)} products")

        products = []
        for container in product_containers:
            try:
                name_element = container.find_element(By.XPATH, config.PRODUCT_NAME)
                product_name = name_element.text.strip()                
                price_element = container.find_element(By.XPATH, config.PRODUCT_PRICE)
                price_text = price_element.text.replace("Price: ", "").replace("₹", "").strip()
                price = int(price_text)              
                add_button = container.find_element(By.TAG_NAME, "button")
                products.append((product_name, price, add_button))
                    
            except Exception as e:
                print(f"⚠️ Couldn't process one product: {e}")
                continue

        if len(products) == 0:
            print("❌ No products found!")
            return 0

        cheapest_product = min(products, key=lambda x: x[1])
        most_expensive_product = max(products, key=lambda x: x[1])

        print(f"💰 Cheapest: {cheapest_product[0]} - ₹{cheapest_product[1]}")
        print(f"💎 Most expensive: {most_expensive_product[0]} - ₹{most_expensive_product[1]}")

        items_added = 0

        # Add cheapest product
        cheapest_product[2].click()
        items_added += 1
        print(f"✅ Added: {cheapest_product[0]}")
        time.sleep(ELEMENT_INTERACTION_WAIT)

        # Add most expensive product (if different)
        if cheapest_product[0] != most_expensive_product[0]:
            most_expensive_product[2].click()
            items_added += 1
            print(f"✅ Added: {most_expensive_product[0]}")
            time.sleep(ELEMENT_INTERACTION_WAIT)
        else:
            print("ℹ️ Cheapest and most expensive are the same product")

        return items_added

    except Exception as e:
        print(f"❌ Error finding {product_type} products: {e}")
        return 0

#      CART AND CHECKOUT SECTION

def go_to_cart_and_checkout(driver):
    """Navigate to cart and complete checkout"""
    try:
        # Go to cart
        cart_button = driver.find_element(By.XPATH, config.CART_BTN)
        cart_button.click()
        time.sleep(PAGE_LOAD_WAIT)
        print("✅ Navigated to cart")

        # Verify items are in cart before proceeding
        try:
            # Check if there are any items in cart (look for checkout button or cart items)
            checkout_elements = driver.find_elements(By.CSS_SELECTOR, config.STRIPE_BTN)
            if not checkout_elements:
                print("❌ No items in cart - cannot proceed with checkout")
                return False
            print("✅ Items verified in cart")
        except Exception as e:
            print(f"⚠️ Could not verify cart contents: {e}")
            return False

        # Start payment process
        stripe_button = driver.find_element(By.CSS_SELECTOR, config.STRIPE_BTN)
        stripe_button.click()
        time.sleep(PAGE_LOAD_WAIT)
        print("✅ Payment process started")

        # Fill payment details
        iframe = driver.find_element(By.CSS_SELECTOR, config.STRIPE_IFRAME)
        driver.switch_to.frame(iframe)

        driver.find_element(By.ID, "email").send_keys(config.EMAIL)
        driver.execute_script(f"""
        document.querySelector("input#card_number").value = "{config.CARD_NUMBER}";
        document.querySelector("input#cc-exp").value = "{config.EXPIRY}";
        document.querySelector("input#cc-csc").value = "{config.CVC}";""")
        print("✅ Payment details filled")

        # Complete payment
        driver.find_element(By.XPATH, config.STRIPE_PAY_BTN).click()
        driver.switch_to.default_content()

        # Confirm success
        success_msg = driver.find_element(By.XPATH, config.SUCCESS_MSG).text
        print(f"🎉 Payment successful: {success_msg.strip()}")
        return True
        
    except Exception as e:
        print(f"❌ Checkout failed: {e}")
        return False

#      MAIN EXECUTION SECTION

def main():
    '''Main function to run the Weather Shopper automation script'''
    print("🚀 Weather Shopper Automation Started")
    driver = setup_browser()
    
        # Navigate to homepage
    driver.get(config.BASE_URL)
    time.sleep(PAGE_LOAD_WAIT)
    temperature = check_temperature(driver)
    product_type, button_xpath = decide_product_type(temperature)
        
        # Navigate to product category
    product_button = driver.find_element(By.XPATH, button_xpath)
    product_button.click()
    time.sleep(PAGE_LOAD_WAIT)
    print(f"✅ Navigated to {product_type}s page")
        
        # Add items to cart
    items_added = find_and_add_cheapest_and_most_expensive(driver, product_type)
        
        # Verify cart and proceed with checkout
    if items_added > 0:
        cart_button = driver.find_element(By.XPATH, config.CART_BTN)
        print(f"🛒 Cart: {cart_button.text}")
            
            # Complete checkout
        checkout_success = go_to_cart_and_checkout(driver)
        if checkout_success:
            print("🎉 Automation completed successfully!")
        else:
            print("❌ Checkout failed")
    else:
        print("❌ No items added - automation failed")
        time.sleep(CLEANUP_WAIT)
        driver.quit()
        print("✅ Browser closed")
      
#   SCRIPT ENTRY POINT

if __name__ == "__main__":
    main()