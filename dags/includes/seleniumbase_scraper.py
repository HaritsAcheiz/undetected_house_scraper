import time
from dataclasses import dataclass, field
from random import uniform, choice
from typing import List

from selectolax.parser import HTMLParser
from urllib.parse import urljoin

from selenium.webdriver import Firefox, ActionChains, Keys
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


@dataclass
class Scraper():
    base_url: str = 'https://www.zillow.com'
    proxies: List[str] = field(default_factory=lambda: ['154.38.156.14', '154.12.113.202', '154.38.156.188', '154.12.112.208', '192.126.194.95',
                                                        '192.126.196.137', '154.12.112.163',  '192.126.194.135',
                                                        '154.38.156.187', '192.126.196.93', '154.12.112.208',
                                                        ])
    # uas: List[str] = field(default_factory=lambda: ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    #                                                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.8',
    #                                                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0 Herring/97.1.1600.1'])

    uas: List[str] = field(
        default_factory=lambda: ['Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/119.0',
                                 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:109.0) Gecko/20100101 Firefox/119.0',
                                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
                                 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0'])

    proxy_index: int = 0

    def webdriversetup(self):
        port = '8800'
        ua = choice(self.uas)
        ip = self.proxies[self.proxy_index]
        if self.proxy_index < 10:
            self.proxy_index += 1
        else:
            self.proxy_index = 0
        opt = FirefoxOptions()
        opt.add_argument("--start-maximized")
        opt.add_argument("--headless")
        opt.add_argument("--no-sandbox")
        # opt.add_argument("-profile")
        # opt.add_argument(profile_path)
        opt.add_argument("--disable-blink-features=AutomationControlled")

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
        opt.set_preference('dom.webdriver.enable', False)
        opt.set_preference('useAutomationExtension', False)
        opt.set_preference("browser.cache.disk.enable", False)
        opt.set_preference("browser.cache.memory.enable", False)
        opt.set_preference("browser.cache.offline.enable", False)
        opt.set_preference("network.http.use-cache", False)
        opt.set_preference("browser.privatebrowsing.autostart", True)

        print(ip, ua)
        driver = Firefox(options=opt)

        return driver

    def fetch_html(self, url):
        html = ''
        htmls = []
        last_page = False
        # while not last_page:
        driver = self.webdriversetup()
        # try:
        print(f'Fetching {url}')
        driver.maximize_window()
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'span.result-count')))

        # Scroll until element found
        clicking_objects = driver.find_elements(By.CSS_SELECTOR, 'ul.photo-cards.photo-cards_extra-attribution > li')
        for object in clicking_objects:
            try:
                time.sleep(uniform(0.1, 1.0))
                js_code = "arguments[0].scrollIntoView();"
                element = object.find_element(By.CSS_SELECTOR, 'a.property-card-link')
                driver.execute_script(js_code, element)
            except:
                continue
        htmls.append(driver.page_source)

        # Move to the next page
        next_page_elem = driver.find_element(By.CSS_SELECTOR, 'a[title="Next page"]')
        if next_page_elem.get_attribute('aria-disabled') == 'true':
            last_page = True
        else:
            last_page = False
            url = urljoin(self.base_url, next_page_elem.get_attribute('href'))
        # except Exception as e:
        # print(e)
        # wait = input("press any key to continue...")
        driver.close()
        # break
        # driver.close()

        return htmls

    def get_listing_link(self, htmls):
        collected_links = []
        for html in htmls:
            tree = HTMLParser(html)
            listings = tree.css('ul.photo-cards.photo-cards_extra-attribution > li')
            links = []
            for listing in listings:
                try:
                    endpoint = listing.css_first('a').attributes.get('href', '')
                    link = endpoint
                    links.append(link)
                except Exception as e:
                    print(e)
                    continue
            collected_links.extend(links)
        return collected_links


    def main(self):
        htmls = self.fetch_html(url='https://www.zillow.com/homes/Tucson,-AZ_rb/')
        collected_links = self.get_listing_link(htmls)
        print(collected_links)

if __name__ == '__main__':
    s = Scraper()
    s.main()