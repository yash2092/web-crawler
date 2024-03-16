import bs4, requests, os, sys
from urllib.parse import urljoin

domain = sys.argv[1]

content_list = []

with open(f'recon/{domain}/crawler_output','w') as file:
    pass

session = requests.Session()

def request(url):
    try:
        html = session.get(url, allow_redirects=False, timeout=2, cookies={"security":"low", "PHPSESSID":"8a178d0d1bf35df77b7fad777f273691"})
        return html.content
    except Exception as e:
        print(e)
        return ''

def crawl(url):

    try:
        html = request(url)
        soup = bs4.BeautifulSoup(html,'html.parser')
        for a in soup.find_all('a', href=True):
            link = urljoin(url,a['href'])

            if '#' in link:
                link = link.split('#')[0]

            if link not in content_list and domain in link:
                content_list.append(link)
                print("[+] Found the URL: {}".format(link))
                with open(f'recon/{domain}/crawler_output','a') as file:
                    file.write(link + '\n')
                crawl(link)
    except KeyboardInterrupt:
        exit(0)


with open(f'recon/{domain}/subdomains','r') as file:
    subdomains = file.read().splitlines()
    for subdomain in subdomains:
        url = f"http://{subdomain}"
        crawl(url)