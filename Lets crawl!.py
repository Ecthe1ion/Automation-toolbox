import pdfplumber
import re
import requests
from io import BytesIO
import tablib


def convert_chinese_date(chinese_date):
    # 汉字数字与对应的阿拉伯数字的映射
    chinese_to_digit = {
        '零': '0', '一': '1', '二': '2', '三': '3', '四': '4',
        '五': '5', '六': '6', '七': '7', '八': '8', '九': '9',
        '十': '1', '〇':'0'
    }

    # 提取年份、月份和日期
    year_part = chinese_date.split('年')[0]
    month_part = chinese_date.split('年')[1].split('月')[0]
    day_part = chinese_date.split('月')[1].split('日')[0]

    # 转换年份
    year = ''
    for char in year_part:
        year += chinese_to_digit[char]

    # 转换月份
    month = ''
    for char in month_part:
        if char in chinese_to_digit:
            month += chinese_to_digit[char]

    # 转换日期
    day = ''
    for char in day_part:
        if char in chinese_to_digit:
            day += chinese_to_digit[char]

    return f"{year}年{month}月{day}日"

def extract_information_from_pdf(pdf_path):
    with pdfplumber.open(BytesIO(requests.get(pdf_path).content)) as pdf:
        total_pages = len(pdf.pages)

        # 创建一个空的列表用于存储信息
        extracted_data = []

        retry_indicator = 0

        for page_number in range(total_pages):
            page = pdf.pages[page_number]

            # 提取文本内容
            text = page.extract_text()

            if page_number == 0:
                try:
                    underlying_security = re.search(r'证券简称[：:]\s*([\*ST\s]*[\u4e00-\u9fa5]{1,4})\s', text).group(1)
                except:
                    if re.search(r'股票简称[：:]\s*([\*ST\s]*[\u4e00-\u9fa5]{1,4})\s', text):
                        underlying_security = re.search(r'股票简称[：:]\s*([\*ST\s]*[\u4e00-\u9fa5]{1,4})\s', text).group(1)
                    else:
                        underlying_security = re.search(r'公司简称[：:]\s*([\*ST\s]*[\u4e00-\u9fa5]{1,4})\s', text).group(1)
                underlying_security = re.sub(r'\s+', '', underlying_security)
                extracted_data.append({ '证券简称': underlying_security})
                if re.search(r'预计', text):
                    extracted_data.append({ '公告类型': str('预计向下修正')})
                    extracted_data.append({ '重启日期': None})
                elif re.search(r'不向下', text):            
                    extracted_data.append({ '公告类型': str('不向下修正')})
                    # 使用正则表达式提取日期
                    try:
                        CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*[）起]*[（如遇法定节假日或休息日延至其后的第 1 个交易日）]*重新[起计]*算)', text).group(1)
                    except:
                        if re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*开始重新起算)', text):
                            CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*开始重新起算)', text).group(1)
                        elif re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*起首个交易日重新开始计算)', text):
                            CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*起首个交易日重新开始计算)', text).group(1)
                        elif re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*起计算)', text):
                            CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*起计算)', text).group(1)
                        elif re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*[为首日开始重新计算之后\s起首个交易日]*，若再次触发)', text):
                            CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*[为首日开始重新计算之后\s起首个交易日]*，若再次触发)', text).group(1)
                        else:
                            retry_indicator = 1
                    if retry_indicator == 0:
                        # 使用正则表达式去除所有空格
                        CD = re.sub(r'\s+', '', CD)  # 替换所有空格为无
                        # 将提取的信息添加到列表中
                        extracted_data.append({ '重启日期': CD})
                elif re.search(r'提议', text):
                    extracted_data.append({ '公告类型': str('提议向下修正')})
                    extracted_data.append({ '重启日期': None})
                elif re.search(r'可能触发', text):
                    extracted_data.append({ '公告类型': str('可能触发提示')})
                    extracted_data.append({ '重启日期': None})
                elif re.search(r'关于向下', text):
                    extracted_data.append({ '公告类型': str('向下修正')})
                    extracted_data.append({ '重启日期': None})
                else:
                    extracted_data.append({ '公告类型': str('未知')})
                    extracted_data.append({ '重启日期': None})

            if page_number+2 == total_pages:
                if retry_indicator == 1:
                    try:
                        CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*[）起]*[（如遇法定节假日或休息日延至其后的第 1 个交易日）]*重新[起计]*算)', text).group(1)
                    except:
                        if re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*开始重新起算)', text):
                            CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*开始重新起算)', text).group(1)
                        elif re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*起首个交易日重新开始计算)', text):
                            CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*起首个交易日重新开始计算)', text).group(1)
                        elif re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*起计算)', text):
                            CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*起计算)', text).group(1)
                        elif re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*[为首日开始重新计算之后\s起首个交易日]*，若再次触发)', text):
                            CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*[为首日开始重新计算之后\s起首个交易日]*，若再次触发)', text).group(1)
                        else:
                            retry_indicator = 2
                if retry_indicator == 1:
                    CD = re.sub(r'\s+', '', CD)
                    extracted_data.append({ '重启日期': CD})

            if page_number+1 == total_pages:

                if retry_indicator == 2:
                    try:
                        CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*[）起]*[（如遇法定节假日或休息日延至其后的第 1 个交易日）]*重新[起计]*算)', text).group(1)
                    except:
                        if re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*开始重新起算)', text):
                            CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*开始重新起算)', text).group(1)
                        elif re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*起首个交易日重新开始计算)', text):
                            CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*起首个交易日重新开始计算)', text).group(1)
                        elif re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*起计算)', text):
                            CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*起计算)', text).group(1)
                        elif re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*[为首日开始重新计算之后\s起首个交易日]*，若再次触发)', text):
                            CD = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)(?=\s*[为首日开始重新计算之后\s起首个交易日]*，若再次触发)', text).group(1)
                        else:
                            CD = str('异常情况，请手动查看')
                    CD = re.sub(r'\s+', '', CD)
                    extracted_data.append({ '重启日期': CD})


                if re.findall(r'([一二三四五六七八九十〇零]+年[一二三四五六七八九十〇]+月[一二三四五六七八九十〇]+日)', \
                text,re.MULTILINE):
                    announcement_date_match = re.findall(r'([一二三四五六七八九十〇零]+年[一二三四五六七八九十〇]+月[一二三四五六七八九十〇]+日)', \
                    text,re.MULTILINE)
                elif re.findall( r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)', text, re.MULTILINE):
                    announcement_date_match = re.findall( r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)', text, re.MULTILINE)
                

                announcement_date = announcement_date_match[-1]
                try:
                    announcement_date = convert_chinese_date(re.sub(r'\s+', '', announcement_date))
                except:
                    announcement_date = re.sub(r'\s+', '', announcement_date)
                extracted_data.append({ '落款日期': announcement_date})
    return extracted_data


# 指定PDF文件路径
data = tablib.Dataset()
with open('D:/0.xlsx', 'rb') as fh:
    data.load(fh, 'xlsx')

del data['公告主题']
del data['发布时间']
updated_data = tablib.Dataset()
updated_data.headers = ['证券简称', '公告类型','重启日期','落款日期']

# # #记得在excel中手动清理多余行（让表格以外的行保持默认状态）
for Hyperlink in data['附件']:
    pdf_file_path = Hyperlink
    result = extract_information_from_pdf(pdf_file_path)
    Row_waits_for_raddition = list()
    for entry in result:
        for key, value in entry.items():
            print(value)
            Row_waits_for_raddition.append(value)
    updated_data.append(Row_waits_for_raddition)

with open('整理结果.xlsx', 'wb') as f:
    f.write(updated_data.export('xlsx'))
