import tablib

tickerlist = """
TS2003
TS2006
TS2009
TS2012
TS2103
TS2106
TS2109
TS2112
TS2203
TS2206
TS2209
TS2212
TS2303
TS2306
TS2309
TS2312
TS2403
TS2406
TS2409
TS2412
TS2503
TS2506
TF2003
TF2006
TF2009
TF2012
TF2103
TF2106
TF2109
TF2112
TF2203
TF2206
TF2209
TF2212
TF2303
TF2306
TF2309
TF2312
TF2403
TF2406
TF2409
TF2412
TF2503
TF2506
T2003
T2006
T2009
T2012
T2103
T2106
T2109
T2112
T2203
T2206
T2209
T2212
T2303
T2306
T2309
T2312
T2403
T2406
T2409
T2412
T2503
T2506
TL2306
TL2309
TL2312
TL2403
TL2406
TL2409
TL2412
TL2503
TL2506
"""
mylist = [line.strip() for line in tickerlist.strip().split('\n')]

summary = tablib.Dataset()
summary.headers = ['日期', '代码', '净价(元)', '收益率(%)', 'IRR(%)', '期现价差', '基差']

data = tablib.Dataset()
for ID in mylist:
    with open('D:/国债期货ctd数据/'+ID+'_最廉走势.xlsx', 'rb') as fh:
        data.load(fh, 'xlsx')
        del data[0]
        del data[-6:-1]
        del data[-1]
        try:
            data.headers = ['日期', '代码', '净价(元)', '收益率(%)', 'IRR(%)', '期现价差', '基差', 
                        '次廉代码', '次廉净价(元)', '次廉收益率(%)', '次廉IRR(%)', '次廉期现价差', '次廉基差', 
                        '三廉代码', '三廉净价(元)', '三廉收益率(%)', '三廉IRR(%)', '三廉期现价差', '三廉基差']
            for entry in ['次廉代码', '次廉净价(元)', '次廉收益率(%)', '次廉IRR(%)', '次廉期现价差', '次廉基差', 
                        '三廉代码', '三廉净价(元)', '三廉收益率(%)', '三廉IRR(%)', '三廉期现价差', '三廉基差']:
                del data[entry]

            for row in data.dict:
                if ID[-1] != '3':
                    if (row['日期'] > '20'+ID[-4:-2]+'-'+str(int(ID[-2:])-4)+'-16') \
                    & (row['日期'] < '20'+ID[-4:-2]+'-'+str(int(ID[-2:])-1)+'-15'):
                        summary.append(row.values())
                else:
                    if (row['日期'] > '20'+str(int(ID[-4:-2])-1)+'-11-16') \
                    & (row['日期'] < '20'+ID[-4:-2]+'-02-15'):
                        summary.append(row.values())
        except:
            pass

print(summary)

with open('合并结果.xlsx', 'wb') as f:
    f.write(summary.export('xlsx'))
