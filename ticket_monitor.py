import requests
import smtplib
import time
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

# --- 配置区域 ---
TARGET_URL = "https://www.baidu.cn"
CHECK_INTERVAL = 60  # 每60秒检查一次

# 邮箱配置 (以163邮箱为例)
SMTP_SERVER = "://*****.163.com"
SENDER_EMAIL = "******.163.com"
SENDER_PASS = "163邮箱16位SMTP密码"  # 记得去邮箱设置里拿
RECEIVER_EMAIL = "purple1234.163.com"

def send_notification(msg_text):
    """发送邮件提醒"""
    message = MIMEText(msg_text, "plain", "utf-8")
    message["Subject"] = "【余票预警】赶紧去买票！"
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, 465)
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], message.as_string())
        server.quit()
        print("邮件提醒已发送！")
    except Exception as e:
        print(f"邮件发送失败: {e}")

def monitor():
    print("开始监控票务信息...")
    while True:
        print("正在检查中...")  # <--- 加在这里，记得保持缩进对齐！
        
        try:
            #headers = {'User-Agent': 'Mozilla/5.0...'} # 之前的伪装代码
            #response = requests.get(TARGET_URL, headers=headers)
            # 在代码开头定义这个
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

            # 修改你的请求行
            response = requests.get(TARGET_URL, headers=headers, verify=False, timeout=10) 
            
            # 逻辑：如果网页里出现了“预订”或“立即购票”，且没有“缺货”字样
            if "百度" in response.text and "缺货登记" not in response.text:
                print("有票了！")
                send_notification(f"发现余票！直达链接: {TARGET_URL}")
                break  # 提醒后停止，防止轰炸邮箱
            else:
                print(f"[{time.strftime('%H:%M:%S')}] 还没票，继续等待...")
        
        except Exception as e:
            print(f"监控出错: {e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor()
