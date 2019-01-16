import argparse
import json
import os
import time
from wilsoncenter_scraper import download
from wilsoncenter_scraper import get_links_from_html
from wilsoncenter_scraper import get_soup
from wilsoncenter_scraper import parse_page


def save(json_obj, directory):    
    url = json_obj['url'].split('/')[-1]
    filepath = '{}/{}.json'.format(directory, url)
    with open(filepath, 'w', encoding='utf-8') as fp:
        json.dump(json_obj, fp, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default='data/html_sample.html', help='Your HTML file')
    parser.add_argument('--directory', type=str, default='./output/', help='Output directory')
    parser.add_argument('--sleep', type=float, default=10, help='Sleep time for each submission (post)')
    parser.add_argument('--debug', dest='debug', action='store_true')

    args = parser.parse_args()
    input_file = args.input_file
    directory = args.directory
    sleep = args.sleep
    debug = args.debug

    # check output directory
    if not os.path.exists(directory):
        os.makedirs(directory)

    # TODO
    urls = get_links_from_html(input_file)
    print('num urls = {}'.format(len(urls)))

    if debug:
        urls = urls[:10]

    n_urls = len(urls)
    for i_url, url in enumerate(urls):
        json_obj = parse_page(url)        
        save(json_obj, directory)
        if '/publication/' in url:
            if json_obj['content']:
                download_path = '{}/{}_{}'.format(directory, url.split('/')[-1], json_obj['content'].split('/')[-1])
                download(json_obj['content'], download_path)
        print('downloaded {} / {}: {}'.format(i_url, n_urls, url))
        time.sleep(sleep)

if __name__ == '__main__':
    main()