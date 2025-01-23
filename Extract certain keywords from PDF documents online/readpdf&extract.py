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

            # 使用正则表达式提取姓名、邮箱地址和电话号码
            name_match = re.search(r'姓名：(.+)', text)
            email_match = re.search(r'邮箱：(.+)', text)
            phone_match = re.search(r'电话：(.+)', text)

            if name_match and email_match and phone_match:
                name = name_match.group(1)
                email = email_match.group(1)
                phone = phone_match.group(1)

                # 将提取的信息添加到列表中
                extracted_data.append({'姓名': name, '邮箱': email, '电话': phone})

    return extracted_data

# 指定PDF文件路径
pdf_file_path = 'D:/12.pdf'

# 提取信息并打印
result = extract_information_from_pdf(pdf_file_path)
for entry in result:
    print(entry)
