from selenium import webdriver
from selenium.webdriver.common.by import By


print("正在启动 Chrome 浏览器...")
driver = webdriver.Chrome()

print("正在访问网页...")
driver.get("https://data.eastmoney.com/xg/xg/default.html")

print("访问成功！浏览器标题是：", driver.title)

# Get the HTML page source
html_source = driver.page_source

# 假设 driver 是你的 Selenium 实例
rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-index]")

for row in rows:
    # 使用相对路径寻找每一行里的代码和名称
    # 代码通常在第一个 a 标签，名称在第二个 a 标签
    links = row.find_elements(By.TAG_NAME, "a")
    if len(links) >= 2:
        code = links[0].text
        name = links[1].text
        print(f"代码: {code}, 名称: {name}")

# 保持窗口 5 秒后关闭
import time
time.sleep(5)
driver.quit()
