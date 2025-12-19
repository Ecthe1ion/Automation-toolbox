from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("正在启动 Chrome 浏览器...")
driver = webdriver.Chrome()

try:
    print("正在访问网页...")
    driver.get("https://data.eastmoney.com/xg/xg/default.html")
    
    current_page = 1
    total_pages = 5  # 预设的总页数

    while current_page <= total_pages:
        print(f"--- 正在爬取第 {current_page} 页 ---")
        
        # 1. 等待表格行加载完成 (确保 data-index 出现了)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr[data-index]"))
        )
        
        # 2. 获取当前页的所有行
        rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-index]")
        for row in rows:
            links = row.find_elements(By.TAG_NAME, "a")
            if len(links) >= 2:
                code = links[0].text
                name = links[1].text
                # 过滤掉空的或者非目标数据
                if code and name:
                    print(f"代码: {code}, 名称: {name}")

        # 3. 翻页逻辑
        if current_page < total_pages:
            try:
                # 寻找“下一页”按钮（通常文本为 "下一页" 或其对应的 CSS 类）
                # 这里使用 Link Text 定位比较直观
                next_btn = driver.find_element(By.LINK_TEXT, "下一页")
                
                # 滚动到按钮位置，防止被遮挡无法点击
                driver.execute_script("arguments[0].scrollIntoView();", next_btn)
                time.sleep(1) # 稍微停顿，防止点击过快
                
                next_btn.click()
                current_page += 1
                
                # 等待页面更新（重要：等待旧数据消失或新数据加载）
                time.sleep(2) 
            except Exception as e:
                print(f"翻页失败或已到最后一页: {e}")
                break
        else:
            print("所有页面爬取完毕！")
            break

finally:
    print("程序结束，5秒后关闭...")
    time.sleep(5)
    driver.quit()
