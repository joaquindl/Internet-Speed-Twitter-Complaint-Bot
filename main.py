from selenium import webdriver
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv('.env')

PROMISED_DOWN = 150
PROMISED_UP = 10
INTERNET_PROVIDER = os.getenv("INTERNET_PROVIDER")
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
TWITTER_USER = os.getenv("TWITTER_USER")
TWITTER_PASS = os.getenv("TWITTER_PASS")


class InternetSpeedTwitterBot:

    def __init__(self):
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)
        self.down = 0.0
        self.up = 0.0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        test_speed_btn = self.driver.find_element_by_xpath(
            '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a')
        test_speed_btn.click()
        sleep(45)
        down_speed = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div['
                                                       '3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div['
                                                       '2]/span')
        up_speed = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div['
                                                     '3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span')
        self.down = float(down_speed.text)
        self.up = float(up_speed.text)

    def tweet_at_provider(self):
        self.driver.get("https://www.twitter.com/")

        first_login_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div/main/div/div/div/div['
                                                            '1]/div/div[3]/a[2]')
        first_login_btn.click()

        sleep(2)
        login_user_input = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div['
                                                             '2]/form/div/div[1]/label/div/div[2]/div/input')
        login_password_input = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div['
                                                                 '2]/main/div/div/div[2]/form/div/div['
                                                                 '2]/label/div/div[2]/div/input')
        login_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div['
                                                      '2]/form/div/div[3]/div')
        login_user_input.send_keys(TWITTER_USER)
        login_password_input.send_keys(TWITTER_PASS)
        login_btn.click()

        sleep(2)
        tweet_input = self.driver.find_element_by_css_selector('.DraftEditor-root .public-DraftEditor-content '
                                                               '.public-DraftStyleDefault-block')

        tweet_btn = self.driver.find_element_by_css_selector("div[data-testid='tweetButtonInline'][role='button']")

        tweet_input.send_keys(f"{INTERNET_PROVIDER} ¿por qué la velocidad de mi internet es {self.down} "
                              f"de bajada y {self.up} de subida cuando pago por {PROMISED_DOWN} de bajada "
                              f"y {PROMISED_UP} de subida?")

        sleep(2)
        tweet_btn.click()

        self.driver.quit()


complaint_bot = InternetSpeedTwitterBot()

complaint_bot.get_internet_speed()

if complaint_bot.up < PROMISED_UP or complaint_bot.down < PROMISED_DOWN:
    complaint_bot.tweet_at_provider()
