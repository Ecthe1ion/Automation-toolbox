import requests
import pdfplumber
from io import BytesIO

...
url = "https://pdf.dfcfw.com/pdf/H2_AN202411041640705965_1.pdf"

with pdfplumber.open(BytesIO(requests.get(url).content)) as pdf:

    total_pages = len(pdf.pages)

    # 遍历每一页
    for page_number in range(total_pages):
        # 获取当前页
        page = pdf.pages[page_number]

        # 提取文本内容
        text = page.extract_text()

        # 打印文本内容
        print(f"Page {page_number + 1}:\n{text}")
