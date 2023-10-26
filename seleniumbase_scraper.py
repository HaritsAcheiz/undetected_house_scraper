import seleniumbase as sb

from dataclasses import dataclass
from selectolax.parser import HTMLParser
from urllib.parse import urljoin


@dataclass
class Scraper():
    base_url: str = 'https://www.zillow.com'


    def webdriversetup(self):
        PROXY = '154.12.112.208:8800'
        # opt = ChromeOptions()
        # opt.add_argument("--start-maximized")
        # opt.add_argument("--headless=new")
        # opt.add_argument("--no-sandbox")
        # opt.add_argument("--user-data-dir=/home/haritz/snap/chromium/common/chromium")
        # opt.add_argument(r'--profile-directory=Default')
        # opt.add_argument(f'--proxy-server={PROXY}')
        # opt.add_argument("--disable-blink-features=AutomationControlled")

        driver = sb.Driver(uc=True, user_data_dir='/home/haritz/snap/chromium/common/chromium', proxy=PROXY)

        return driver

    def fetch_html(self, driver, url):
        # driver.get(url)
        with driver:
            driver.open(url)
            html = driver.get_page_source
        # html = driver.page_source
        print(html)
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
        html = self.fetch_html(driver=driver, url='https://www.zillow.com/homes/Tucson,-AZ_rb/')
        self.get_listing_link(html)

if __name__ == '__main__':
    s = Scraper()
    s.main()