import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from PyPDF2 import PdfReader, PdfWriter

def split_pdf_by_pages(pdf_file_path, split_pages, output_dir=None):
    """
    按指定页码分割PDF文件（核心分割逻辑）
    
    参数:
        pdf_file_path: 待分割的PDF文件完整路径（已校验）
        split_pages: 分割页码列表（已校验）
        output_dir: 分割后文件的保存目录（默认和原PDF同目录）
    """
    # 设置输出目录（默认和原PDF同目录）
    if output_dir is None or output_dir.strip() == "":
        output_dir = os.path.dirname(pdf_file_path)
    
    # 读取原PDF并分割
    try:
        reader = PdfReader(pdf_file_path)
        total_pages = len(reader.pages)
        messagebox.showinfo("提示", f"检测到PDF总页数：{total_pages}页")
        
        # 补充最后一个分割点（到最后一页）
        split_pages.append(total_pages + 1)
        
        # 按页码范围分割
        split_count = 0
        for i in range(len(split_pages) - 1):
            start_page = split_pages[i] - 1  # PyPDF2页码从0开始，用户输入从1开始
            end_page = split_pages[i+1] - 1
            
            # 校验页码是否超出范围
            if start_page >= total_pages:
                break
            # 确保end_page不超过总页数
            end_page = min(end_page, total_pages)
            
            # 初始化PDF写入器
            writer = PdfWriter()
            
            # 添加指定页码的页面到新PDF
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])
            
            # 生成输出文件名（原文件名_分割序号_页码范围.pdf）
            original_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
            output_filename = f"{original_name}_part{split_count+1}_pages{split_pages[i]}-{split_pages[i+1]-1}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            # 写入分割后的PDF文件
            with open(output_path, "wb") as f:
                writer.write(f)
            
            split_count += 1
        
        if split_count > 0:
            messagebox.showinfo("成功", f"PDF分割完成！\n共生成 {split_count} 个文件，保存至：\n{output_dir}")
        else:
            messagebox.showwarning("提示", "未生成任何分割文件（分割页码超出PDF总页数）！")
    
    except Exception as e:
        messagebox.showerror("分割失败", f"出错原因：{str(e)}\n请检查PDF文件是否加密或损坏")

def get_input_and_split():
    """
    弹出输入框获取PDF路径和分割页码（每步支持重试/返回修改），执行分割
    """
    # 创建隐藏的tkinter主窗口
    root = tk.Tk()
    root.withdraw()
    
    # ------------------- 步骤1：获取PDF文件路径（支持重试） -------------------
    pdf_path = None
    while True:
        # 弹出输入框
        pdf_path_input = simpledialog.askstring(
            title="PDF分割工具 - 步骤1/2",
            prompt="请粘贴待分割的PDF文件完整路径：\n（支持不带.pdf后缀，示例：C:/Users/xxx/Desktop/test 或 C:/Users/xxx/Desktop/test.pdf）"
        )
        
        # 处理用户点击「取消」
        if pdf_path_input is None:
            if messagebox.askyesno("确认退出", "确定要取消操作吗？"):
                messagebox.showinfo("提示", "已取消操作")
                return
            else:
                continue  # 用户选择「不退出」，重新弹出输入框
        
        # 处理输入内容
        pdf_path_input = pdf_path_input.strip().strip('"').strip("'")
        if not pdf_path_input:
            if messagebox.askretrycancel("错误", "PDF文件路径不能为空！\n是否重试？"):
                continue  # 用户选择「重试」，重新弹出输入框
            else:
                messagebox.showinfo("提示", "已取消操作")
                return
        
        # 校验路径（自动补.pdf后缀）
        temp_path = pdf_path_input
        path_valid = False
        if os.path.isfile(temp_path):
            path_valid = True
        else:
            if not temp_path.lower().endswith(".pdf"):
                temp_path_with_suffix = temp_path + ".pdf"
                if os.path.isfile(temp_path_with_suffix):
                    temp_path = temp_path_with_suffix
                    path_valid = True
        
        # 路径无效时的处理
        if not path_valid:
            error_msg = f"文件 '{pdf_path_input}' 或 '{pdf_path_input}.pdf' 不存在！"
            if messagebox.askretrycancel("错误", f"{error_msg}\n是否重试？"):
                continue
            else:
                messagebox.showinfo("提示", "已取消操作")
                return
        
        # 校验是否为PDF文件
        if not temp_path.lower().endswith(".pdf"):
            if messagebox.askretrycancel("错误", "请输入有效的PDF文件路径！\n是否重试？"):
                continue
            else:
                messagebox.showinfo("提示", "已取消操作")
                return
        
        # 路径有效，确认后进入下一步
        pdf_path = temp_path
        if messagebox.askyesno("确认路径", f"已识别到有效PDF文件：\n{pdf_path}\n是否继续下一步？"):
            break
        else:
            continue  # 用户选择「不继续」，重新输入路径
    
    # ------------------- 步骤2：获取分割页码（支持重试） -------------------
    split_pages = None
    while True:
        # 弹出输入框
        split_pages_input = simpledialog.askstring(
            title="PDF分割工具 - 步骤2/2",
            prompt="请输入分割页码（支持英文逗号/中文逗号/空格分隔，如 1,5,10 或 1，5，10 或 1 5 10）：\n说明：1,5,10 表示分割为 1-4页、5-9页、10-最后一页"
        )
        
        # 处理用户点击「取消」
        if split_pages_input is None:
            if messagebox.askyesno("确认退出", "确定要取消操作吗？"):
                messagebox.showinfo("提示", "已取消操作")
                return
            else:
                continue  # 用户选择「不退出」，重新弹出输入框
        
        # 处理输入内容
        split_pages_input = split_pages_input.strip()
        if not split_pages_input:
            if messagebox.askretrycancel("错误", "分割页码不能为空！\n是否重试？"):
                continue
            else:
                messagebox.showinfo("提示", "已取消操作")
                return
        
        # 兼容多种分隔符（中文逗号、空格 → 英文逗号）
        split_pages_processed = split_pages_input.replace("，", ",").replace(" ", ",")
        # 过滤连续逗号导致的空字符串
        split_pages_list = [page.strip() for page in split_pages_processed.split(",") if page.strip()]
        
        # 解析并校验页码
        try:
            split_pages_temp = [int(page) for page in split_pages_list]
            split_pages_temp = sorted(split_pages_temp)
            if split_pages_temp[0] < 1:
                raise ValueError("页码不能小于1")
        except ValueError:
            error_msg = "分割页码格式错误！请输入正整数，用英文逗号/中文逗号/空格分隔（如 1,5,10）"
            if messagebox.askretrycancel("错误", f"{error_msg}\n是否重试？"):
                continue
            else:
                messagebox.showinfo("提示", "已取消操作")
                return
        
        # 页码有效，确认后执行分割
        split_pages = split_pages_temp
        if messagebox.askyesno("确认页码", f"已识别到分割页码：{split_pages}\n是否开始分割？"):
            break
        else:
            continue  # 用户选择「不继续」，重新输入页码
    
    # ------------------- 执行分割 -------------------
    split_pdf_by_pages(pdf_path, split_pages)

# ------------------- 运行程序 -------------------
if __name__ == "__main__":
    get_input_and_split()