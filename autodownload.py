from pyautogui import *

FAILSAFE

data = """
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
mylist = [line.strip() for line in data.strip().split('\n')]

# 任务栏打开软件（最好添加sleep函数手动打开）
click(1149,1417)

for ticker in mylist:
    # 搜索（注意输入法改英文以防止输入错误）
    click(86,101)
    click(1524,172)
    typewrite(ticker)
    press('enter')

    # 打开深度资料&打开最廉走势
    sleep(1.5)
    click(1394,439)
    sleep(2)
    click(94,611)

    # 修改日期区间
    sleep(1.5)
    click(443,209)
    sleep(1.5)
    click(406,273,5)
    click(404,409)
    sleep(1)
    click(1117,203)
    click(1065,320)
    click(1065,360)
    click(1065,400)

    # 下载文件
    sleep(0.7)
    click(2060,202)
    click(1325,815)
    sleep(0.7)

    # 关闭第二个窗口
    click(426,103,2,0.3)
