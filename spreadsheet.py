from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from constants import DB_URI, AFFILIATE_DOMAINS
from models import Base, Inbound, Outbound, Affiliate


class SpreadsheetMaker():
    def __init__(self):
        engine = create_engine(DB_URI)
        Base.metadata.bind = engine
        self.db = sessionmaker(bind=engine)()
        self.main_reports()
        self.affiliate_reports()


    def affiliate_reports(self):
        for domain in AFFILIATE_DOMAINS:
            file_path = 'reports/affiliates/{}csv'.format(domain)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write('STATUS,DOMAIN,URL,PARENTS,REDIRECT\n')
                query = self.db.query(Affiliate).filter(
                        Affiliate.url.contains(domain))
                for entry in query:
                    self.write_entry(file, entry, Affiliate)


    def main_reports(self):
        for model in [Inbound, Outbound, Affiliate]:
            file_path = 'reports/{}.csv'.format(model.__tablename__)
            self.write_table(model, file_path)


    def write_table(self, model, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('STATUS,DOMAIN,URL,PARENTS,REDIRECT\n')
            query = self.db.query(model).order_by(
                    model.status.desc(), model.url)
            for entry in query:
                self.write_entry(file, entry, model)


    def write_entry(self, file, entry, model):
        def esc(string):
            if string:
                return string.replace('\"', '\"\"').replace('\n', '\\n')
            return None

        parents = entry.parents.split(' ; ')
        data = '\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"\n'.format(
                entry.status, model.__tablename__, esc(entry.url),
                esc(parents[0]), esc(entry.redirect))
        if len(parents) > 1:
            for index in range(1, len(parents)-1):
                data += ',,,\"{}\"\n'.format(esc(parents[index]))
        file.write(data)




SpreadsheetMaker()
