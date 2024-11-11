#pip install beautifulsoup4
#pip install pdfplumber

import pdfplumber

# 读取PDF文档
with pdfplumber.open('D:/2.pdf') as pdf:
    # 获取文档的总页数
    total_pages = len(pdf.pages)

    # 遍历每一页
    for page_number in range(total_pages):
        # 获取当前页
        page = pdf.pages[page_number]

        # 提取文本内容
        text = page.extract_text()

        # 打印文本内容
        print(f"Page {page_number + 1}:\n{text}")