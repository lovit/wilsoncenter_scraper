from bs4 import BeautifulSoup
from .utils import get_soup


def parse_title(soup):
    try:
        soup.select('h1[class=hero__title]')[0].text.strip()
    except Exception as e:
        return ''

def parse_date(soup):
    try:
        for li in soup.select('ul[class=hero__info] li'):
            if 'hero__info-item--date' in li.attrs.get('class', ''):
                return li.text.strip()
        return ''
    except Exception as e:
        return ''

def parse_author(soup):
    try:
        names = []
        for a in soup.select('ul[class=hero__info] a'):
            if '/person/' in a.attrs.get('href', ''):
                names.append(a.text.strip())
        if names:
            return ', '.join(names)
        return ''
    except Exception as e:
        return ''

def parse_content(soup):
    phrases = [p.text for p in soup.select('div[class=article-body__inner] p')]
    if not phrases:
        return ''
    return '\n'.join(phrases)

def parse_page(url):
    soup = get_soup(url)
    return {
        'url': url,
        'title': parse_title(soup),
        'date': parse_date(soup),
        'author': parse_author(soup),
        'content': parse_content(soup)
    }

url_base = 'https://www.wilsoncenter.org/{}'

def get_links_from_html(html_path):
    """
    Arguments
    ---------
    html_path : str
        HTML file path (local or remote)

    Returns
    -------
    urls : list of str
        URLs of articles, blog-posts, and publications
    """

    with open(html_path, encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'lxml')
    links = soup.select('div[class^=wc-masonry-grid__item] a')
    hrefs = [parse_href(link) for link in links]
    hrefs = {href for href in hrefs if href is not None}
    urls = [url_base.format(href) for href in hrefs]
    return urls

def parse_href(link):
    if not hasattr(link, 'attrs'):
        return None
    href = link.attrs.get('href', '')
    if href.find('/blog-post/') == 0:
        return href
    if href.find('/publication/') == 0:
        return href
    if href.find('/article/') == 0:
        return href
    return None