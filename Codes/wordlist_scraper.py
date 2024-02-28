import httpx
from selectolax.parser import HTMLParser
import time
import pandas

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
        return X.replace('\u200c', '')
        print("Inside Extract Text")
    except AttributeError:
        return None
    
def parse_page(html):
    words = html.css('div#cat_page ul li')    

    wordlist = []

    for word in words:
        # item = {
        # #"word" : extract_text(word, "div#cat_page"),
        # #"meanings" : extract_text(word, "span.format1")
        # }
        item = extract_text(word, "li")
        wordlist.append(item)
        #print(words)

    # X = extract_text(word, "span.nextword")
    # #next = X.replace("পরবর্তী শব্দ : ","")
    # print(next)
    # return next
    # #yield next
    return wordlist
      

def main():
    
    baseurl = "https://www.english-bangla.com/browse/bntobn/"
    letters = [ "অ", "আ", "ই", 
               "ঈ", "উ", "ঊ", "ঋ", "এ", "ঐ", "ও", "ঔ", "ক", "খ", "গ", "ঘ", 
               #"ঙ",
               "চ", "ছ", "জ", "ঝ", #"ঞ",
               "ট", "ঠ", "ড", "ঢ", "ণ", "ত", "থ", "দ", "ধ", "ন", "প", "ফ", "ব", "ভ", "ম", "য", "র", "ল", "শ", "ষ", "স", "হ", "ক্ষ",
               #"ড়", "ঢ়", "য়"
                    ]
    words_all = []
    letter_all = []
    for letter in letters:
        print(f"Gathering page: {letter}")
        html = get_html(baseurl, letter)
        
        if html is False:
            break
        #data= parse_page(html)
        
        data = parse_page(html)
        #print(f"Printing data {data}")
        #letter_all.append(letter)
        for dat in data:
            words_all.append(dat)
        print(f"Printing words all {words_all}")
        time.sleep(2)
    df = pandas.DataFrame(data={"words": words_all})
    df.to_csv("./file_5.csv", sep=',',index=False)
if __name__ == "__main__":
    main()

