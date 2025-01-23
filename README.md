目前本项目包含“Download detailed statistical data from Choice Terminal”和“Extract certain keywords from PDF documents online”两个子项目。

在使用Choice终端收集数据时，某些情况下会出现目标数据不存在批量导出的选项。
“Download detailed statistical data from Choice Terminal”的脚本通过模拟鼠标点击指定位置与模拟键盘输入的方式代替人力搜索并下载表格。
然后通过调用tablib对所需大量xlsx文件中的信息进行整合。

“Extract certain keywords from PDF documents online”的脚本（Lets crawl!.py）通过调用pdfplumber和request按照给定xlsx文件中的链接列读取在线pdf文件，
再使用re正则表达式对查找内容进行匹配，一般适用于存在固定格式的公告文件，最后调用tablib创建表格存取所需信息并输出至新创建的xlsx文件中。
在Choice内搜索公告时，可事先通过高级搜索排除无关公告，例如：搜索可转债下修公告时检索含“修”的标题，不包含“修订”、“修复”、“修改”、修文”。
