# books-spider

用 Python + requests + BeautifulSoup 爬取 books.toscrape.com 全站
1000 本书的完整信息（书名、价格、库存、评分、简介）。

## 技术栈

- Python 3
- requests
- BeautifulSoup4
- csv

## 功能

- 自动翻页爬取全站 50 页
- 进入每本书的详情页提取 5 个字段
- 数据存入 CSV 文件

## 运行

```bash
python my_five_spider.py


