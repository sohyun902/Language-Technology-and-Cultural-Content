import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

# 네이버 API로 블로그 검색
def search_naver_blogs(client_id, client_secret, query, display=100):
    encoded_query = urllib.parse.quote(query + " 리뷰")
    url = "https://openapi.naver.com/v1/search/blog?query=" + encoded_query + '&display=' + str(display)

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    

    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read().decode("utf-8")
        return parse_blog_links(response_body)
    else:
        print("Error Code:" + rescode)
        return []

# 링크 추출
def parse_blog_links(response_body):
    body=response_body.replace('"', '')

    List=body.split("\n\t\t{\n\t\t\t")
    LIST=[]
    for i in List:
        if 'naver' in i:
            LIST.append(i)

    links=[]
    for i in LIST:
        letter=i.split("\n\t\t\t")
        for j in letter:
            if "link:" in j and "blogger" not in j:
                j.strip()
                j=j.replace("\\", "")
                links.append(j[5:])
    return links

# 블로그 본문 크롤링
def extract_blog_content(blog_urls):
    true_links=[]
    for link in blog_urls:
        blog_url=link
        blog=urllib.request.urlopen(blog_url)
        soup=BeautifulSoup(blog.read(), "html.parser")
        true_link="http://blog.naver.com/"+soup.iframe["src"]
        true_links.append(true_link)

    contents = []
    for url in true_links:
        try:
            blog = urllib.request.urlopen(url)
            soup = BeautifulSoup(blog.read(), "html.parser")

            content_container = soup.find("div", {"class": "se-main-container"})
            if content_container is None:
                content_container = soup.find("div", {"id": "content-area"})

            if content_container is not None:
                contents.append(content_container.text)
            else:
                print(f"Could not find content for {url}")
                contents.append("")

        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            contents.append("")
    return contents