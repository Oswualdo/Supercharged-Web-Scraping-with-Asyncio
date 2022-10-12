import os
import asyncio
from arsenic import get_session, keys, browsers, services
import pandas as pd
from requests_html import HTML
import re
import pathlib

import logging
import structlog # pip install structlog

path = os.getcwd()

def set_arsenic_log_level(level = logging.WARNING):
    # Create logger
    logger = logging.getLogger('arsenic')

    # We need factory, to return application-wide logger
    def logger_factory():
        return logger

    structlog.configure(logger_factory=logger_factory)
    logger.setLevel(level)


# /en/fabric/7137786-genevieve-floral-by-crystal_walen
async def extract_id_slug(url_path):
    regex = r"^[^\s]+/(?P<id>\d+)-(?P<slug>[\w_-]+)$"
    group = re.match(regex, url_path)
    if not group:
        return None, None
    return group['id'], group['slug']



async def get_links(body_content):
    html_r = HTML(html=body_content)
    fabric_links = [x for x in list(html_r.links) if x.startswith("/en/fabric")]
    datas = []
    for path in fabric_links:
        id_, slug_ = await extract_id_slug(path)
        data = {
            "id": id_,
            "slug": slug_,
            "path": path,
            "scraped": 0 # True / False -> 1 / 0 
        }
        datas.append(data)
    return datas

async def scraper(url):
    service = services.Chromedriver(binary=path+"/chromedriver")
    browser = browsers.Chrome()
    #browser = browsers.Chrome(chromeOptions={
    #    'args': ['--headless', '--disable-gpu']
    #})
    async with get_session(service, browser) as session:
        await session.get(url)
        body = await session.get_page_source()
        # print(body)
        return body


def store_links_as_df_pickle(datas=[], name='links.pkl'):
    new_df = pd.DataFrame(datas)
    og_df = pd.DataFrame([{'id': 0}])
    if pathlib.Path(name).exists():
        og_df = pd.read_pickle(name) # read_csv
    df = pd.concat([og_df, new_df])
    df.reset_index(inplace=True, drop=False)
    df = df[['id', 'slug', 'path', 'scraped']]
    df = df.loc[~df.id.duplicated(keep='first')]
    # df.set_index('id', inplace=True, drop=True)
    df.dropna(inplace=True)
    df.to_pickle(name)
    return df
    
    
async def run(url):
    body_content = await scraper(url)
    links = await get_links(body_content)
    return links
    
if __name__ == "__main__":
    set_arsenic_log_level()
    url = 'https://www.spoonflower.com/en/shop?on=fabric'
    name = "link.pkl"
    results = asyncio.run(run(url))
    df = store_links_as_df_pickle(results, name=name)
    print(df.head())