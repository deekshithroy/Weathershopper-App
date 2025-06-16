<<<<<<< HEAD
"""
=============================================================================
                        WEATHER SHOPPER - CONFIGURATION FILE
=============================================================================
This file contains all configuration constants, XPath selectors, CSS selectors,
and test data used in the Weather Shopper automation script.
=============================================================================
"""

# Temperature threshold for product decision
TEMP_THRESHOLD = 30

# Base URL
BASE_URL = "https://weathershopper.pythonanywhere.com/"

# Navigation buttons
BUY_SUNSCREENS_BTN = "//button[text()='Buy sunscreens']"
BUY_MOISTURIZERS_BTN = "//button[text()='Buy moisturizers']"

# Cart and checkout
CART_BTN = "//button[contains(text(),'Cart')]"
STRIPE_PAY_BTN = "//span[contains(text(),'Pay INR')]"

# Success message
SUCCESS_MSG = "//*[contains(text(),'success')]"

# Product selectors
PRODUCT_CONTAINER = "//p[contains(text(),'Price')]/.."
PRODUCT_PRICE = "./p[contains(text(),'Price')]"
PRODUCT_NAME = "./p[1]"

# Stripe payment
STRIPE_BTN = "button.stripe-button-el"
STRIPE_IFRAME = "iframe[name='stripe_checkout_app']"

# Temperature element
TEMPERATURE_ID = "temperature"

# Page elements
HEADING_TAG = "h2"

# Stripe test payment data
EMAIL = "Deekshi@gmail.com"
CARD_NUMBER = "4242 4242 4242 4242"
EXPIRY = "12/25"
CVC = "123"

# Wait times (in seconds)
IMPLICIT_WAIT = 10
PAGE_LOAD_WAIT = 3
ELEMENT_INTERACTION_WAIT = 1
CLEANUP_WAIT = 3
=======
"""
=============================================================================
                        WEATHER SHOPPER - CONFIGURATION FILE
=============================================================================
This file contains all configuration constants, XPath selectors, CSS selectors,
and test data used in the Weather Shopper automation script.
=============================================================================
"""

# =============================================================================
#                           APPLICATION SETTINGS
# =============================================================================

# Temperature threshold for product decision
TEMP_THRESHOLD = 30

# Base URL
BASE_URL = "https://weathershopper.pythonanywhere.com/"

# =============================================================================
#                              XPATH SELECTORS
# =============================================================================

# Navigation buttons
BUY_SUNSCREENS_BTN = "//button[text()='Buy sunscreens']"
BUY_MOISTURIZERS_BTN = "//button[text()='Buy moisturizers']"

# Cart and checkout
CART_BTN = "//button[contains(text(),'Cart')]"
STRIPE_PAY_BTN = "//span[contains(text(),'Pay INR')]"

# Success message
SUCCESS_MSG = "//*[contains(text(),'success')]"

# Product selectors
PRODUCT_CONTAINER = "//p[contains(text(),'Price')]/.."
PRODUCT_PRICE = "./p[contains(text(),'Price')]"
PRODUCT_NAME = "./p[1]"

# =============================================================================
#                             CSS SELECTORS
# =============================================================================

# Stripe payment
STRIPE_BTN = "button.stripe-button-el"
STRIPE_IFRAME = "iframe[name='stripe_checkout_app']"

# =============================================================================
#                            ELEMENT LOCATORS
# =============================================================================

# Temperature element
TEMPERATURE_ID = "temperature"

# Page elements
HEADING_TAG = "h2"

# =============================================================================
#                              TEST DATA
# =============================================================================

# Stripe test payment data
EMAIL = "Deekshi@gmail.com"
CARD_NUMBER = "4242 4242 4242 4242"
EXPIRY = "12/25"
CVC = "123"

# =============================================================================
#                            TIMEOUT SETTINGS
# =============================================================================

# Wait times (in seconds)
IMPLICIT_WAIT = 10
PAGE_LOAD_WAIT = 3
ELEMENT_INTERACTION_WAIT = 1
CLEANUP_WAIT = 3
>>>>>>> 041527a9b270d3494536d3b90a380293f61058fa
