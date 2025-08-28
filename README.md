在对金融数据进行处理时，常遇到金融数据软件导出功能不够智能的情况，因此在Automation-toolbox中收录自己写的一些改进效率的程序。目前，本项目共包含“Download detailed statistical data from Choice Terminal”和“Extract certain keywords from PDF documents online”两个子项目。

在使用Choice终端收集数据时，某些情况下会出现目标数据不存在批量导出的选项。“Download detailed statistical data from Choice Terminal”的脚本通过模拟鼠标点击指定位置与模拟键盘输入的方式代替人力搜索并下载表格，然后通过调用tablib对所需大量xlsx文件中的信息进行整合。适用于只能在标的资产的深度资料中下载xlsx导出的数据。

“Extract certain keywords from PDF documents online”的脚本（Lets crawl!.py）通过调用pdfplumber和request按照给定xlsx文件中的链接列读取在线pdf文件，
再使用re正则表达式对查找内容进行匹配，一般适用于存在固定格式的公告文件，最后调用tablib创建表格存取所需信息并输出至新创建的xlsx文件中。
在Choice内搜索公告时，可事先通过高级搜索排除无关公告，例如：搜索可转债下修公告时检索含“修”的标题，不包含“修订”、“修复”、“修改”、“修文”。

---------------------------------------------------------------------------------

 When processing financial data, it is common to encounter situations in which the export functions of financial data software are not very intelligent. Therefore, I have included some self-written programs in the Automation Toolbox to improve efficiency. Currently, this project contains two subprojects: "Download Detailed Statistical Data from Choice Terminal" and "Extract Certain Keywords from PDF Documents Online."

When collecting data using the Choice Terminal, it is sometimes necessary to use a batch export option, as the target data may not have one. The "Download detailed statistical data from Choice Terminal" script simulates mouse clicks and keyboard input at specified locations, replacing the need for manual searching and downloading of tables. Then, it uses TabLib to consolidate information from a large number of XLSX files. This method is suitable for downloading XLSX-exported data that can only be accessed through the in-depth information of the underlying assets.

The "Extract certain keywords from PDF documents online" script (LetsCrawl!.py) reads online PDF files by calling PdfPlumber and requesting them using the link column provided in an XLSX file. It then uses regular expressions to match the content being searched. This is generally suitable for announcement files with a fixed format. When searching for announcements in Choice, irrelevant announcements can be excluded in advance using the advanced search feature. For example, when searching for announcements about convertible bond adjustments, search for titles containing "修" while excluding "修订," "修复," "修改," and "修文."
