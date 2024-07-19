#main窗口程序

import tkinter as tk
from tkinter import filedialog,messagebox
from tkinter.ttk import Progressbar
import os
from arxiv.spider import scrape_arxiv,save_to_json
from arxiv.downloads import download_pdf,get_pdf_url,download_from_json


#选择存储路径
def select_save_path():
    directory=filedialog.askdirectory()
    if directory:
        save_path_var.set(os.path.normpath(directory))



def update_progress(progress):
    progress_var.set(progress)
    root.update_idletasks()


def start_scraping():
    field=field_var.get()
    num_papers=num_papers_var.get()
    save_path=save_path_var.get()

    if not field or not num_papers or not save_path:
        messagebox.showerror("错误，请指定相关领域与需要获取的数量与存储路径")
        return
    
    try:
        num_papers=int(num_papers)
        papers=scrape_arxiv(field,num_papers,update_progress)
        json_file_path=os.path.join(save_path,'arxiv_papers.json')
        save_to_json(papers,json_file_path)
        messagebox.showinfo("Success","Scraping completed successfully! Starting downloading...")

        total_papers=len(papers)
        for i,paper in enumerate(papers,start=1):
            pdf_url=get_pdf_url(paper.get('url'))
            download_from_json(json_file_path,save_path)
            update_progress((i/total_papers)*100)

        messagebox.showinfo("Success","Download completed successfully!")
    except Exception as e:
        messagebox.showerror("Error",f"An error occurred: {e}")



root=tk.Tk()
root.title("ArXiv PDF Downloader")


#定义变量
field_var=tk.StringVar(root)
num_papers_var=tk.StringVar(root)
save_path_var=tk.StringVar(root)
progress_var=tk.DoubleVar(root)

# 创建并放置组件
tk.Label(root, text="Enter Field:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=field_var, width=50).grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Number of Papers:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=num_papers_var, width=50).grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Select Save Directory:").grid(row=2, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=save_path_var, width=50).grid(row=2, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_save_path).grid(row=2, column=2, padx=10, pady=10)

progress_bar = Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=20, sticky='ew')

tk.Button(root, text="Start", command=start_scraping).grid(row=4, column=1, pady=10)
tk.Button(root,text="Exit",command=root.destroy).grid(row=5,column=1,pady=10)


root.mainloop()
