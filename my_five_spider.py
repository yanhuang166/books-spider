# 全量版，爬取50页书本详情页
import requests
import csv
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

# 前置，
url = 'https://books.toscrape.com/'
page_url = url # 翻页初始化
book = [] # 临时存放
# page_num = 0 # 先爬一页验收
# 请求，解析，防护，
while page_url:
    page_response = requests.get(page_url,timeout=10)
    page_response.raise_for_status()
    page_response.encoding = page_response.apparent_encoding
    soup = BeautifulSoup(page_response.text, 'html.parser')
    page_all_book=soup.find_all('article',class_="product_pod")

    for one_book in page_all_book: # 遍历取单本地址
        one_book_id_name= one_book.find('h3').find('a')['href']
        one_book_id = urljoin(page_url,one_book_id_name)

        response = requests.get(one_book_id,timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup_on_book = BeautifulSoup(response.text, 'html.parser')

        soup_name=soup_on_book.find('h1').text # name
        soup_p = soup_on_book.find('p',class_="price_color").text.replace('£','') # price
        soup_s = soup_on_book.find('p',class_="instock availability").text.strip() # stock
        soup_star = soup_on_book.find('p',class_="star-rating") # star
        if soup_star:
            soup_star_s=soup_star['class'][1]
        else:
            soup_star_s = None

        soup_pd = soup_on_book.find('div',id="product_description")# 为什么不复制class唯独留下id属性？
        soup_j = '无简介'
        if soup_pd:
            p=soup_pd.find_next_sibling('p')
            if p:
                soup_j=p.text # 有简介则覆盖p变量
        book.append((soup_name,soup_p,soup_s,soup_star_s,soup_j))
        time.sleep(1)
    # page_num+=1
    # if page_num==1:
    #     break # 先爬一页验收

    # 翻页
    page_tf=soup.find('li',class_="next")
    if page_tf:
        print(f'正在加载页面{page_tf}中...🤪')
        page_url = urljoin(page_url,page_tf.find('a')['href'])
        time.sleep(1) # 礼貌
    else:
        break # 最后一页就结束
with open('整站书1000.csv','w',newline='',encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['书名','价格','库存','星标数','简介'])
    writer.writerows(book)







