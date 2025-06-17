
# CONFIG FILE

# Temperature threshold for product decision
TEMP_THRESHOLD = 30

# Base URL
BASE_URL = "https://weathershopper.pythonanywhere.com/"

# Browser wait times (in seconds)
IMPLICIT_WAIT = 10
PAGE_LOAD_WAIT = 3
ELEMENT_INTERACTION_WAIT = 1
CLEANUP_WAIT = 2


# Navigation buttons
BUY_SUNSCREENS_BTN = "//button[text()='Buy sunscreens']"
BUY_MOISTURIZERS_BTN = "//button[text()='Buy moisturizers']"
CART_BTN = "//button[contains(text(),'Cart')]"

# Product page elements
PRODUCT_CONTAINER = "//p[contains(text(),'Price')]/.."
PRODUCT_PRICE = "./p[contains(text(),'Price')]"
PRODUCT_NAME = "./p[1]"

# Checkout and payment elements
STRIPE_PAY_BTN = "//span[contains(text(),'Pay INR')]"
SUCCESS_MSG = "//*[contains(text(),'success')]"

# Stripe payment elements
STRIPE_BTN = "button.stripe-button-el"
STRIPE_IFRAME = "iframe[name='stripe_checkout_app']"

# Temperature element
TEMPERATURE_ID = "temperature"

# Stripe test payment information
EMAIL = "dheekshi@gmail.com"
CARD_NUMBER = "4242 4242 4242 4242"
EXPIRY = "12/25"
CVC = "123"

# HTML tag selectors
HEADING_TAG = "h2"