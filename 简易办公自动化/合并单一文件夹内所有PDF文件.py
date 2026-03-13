# %%
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from PyPDF2 import PdfMerger

def merge_all_pdfs_in_folder(folder_path, output_filename="合并后文件.pdf"):
    """
    合并指定文件夹下的所有 PDF 文件
    
    参数:
        folder_path: 存放 PDF 文件的文件夹路径
        output_filename: 合并后的 PDF 文件名（默认是 merged.pdf）
    """
    # 初始化 PDF 合并器
    merger = PdfMerger()
    
    # 验证文件夹是否存在
    if not os.path.isdir(folder_path):
        messagebox.showerror("错误", f"文件夹 '{folder_path}' 不存在！")
        return
    
    # 遍历文件夹，筛选出所有 PDF 文件并按文件名排序
    pdf_files = []
    for filename in os.listdir(folder_path):
        # 只处理 .pdf 后缀的文件（忽略大小写）
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            pdf_files.append(file_path)
    
    # 检查是否有 PDF 文件
    if not pdf_files:
        messagebox.showwarning("提示", "指定文件夹中未找到任何 PDF 文件！")
        return
    
    # 按文件名排序（保证合并顺序可预期）
    pdf_files.sort()
    
    # 逐个添加 PDF 文件到合并器
    try:
        for pdf_file in pdf_files:
            merger.append(open(pdf_file, "rb"))
        
        # 生成合并后的文件路径
        output_path = os.path.join(folder_path, output_filename)
        # 写入合并后的 PDF 文件
        with open(output_path, "wb") as output_file:
            merger.write(output_file)
        
        messagebox.showinfo("成功", f"PDF 合并完成！\n文件保存至：{output_path}")
    
    except Exception as e:
        messagebox.showerror("合并失败", f"出错原因：{str(e)}")
    
    finally:
        # 关闭合并器，释放资源
        merger.close()

def get_folder_path_and_merge():
    """
    弹出输入框获取文件夹路径，确认后执行合并
    """
    # 创建隐藏的 tkinter 主窗口（仅用于弹出对话框）
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    # 弹出输入框，提示用户粘贴文件夹路径
    folder_path = simpledialog.askstring(
        title="PDF 合并工具",
        prompt="请粘贴需要合并 PDF 的文件夹路径：\n（示例：C:/Users/xxx/Desktop/pdfs 或 ./pdf_files）"
    )
    
    # 判断用户操作：点击取消/关闭则退出，输入路径则执行合并
    if folder_path is None:
        messagebox.showinfo("提示", "已取消操作")
        return
    if folder_path.strip() == "":
        messagebox.showwarning("提示", "文件夹路径不能为空！")
        return
    
    # 执行合并操作
    merge_all_pdfs_in_folder(folder_path.strip())

# ------------------- 运行程序 -------------------
if __name__ == "__main__":
    get_folder_path_and_merge()


