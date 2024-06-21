from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Define the website and path to ChromeDriver
website = 'https://www.thesun.co.uk/sport/football/'
path = 'C:/Users/agnik/OneDrive/Documents/Selenium/chromedriver.exe'  # Use forward slashes

# Create Chrome options to ignore SSL errors
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Initialize the Chrome WebDriver with options
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get(website)
    time.sleep(5)  # Wait for the page to load

    containers = driver.find_elements(by='xpath', value='//div[@class="teaser__copy-container"]')

    titles = []
    subtitles = []
    links = []

    for container in containers:
        try:
            title = container.find_element(by='xpath', value='//div[@class="teaser__copy-container"]/a/span').text
            subtitle_text = container.find_element(by='xpath', value='//div[@class="teaser__copy-container"]/a/h3').text
            link = container.find_element(by='xpath', value='//div[@class="teaser__copy-container"]/a').get_attribute("href")

            titles.append(title)
            subtitles.append(subtitle_text)
            links.append(link)
        except Exception as e:
            print(f"An error occurred while processing container: {e}")

    my_dict = {'titles': titles, 'subtitles': subtitles, 'links': links}
    df_headlines = pd.DataFrame(my_dict)
    df_headlines.to_csv('headline.csv', index=False)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
