import re

# 正则表达式
pattern = r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)' 

# 测试字符串
test_dates = [
    "二〇二四年十一月一日",
    "二零二四年十二月三十日",
    "二零二三年一月一日",
    "二零二三年十月五日",
    "三千二百年一月一日",
    "一九八四年七月四日",
    "1231年1月12日",
    "2013年3月2日",
    "1938年4月4日",
    "二〇二四年二月二十日"
]

# 验证
for date in test_dates:
    if re.findall(r'([一二三四五六七八九十〇零]+年[一二三四五六七八九十〇]+月[一二三四五六七八九十〇]+日)',date) or re.findall(pattern, date):
        print(f"匹配: {date}")
    else:
        print(f"不匹配: {date}")
