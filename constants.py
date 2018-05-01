def get_homepage(file_path):
    homepage = None
    with open(file_path) as file:
        homepage = file.read()
    return homepage


def get_affiliate_domains(file_path):
    aff_domains = set({})
    with open(file_path) as file:
        for line in file:
            aff_domains.add(line.strip())
    return aff_domains


def get_domain(homepage):
    if homepage[-1] == '/':
        homepage = homepage[:-1]
    domain = homepage.split('://')[1]
    if domain[:4] == 'www.':
        domain = domain[4:]
    return domain


HEADERS = {'user-agent': ('Mozilla/5.0 (Linux; Android 6.0; '
           'Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/66.0.3359.139 Mobile Safari/537.36')}
HOMEPAGE = get_homepage('info/homepage.txt')
DOMAIN = get_domain(HOMEPAGE)
AFFILIATE_DOMAINS = get_affiliate_domains('info/aff_domains.txt')
DB_URI = 'sqlite:///urls.db'
