# Dependencies list
#pip install requests_html pandas selenium
#pip install webdriver-manager

import re
from requests_html import HTML
import pandas as pd

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def scraper(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    return driver.page_source


# /en/fabric/7137786-genevieve-floral-by-crystal_walen
def extract_id_slug(url_path):
    regex = r"^[^\s]+/(?P<id>\d+)-(?P<slug>[\w_-]+)$"
    group = re.match(regex, url_path)
    if not group:
        return None, None
    return group['id'], group['slug']


if __name__ == "__main__":
    url = 'https://www.spoonflower.com/en/shop?on=fabric'
    content = scraper(url)
    html_r = HTML(html=content)

    fabric_links = [x for x in list(html_r.links) if x.startswith("/en/fabric")]

    datas = []
    for path in fabric_links:
        id_, slug_ = extract_id_slug(path)
        print(id_, slug_)
        data = {
            "id": id_,
            "slug": slug_,
            "path": path,
            "scraped": 0 # True / False -> 1 / 0 
        }
        datas.append(data)
    df = pd.DataFrame(datas)
    df.head()
    df.to_csv("local.csv", index=False)