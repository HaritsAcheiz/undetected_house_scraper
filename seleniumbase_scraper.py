import time
from dataclasses import dataclass
from random import uniform

from selectolax.parser import HTMLParser
from urllib.parse import urljoin

from selenium.webdriver import Firefox, ActionChains
from selenium.webdriver import FirefoxOptions


@dataclass
class Scraper():
    base_url: str = 'https://www.zillow.com'


    def webdriversetup(self):
        # ip = '154.12.112.208'
        ip = '192.126.194.95'
        # ip = '192.126.196.137'
# 154.12.112.163:8800
# 154.38.156.14:8800
# 192.126.194.135:8800
# 154.38.156.187:8800
# 192.126.196.93:8800
# 154.12.112.208:8800
# 154.12.113.202:8800
# 154.38.156.188:8800'

        port = '8800'
        # ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'
        # ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.8'
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0 Herring/97.1.1600.1'

        # profile_path = "C:/Users/Muhammad Harits R/AppData/Roaming/Mozilla/Firefox/Profiles/cr7alez2.default-release"
        opt = FirefoxOptions()
        # opt.add_argument("--window-size=1024,768")
        opt.add_argument("--start-maximized")
        # opt.add_argument("--headless")
        # opt.add_argument("--no-sandbox")
        # opt.add_argument("-profile")
        # opt.add_argument(profile_path)
        # opt.add_argument("--disable-blink-features=AutomationControlled")

        opt.set_preference("general.useragent.override", ua)
        opt.set_preference('network.proxy.type', 1)
        opt.set_preference('network.proxy.socks', ip)
        opt.set_preference('network.proxy.socks_port', int(port))
        opt.set_preference('network.proxy.socks_version', 4)
        opt.set_preference('network.proxy.socks_remote_dns', True)
        opt.set_preference('network.proxy.http', ip)
        opt.set_preference('network.proxy.http_port', int(port))
        opt.set_preference('network.proxy.ssl', ip)
        opt.set_preference('network.proxy.ssl_port', int(port))
        # opt.set_preference('dom.webdriver.enable', False)
        # opt.set_preference('useAutomationExtension', False)
        # opt.set_preference("browser.cache.disk.enable", False)
        # opt.set_preference("browser.cache.memory.enable", False)
        # opt.set_preference("browser.cache.offline.enable", False)
        # opt.set_preference("network.http.use-cache", False)
        # opt.set_preference("browser.privatebrowsing.autostart", True)

        driver = Firefox(options=opt)

        return driver

    def fetch_html(self, driver, url):
        driver.get(url)
        html = driver.page_source
        wait = input("press any key to continue...")
        driver.close()
        print(html)
        return html

    def get_listing_link(self, html):
        tree = HTMLParser(html)
        listings = tree.css('ul.photo-cards.photo-cards_extra-attribution > li')
        links=[]
        for listing in listings:
            print("---------------------------------------------------------------------")
            print(listing.html)
            try:
                endpoint = listing.css_first('a').attributes.get('href', '')
                link = endpoint
                links.append(link)
            except Exception as e:
                print(e)
                continue
        print(f'{len(links)} link(s) collected!')
        print(links)

    def main(self):
        driver = self.webdriversetup()

        # Wait and move the cursor to mimic human behavior
        time.sleep(uniform(0.1, 1.0))

        # action = ActionChains(driver)
        # action.click_and_hold()
        # action.move_by_offset(1, 1)
        # action.move_by_offset(1, 1)
        # action.move_by_offset(1, 1)
        # action.move_by_offset(1, 1)
        # action.move_by_offset(1, 1)
        # action.move_by_offset(1, 1)
        # action.move_by_offset(1, 1)
        # action.move_by_offset(1, 1)
        # action.move_by_offset(1, 1)
        # action.move_by_offset(1, 1)
        # action.move_by_offset(1, 6)
        # action.move_by_offset(1, 8)
        # action.release()
        # action.perform()
        # action.reset_actions()


        html = self.fetch_html(driver=driver, url='https://www.zillow.com/homes/Tucson,-AZ_rb/')
        self.get_listing_link(html)

if __name__ == '__main__':
    s = Scraper()
    s.main()