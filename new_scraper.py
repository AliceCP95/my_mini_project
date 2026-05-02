import requests
from bs4 import BeautifulSoup

# 1. 目标：BBC 科技新闻频道
url = "https://bbc.com"

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. 核心变化：寻找新闻标题的标签
        # BBC 的标题通常在 <h3> 标签里，且外部有链接 <a>
        # 我们寻找带特定类名的 <a> 标签
        news_list = soup.find_all('a', class_='sc-2e030643-0') 
        
        print(f"--- BBC 今日科技动态 (共 {len(news_list)} 条) ---\n")
        
        for i, news in enumerate(news_list, 1):
            title = news.get_text() # 获取标题文本
            link = "https://bbc.com" + news['href'] # 获取跳转链接
            
            print(f"{i}. {title}")
            print(f"   链接: {link}\n")
    else:
        print(f"请求失败，状态码: {response.status_code}")

except Exception as e:
    print(f"发生错误: {e}")