from bs4 import BeautifulSoup
from .utils import get_soup


def parse_page(url):
    if '/article/' in url:
        return parse_article(url)
    if '/publication/' in url:
        return parse_publication(url)
    if '/blog-post/' in url:
        return parse_blog_post(url)
    return None

def parse_publication(url):
    def parse_title(soup):
        h1 = soup.select('h1[class=hero__title]')
        if not h1:
            return ''
        return h1[0].text.strip()

    def parse_date(soup):
        try:
            for li in soup.select('ul[class=hero__info] li'):
                if 'hero__info-item--date' in li.attrs.get('class', ''):
                    return li.text.strip()
            return ''
        except Exception as e:
            return ''

    def parse_publication_link(soup):
        for a in soup.select('a'):
            if 'https://www.wilsoncenter.org/sites/default/files/' in a.attrs.get('href', ''):
                return a.attrs['href']
        return ''

    soup = get_soup(url)
    content_url = parse_publication_link(soup)
    return {
        'url': url,
        'title': parse_title(soup),
        'date': parse_date(soup),
        'content': content_url
    }

def parse_article(url):
    def parse_author(soup):
        names = []
        for a in soup.select('a'):
            if '/person/' in a.attrs.get('href', ''):
                names.append(a.text.strip())
        if names:
            return ', '.join(names)
        return ''

    def parse_title(soup):
        h1 = soup.select('h1[class=hero__title]')
        if not h1:
            return ''
        return h1[0].text.strip()

    def parse_date(soup):
        try:
            for li in soup.select('ul[class=hero__info] li'):
                if 'hero__info-item--date' in li.attrs.get('class', ''):
                    return li.text.strip()
            return ''
        except Exception as e:
            return ''

    def parse_content(soup):
        phrases = [p.text for p in soup.select('div[class=article-body__inner] p')]
        if not phrases:
            return ''
        return '\n'.join(phrases)

    soup = get_soup(url)
    return {
        'url': url,
        'title': parse_title(soup),
        'date': parse_date(soup),
        'author': parse_author(soup),
        'content': parse_content(soup)
    }

def parse_blog_post(url):
    def parse_author(soup):
        authors = [a.text.strip() for a in soup.select('a') if '/person/' in a.attrs.get('href', '')]
        authors = '' if not authors else ', '.join(authors)
        return authors

    def parse_title(soup):
        h1 = soup.select('h1[class^=article-title]')
        if not h1:
            return ''
        return h1[0].text.strip()

    def parse_date(soup):
        span = soup.select('span[class=blog-post-meta__date__text]')
        if not span:
            return ''
        return span[0].text.strip()

    def parse_content(soup):
        p = soup.select('div[class^=field-item] p')
        if not p:
            return ''
        return '\n'.join(pi.text.strip() for pi in p)

    soup = get_soup(url)
    return {
        'url': url,
        'title': parse_title(soup),
        'date': parse_date(soup),
        'author': parse_author(soup),
        'content': parse_content(soup)
    }

url_base = 'https://www.wilsoncenter.org{}'

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