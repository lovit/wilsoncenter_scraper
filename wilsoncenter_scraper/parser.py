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

def parse_page(soup):
    return {
        'title': parse_title(soup),
        'date': parse_date(soup),
        'author': parse_author(soup),
        'content': parse_content(soup)
    }