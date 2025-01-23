import pdfplumber
import re

def extract_information_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)

        # 创建一个空的列表用于存储信息
        extracted_data = []

        for page_number in range(total_pages):
            page = pdf.pages[page_number]

            # 提取文本内容
            text = page.extract_text()

            if page_number == 0:
                indicator = re.search(r'不向下', text)
            
            if indicator:
                # 使用正则表达式提取姓名、邮箱地址和电话号码
                CD_match = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*重新起算)', text)
                if CD_match:
                    CD = CD_match.group(1)
                    # 使用正则表达式去除所有空格
                    CD = re.sub(r'\s+', '', CD)  # 替换所有空格为无
                    # 将提取的信息添加到列表中
                    extracted_data.append({ '重启日期': CD})
            
            if page_number+1 == total_pages:
                announcement_date_match = re.findall(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)', text, re.MULTILINE)
                if announcement_date_match:
                    announcement_date = announcement_date_match[-1]
                    announcement_date = re.sub(r'\s+', '', announcement_date)
                extracted_data.append({ '落款日期': announcement_date})

    return extracted_data

# 指定PDF文件路径
pdf_file_path = 'D:/1.pdf'

# 提取信息并打印
result = extract_information_from_pdf(pdf_file_path)
for entry in result:
    print(entry)
