import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 初始化存放数据的列表
results = []

print("正在启动 Chrome 浏览器...")
driver = webdriver.Chrome()

try:
    print("正在访问网页...")
    driver.get("https://data.eastmoney.com/xg/xg/default.html")
    
    current_page = 1
    total_pages = 79 # 目标页数

    while current_page <= total_pages:
        print(f"--- 正在爬取第 {current_page} 页 ---")
        
        # 1. 等待表格加载
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr[data-index]"))
        )
        
        # 2. 抓取当前页数据
        rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-index]")
        for row in rows:
            try:
                links = row.find_elements(By.TAG_NAME, "a")
                if len(links) >= 2:
                    code = links[0].text.strip()
                    name = links[1].text.strip()
                    if code and name:
                        results.append({"股票代码": code, "公司简称": name})
            except Exception:
                continue # 忽略单行抓取错误

        # 3. 翻页操作
        if current_page < total_pages:
            try:
                # 定位“下一页”按钮
                next_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "下一页"))
                )
                # 滚动并点击
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
                time.sleep(0.5) 
                next_btn.click()
                
                current_page += 1
                # 给页面一点点加载新数据的时间
                time.sleep(1.5) 
            except Exception as e:
                print(f"翻页中途中断: {e}")
                break
        else:
            break

    # --- 核心添加部分：保存数据 ---
    print(f"\n爬取完毕！共获取 {len(results)} 条数据。")
    
    # 转换为 Pandas 数据框
    df = pd.DataFrame(results)
    
    # 保存为 Excel (需安装 openpyxl: pip install openpyxl)
    df.to_excel("新股列表.xlsx", index=False)
    # 或者保存为 CSV
    # df.to_csv("新股列表.csv", index=False, encoding='utf_8_sig')
    
    print("数据已成功保存至：新股列表.xlsx")

finally:
    driver.quit()