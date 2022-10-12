import re
from requests_html import HTML
from urllib.parse import urlparse
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def scraper(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(5)
    return driver.page_source

def extract_id_slug(url_path):
    path = url_path
    if path.startswith('http'):
        parsed_url = urlparse(path)
        path = parsed_url.path
    regex = r"^[^\s]+/(?P<id>\d+)-(?P<slug>[\w_-]+)$"
    group = re.match(regex, path)
    if not group:
        return None, None, path
    return group['id'], group['slug'], path

def get_product_data(url, content):
    id_, slug_, path = extract_id_slug(url)
    titleEl = content.find(".design-title", first=True)
    data = {
        'id': id_,
        'slug': slug_,
        'path': path,
    }
    title = None
    if titleEl == None:
        return data
    title = titleEl.text
    data['title'] = title
    sizeEl = content.find("#fabric-size", first=True)
    size = None
    if sizeEl != None:
        size = sizeEl.text
    data['size'] = size
    price_parent_el = content.find('.b-item-price', first=True)
    price_el = price_parent_el.find('.visuallyhidden', first=True)
    for i in price_el.element.iterchildren():
        attrs = dict(**i.attrib)
        try:
            #del attrs['itemprop']
            pass
        except:
            pass
        attrs_keys = list(attrs.keys())
        data[i.attrib['itemprop']] = i.attrib[attrs_keys[0]]
    return data

if __name__ == "__main__":
    url = 'https://www.spoonflower.com/en/fabric/6444170-catching-fireflies-by-thestorysmith'

    html_str = scraper(url)
    content = HTML(html=html_str)
    print(get_product_data(url, content))