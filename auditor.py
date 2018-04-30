import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
from constants import HEADERS, HOMEPAGE, DOMAIN, AFFILIATE_DOMAINS
from models import Base, Inbound, Outbound, Affiliate


class Auditor():
    def __init__(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        engine = create_engine('sqlite:///urls.db')
        Base.metadata.bind = engine
        self.db = sessionmaker(bind=engine)()
        self.crawl_page(requests.get(HOMEPAGE))


    def get_data(self):
        for webpage in SITEMAP_XML.find_all('loc'):
            webpage = webpage.string


    def is_affiliate(self, url):
        affiliate = False
        for domain in AFFILIATE_DOMAINS:
            if domain in url:
                affiliate = True
        return affiliate


    def strip_slash(self, path):
        if path[-1] == '/':
            path = path[:-1]
        return path


    def handle_inbound(self, url, parent):
        url = self.strip_slash(url)
        path = url.split(DOMAIN)[1]
        if url == HOMEPAGE or not path:
            return
        query = self.db.query(Inbound).filter_by(url=path)
        if not query.count():
            resp = requests.get(url, headers=HEADERS)
            data = {
                'status': resp.status_code,
                'url': path,
                'parents': parent
            }
            self.db.add(Inbound(**data))
            self.db.commit()
            if (resp.status_code == 200
            and 'html' in resp.headers['Content-Type']):
                self.crawl_page(resp)
        else:
            self.add_parent(query.one(), parent)


    def handle_outbound(self, url, parent):
        url = self.strip_slash(url)
        query = self.db.query(Outbound).filter_by(url=url)
        if not query.count():
            resp = requests.get(url, headers=HEADERS)
            data = {
                'status': resp.status_code,
                'url': url,
                'parents': parent
            }
            self.db.add(Outbound(**data))
            if self.is_affiliate(url):
                self.db.add(Affiliate(**data))
            self.db.commit()
        else:
            self.add_parent(query.one(), parent)


    def add_parent(self, entry, parent):
        if parent not in entry.parents.split(' ; '):
            entry.parents += ' ; ' + parent
            self.db.add(entry)
            self.db.commit()


    def crawl_page(self, resp):
        print('Crawling page ' + resp.url, flush=True)
        html = BeautifulSoup(resp.text, 'lxml')
        for anchor in html.find_all('a'):
            href = self.get_full_href_path(anchor)
            if href is None or href[:4] != 'http':
                continue
            path = self.get_inbound_path(resp.url)
            if DOMAIN in href:
                self.handle_inbound(href, path)
            else:
                self.handle_outbound(href, path)


    def get_inbound_path(self, url):
        path = url.split(DOMAIN)[1]
        if path != '/':
            path = self.strip_slash(path)
        return path

    def get_full_href_path(self, anchor):
        href = anchor.get('href', None)
        if not href:
            return None
        elif href[0] == '/':
            href = HOMEPAGE + href
        return href



Auditor()
