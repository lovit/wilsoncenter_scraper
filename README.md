# Wilson Center parser

blog-post, article, publication 의 웹페이지를 파싱하는 코드입니다. 웹페이지의 링크가 포함되어 있는 html 파일을 input 으로 입력하면, blog-post, article, publication 의 종류에 따라 각각 다른 parser 를 통하여 정보를 수집합니다. publication 의 출간 자료는 download 함수를 이용하여 다운로드 됩니다.

```
python extract_urls_and_get_page.py --input_file data/html_sample.html --directory ./output/ --sleep 5 --debug
```