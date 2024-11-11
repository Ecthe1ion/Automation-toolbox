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
                if re.search(r'不向下', text):            
                    extracted_data.append({ '公告类型': str('不向下修正')})
                    # 使用正则表达式提取日期
                    CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*重新起算)', text).group(1)
                    # 使用正则表达式去除所有空格
                    CD = re.sub(r'\s+', '', CD)  # 替换所有空格为无
                    # 将提取的信息添加到列表中
                    extracted_data.append({ '重启日期': CD})
                elif re.search(r'预计', text):
                    extracted_data.append({ '公告类型': str('预计向下修正')})
                elif re.search(r'提议', text):
                    extracted_data.append({ '公告类型': str('提议向下修正')})
                #elif re.search(r'', text):
                    #extracted_data.append({ '公告类型': str('向下修正')})
                else:
                    extracted_data.append({ '公告类型': str('未知')})

            if page_number+1 == total_pages:
                if re.findall(r'([一二三四五六七八九十〇零]+年[一二三四五六七八九十〇]+月[一二三四五六七八九十〇]+日)', \
                text,re.MULTILINE):
                    announcement_date_match = re.findall(r'([一二三四五六七八九十〇零]+年[一二三四五六七八九十〇]+月[一二三四五六七八九十〇]+日)', \
                    text,re.MULTILINE)
                elif re.findall( r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)', text, re.MULTILINE):
                    announcement_date_match = re.findall( r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)', text, re.MULTILINE)
                else:
                    break

                announcement_date = announcement_date_match[-1]
                announcement_date = re.sub(r'\s+', '', announcement_date)
                extracted_data.append({ '落款日期': announcement_date})

    return extracted_data

# 指定PDF文件路径
pdf_file_path = 'D:/3.pdf'

# 提取信息并打印
result = extract_information_from_pdf(pdf_file_path)
for entry in result:
    print(entry)