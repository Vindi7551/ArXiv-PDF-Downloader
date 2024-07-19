#下载程序

import os
import io
import requests
import json
import time


def get_pdf_url(arxiv_url):
    return arxiv_url.replace('/abs/','/pdf/')




def download_pdf(pdf_url,save_path,id):
    send_headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    responses=requests.get(pdf_url,headers=send_headers)
    bytes_io=io.BytesIO(responses.content)
    pdf_path=os.path.join(save_path,f"{id}"+".PDF")
    print(f"{pdf_path}")

    if responses.status_code==200:
        with open(pdf_path,mode='wb') as f:
            f.write(bytes_io.getvalue())
            print(f"{id}.pdf 下载成功！")
    else:
        print(f"{id}.pdf 下载失败, Status code:{responses.status_code}")




def download_from_json(json_file_path,save_path):
    with open(json_file_path,'r',encoding='utf-8') as file:
        data=json.load(file)
        for entry in data:
            url=entry.get('url')
            id=entry.get('id')
            
            if url:
                pdf_url=get_pdf_url(url)
                id1=id.replace('arXiv:','')
                print(f"{pdf_url}")
                print(f"{id1}")
                download_pdf(pdf_url,save_path,id1)
                time.sleep(4)
        


    


if __name__=='__main__':
    save_path=r'D:\desktop\pachong\arxiv\pdf'
    json_file_path=r"D:\desktop\pachong\arxiv_papers.json"
    download_from_json(json_file_path,save_path)
