import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from download_driver import download_chromedriver

HEADLESS = True
MAX_RETRIES = 5
RETRY_DELAY = 30
COOKIES_FILE = './cookies.json'

CODES = [
    "PNAT TWFF 7TJ9",
]

INPUT_ID = "pcm-form-code"
SUBMIT_CLASS = "add__points"
SUCCESS_CLASS = "premio-points__title"

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
CUSTOM_HEADERS = [
    "accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    "accept-language=pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6"
    "referer=https://www.nescafe-dolcegusto.com.br/premio/index/index/"
    'sec-ch-ua="Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"'
    "sec-ch-ua-mobile=?0"
    'sec-ch-ua-platform="macOS"'
    "sec-fetch-dest=document"
    "sec-fetch-mode=navigate"
    "sec-fetch-site=same-origin"
    "sec-fetch-user=?1"
    "upgrade-insecure-requests=1"
]


def main():
    driver_path = download_chromedriver()

    print("Loading cookies from the JSON file...")
    with open(COOKIES_FILE, 'r') as file:
        cookies = json.load(file)

    print("Setting up the webdriver...")
    service = Service(driver_path)
    options = Options()

    options.add_argument(f"user-agent={USER_AGENT}")

    if HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        options.add_argument("--no-sandbox")  # Bypass OS security model
        options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--ignore-certificate-errors')

    for header in CUSTOM_HEADERS:
        key, value = header.split("=")
        options.add_argument(f"--{key}={value}")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        initial_url = "https://www.nescafe-dolcegusto.com.br/club/?autofocus=1#pcm-form"
        reset_url = "https://www.nescafe-dolcegusto.com.br/club/?autofocus=1&clear-code=1#pcm-form"

        for attempt in range(MAX_RETRIES):
            try:
                print(f"Opening the website (Attempt {attempt + 1}/{MAX_RETRIES})...")
                driver.get(initial_url)

                print("Adding cookies to the driver...")
                for cookie in cookies:
                    if 'sameSite' in cookie:
                        del cookie['sameSite']
                    driver.add_cookie(cookie)

                print("Refreshing the page to apply cookies...")
                driver.refresh()

                print("Waiting for the form to be ready...")
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "pcm-form-code"))
                )
                print("Form is ready.")
                break  # Exit the retry loop if successful
            except Exception as e:
                print(f"Error: {e}")
                print("Website is not available. Retrying...")
                if attempt == MAX_RETRIES - 1:
                    print("Max retries reached. Exiting.")
                    driver.save_screenshot("debug_screenshot_final.png")
                    raise
                time.sleep(RETRY_DELAY)

        for i, code in enumerate(CODES, start=1):
            print(f"Processing code {i}/{len(CODES)}: {code}")

            input_element = driver.find_element(By.ID, INPUT_ID)
            input_element.clear()
            input_element.send_keys(code)

            print("Submitting the form...")
            submit_button = driver.find_element(By.CLASS_NAME, SUBMIT_CLASS)
            submit_button.click()

            print("Waiting for the confirmation message...")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, SUCCESS_CLASS))
            )

            print("Code submitted successfully. Waiting before the next submission...")
            time.sleep(2)  # Adjust the sleep time as necessary

            print("Navigating back to the form for the next code...")
            driver.get(reset_url)

            print("Waiting for the form to be ready again...")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, INPUT_ID))
            )
    except Exception:
        print("An error occurred. Saving a screenshot...")
        driver.save_screenshot("debug_screenshot_error.png")
        raise
    finally:
        print("Closing the browser...")
        driver.quit()

if __name__ == "__main__":
    main()
