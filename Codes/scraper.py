import httpx
from selectolax.parser import HTMLParser
import pandas as pd
import time
from dataclasses import dataclass
import csv
import string

# @dataclass
# class Item:
#     word: str
#     meanings: str

def get_html(baseurl, page):

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    resp = httpx.get(baseurl + page, headers=headers) #follow_redirects=True)
    try:
        resp.raise_for_status()
    except httpx.HTTPSTATUSError as exc:
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

    for word in words:
        item = {
        extract_text(word, "span.stl3") : extract_text(word, "span.format1")
        }
    print(item)
    return item



    # X = extract_text(word, "span.nextword")
    # #next = X.replace("পরবর্তী শব্দ : ","")
    # print(next)
    # return next
    # #yield next
      

def main():
    #listPage = []
    #df = pd.read_csv("file_5.csv")
    #df = df["words"]
    data = pd.DataFrame()
    df = ["অংশাংশি", "আঁশ", "আঁইশ, অকর্ণ"]
    diction = {}
    for word in df:
        #print(f"Gathering this word {words}")
        #listPage.append(words)
        print(f"Print word Before {word}")
        word = str(word)
        #if ',' in word:
        print("Entering here")
        #str = "/%2c/%20"
        strings = "XXX"
        word.replace(", ", strings )
        print(f"NEW word {word}")
        
        baseurl = "https://www.english-bangla.com/bntobn/index/"
        x = baseurl + word
        print(f"HTML LINK {x}")
        html = get_html(baseurl, word)
        #data= parse_page(html)
        data = parse_page(html)
        #print(f"HERE IS WJAT IS COMING {data}")
        #data["word"]

        diction.update(data)
        
        print(f"Updating : {diction}")

        time.sleep(2)
    print(f"Here is the final data----------------- {diction}")
    #df = pandas.DataFrame(data={"words": words_all})
    # with open('Ben2Ben.csv','w') as f:
    #     w = csv.writer(f, delimiter=';')
    #     w.writerows(diction.items())
    # #diction.to_csv("./wordsssss.csv", sep=',',index=False)

if __name__ == "__main__":
    main()

