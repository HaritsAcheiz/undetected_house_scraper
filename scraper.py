from dataclasses import dataclass
from selectolax.parser import HTMLParser
from urllib.parse import urljoin

import undetected_chromedriver as uc
from undetected_chromedriver.options import ChromeOptions

@dataclass
class Scraper():
    base_url: str = 'https://www.zillow.com'

    def webdriversetup(self):
        PROXY = '192.126.196.93:8800'
        opt = ChromeOptions()

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.6441.99 Safari/537.36'
        # 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.7608.60 Safari/537.36'
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.7.7709.37 Safari/537.36'
        # 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5694.46 Safari/537.36'
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.7.8254.20 Safari/537.36'

        opt.add_argument("--start-maximized")
        opt.add_argument("--headless=new")
        opt.add_argument(f'--user-agent={user_agent}')
        opt.add_argument("--no-sandbox")
        opt.add_argument(r'--user-data-dir=C:\Users\Muhammad Harits R\AppData\Local\Google\Chrome\User Data')
        opt.add_argument(r'--profile-directory=Default')
        opt.add_argument(f'--proxy-server={PROXY}')
        opt.add_argument("--disable-blink-features=AutomationControlled")

        driver = uc.Chrome(options=opt)

        return driver

    def fetch_html(self, driver, url):
        driver.get(url)
        driver.save_screenshot('screenshot1.png')
        ua = driver.execute_script("return navigator.userAgent")
        html = driver.page_source
        driver.close()
        print(html)
        print(ua)
        return html

    def get_listing_link(self, html):
        tree = HTMLParser(html)
        listings = tree.css('li.StyledListCardWrapper-srp__sc-wtsrtn-0')
        links=[]
        for listing in listings:
            print(listing.html)
            endpoint = listing.css_first('a').attributes.get('href', '')
            link = urljoin(self.base_url, endpoint)
            links.append(link)
        print(f'{len(links)} link(s) collected!')
        print(links)

    def main(self):
        driver = self.webdriversetup()
        html = self.fetch_html(driver=driver, url='https://www.zillow.com')
        self.get_listing_link(html)

if __name__ == '__main__':
    s = Scraper()
    s.main()