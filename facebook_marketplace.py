from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options

# Define search parameters
SEARCH_URL = "https://www.facebook.com/marketplace"
GEOGRAPHIC_AREA = "Vaughan, ON"
PRICE_MIN = 4000
PRICE_MAX = 10000
MAKE_MODEL = "Dodge Caravan"

# Set up Chrome options to use your Chrome profile
options = Options()
options.add_argument("user-data-dir=C:/Users/alima/AppData/Local/Google/Chrome/User Data")  # Path to Chrome User Data
options.add_argument("--profile-directory=Default")  # Default profile directory

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

try:
    # Open Facebook Marketplace
    driver.get(SEARCH_URL)
    print("Opened Facebook Marketplace.")

    # Wait for the search input field to be present
    search_box = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search Marketplace')]"))
    )
    print("Search box found.")
    search_box.send_keys(MAKE_MODEL + Keys.RETURN)
    print(f"Searching for {MAKE_MODEL}.")
    time.sleep(5)

    # Apply location filter
    location_filter = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Location']"))
    )
    location_filter.click()
    print("Location filter opened.")
    time.sleep(2)

    location_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@aria-label, 'Enter a location')]"))
    )
    location_input.clear()
    location_input.send_keys(GEOGRAPHIC_AREA)
    time.sleep(1)
    location_input.send_keys(Keys.RETURN)
    print(f"Location set to {GEOGRAPHIC_AREA}.")
    time.sleep(5)

    # Apply price range filter
    min_price_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Minimum price']"))
    )
    max_price_box = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Maximum price']"))
    )

    min_price_box.clear()
    max_price_box.clear()
    min_price_box.send_keys(str(PRICE_MIN))
    max_price_box.send_keys(str(PRICE_MAX))
    max_price_box.send_keys(Keys.RETURN)
    print(f"Price range set: ${PRICE_MIN} - ${PRICE_MAX}.")
    time.sleep(5)

    # Collect listings
    listings = driver.find_elements(By.XPATH, "//div[@role='article']")
    if not listings:
        print("No listings found. Please verify the search criteria.")
    else:
        for idx, listing in enumerate(listings, start=1):
            try:
                title = listing.find_element(By.XPATH, ".//span[contains(@class, 'text')]").text
                price = listing.find_element(By.XPATH, ".//span[contains(@class, 'price')]").text
                link = listing.find_element(By.XPATH, ".//a").get_attribute("href")
                print(f"{idx}. Title: {title}, Price: {price}, Link: {link}")
            except Exception as e:
                print(f"Error processing listing #{idx}: {e}")

except Exception as main_error:
    print("An error occurred:", main_error)
    # Save the page source for debugging
    with open("error_page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("Saved the page source to 'error_page_source.html'. Please inspect it for missing elements.")

finally:
    driver.quit()
    print("Browser closed.")
