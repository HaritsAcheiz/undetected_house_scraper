import undetected_chromedriver as uc
from dataclasses import dataclass

from undetected_chromedriver import ChromeOptions


@dataclass
class Scraper():



    def webdriversetup(self):
        opt = ChromeOptions()
        opt.add_argument("--start-maximized")
        opt.add_argument("--headless=new")
        opt.add_argument("--no-sandbox")
        opt.add_argument(r'--user-data-dir=D:\Naru\undetected_house_scraper\User Data')
        opt.add_argument(r'--profile-directory=Profile 1')

        driver = uc.Chrome(options=opt)

        return driver

    def fetch_html(self, driver, url):
        driver.get(url)
        html = driver.page_source
        driver.close()

        return html

    def main(self):
        driver = self.webdriversetup()
        html = self.fetch_html(driver=driver, url='https://www.zillow.com/tucson-az/rent-houses/')
        print(html)

if __name__ == '__main__':
    s = Scraper()
    s.main()