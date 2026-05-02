import requests
from bs4 import BeautifulSoup

# 1. 定义要爬取的网址
url = "http://quotes.toscrape.com"

try:
    # 2. 发送请求获取网页内容
    # 加入 Headers 模拟浏览器，避免被网站简单识别为爬虫
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    # 检查请求是否成功 (状态码 200)
    if response.status_code == 200:
        # 3. 使用 BeautifulSoup 解析网页 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 4. 提取数据
        # 在这个网站中，每条名言都在 <div class="quote"> 标签里
        quotes = soup.find_all('div', class_='quote')
        
        # --- 确保下面这一块代码的所有行前面都有同样多的空格/Tab ---
        print(f"--- 成功获取来自 {url} 的名言 ---\n")

        # --- 在这里加入打印数量的代码 ---
        print(f"--- 成功连接网站：{url} ---")
        print(f"--- 本次共抓取到 {len(quotes)} 条名言 ---\n")
        
        for i, quote in enumerate(quotes, 1):
            text = quote.find('span', class_='text').get_text()
            author = quote.find('small', class_='author').get_text()
            print(f"{i}. \"{text}\"")
            print(f"   —— 作者: {author}\n")
    else:
        print(f"请求失败，状态码: {response.status_code}")

except Exception as e:
    print(f"发生错误: {e}")
