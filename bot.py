import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    return webdriver.Chrome(options=chrome_options)

def visit_notes(driver):
    try:
        # Log in
        if not driver.current_url.endswith('/login'):
            driver.get('http://localhost:8081/login')

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'email'))
            )
            
            driver.find_element(By.NAME ,'email').send_keys('xss@example.com')
            driver.find_element(By.NAME, 'password').send_keys('NoWayYouCanStealMyCookies!')
            driver.find_element(By.NAME, 'login').click()
        print("Logged in.")

        driver.add_cookie({
            'name': 'Flag', 
            'value': "FLAG{s7Or3d_XsS_9On3_CR42YYy!}"
        })

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        # Visit the page with XSS
        driver.get('http://localhost:8081/notes')
        print("Visting..")
        # Print page content or check for expected changes
        # print(driver.page_source)  # This is useful for debugging
        # driver.close()
        driver.quit()

    except Exception as e:
        print(f"Error: {e}")

# Start the scheduling task
if __name__ == "__main__":

    while True:
        driver = create_driver()
        visit_notes(driver)
        time.sleep(180) # Wait for 3 minutes before sending next request
