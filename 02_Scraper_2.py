import httpx
from selectolax.parser import HTMLParser
import pandas as pd
import time
from dataclasses import dataclass
import csv

# @dataclass
# class Item:
#     word: str
#     meanings: str

def get_html(baseurl, page):

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    resp = httpx.get(baseurl + page, headers=headers, follow_redirects=True)
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error Response {exc.response.status_code}while requesting {exc.request.url!r}. Page Limit exceeded")
        return False    
    html = HTMLParser(resp.text)
    print(resp.status_code)
    return html

def extract_text(html, selector):
    try:
        X = html.css_first(selector).text()
        return X.replace('\xa0', ' ')
        print("Inside Extract Text")
    except AttributeError:
        return None
    
def parse_page(html):
    words = html.css('div.w_info')    

    item = {}
    for word in words:
        item = {
        extract_text(word, "span.stl3") : extract_text(word, "span.format1")
        }
    print(item)
    return item      

def main():
    df = pd.read_csv("wordList_with_symbols.csv")
    #df = pd.read_csv("file_5(copy)_temp.csv")
    df = df["words"]
    print(f"Here is all the word list: { df}")
    data = pd.DataFrame()
    diction = {}
    for word in df:
        baseurl = "https://www.english-bangla.com/bntobn/index/"
        # if word.contains(", "):
        #     word.replace(", ", "%2c%20" )
        html = get_html(baseurl, word)  

        if html == False:
            continue
        data = parse_page(html)
        

        diction.update(data)
        
        print(f"Updating : {diction}")

        time.sleep(2)
    print(f"Here is the final data----------------- {diction}")
    with open('Ben2Ben2.csv','w') as f:
        w = csv.writer(f, delimiter='|')
        w.writerows(diction.items())

if __name__ == "__main__":
    main()

