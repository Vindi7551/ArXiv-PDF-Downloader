import io
import requests
import os
def download_pdf(pdf_url,save_path,id):
    send_headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    responses=requests.get(pdf_url,headers=send_headers)
    bytes_io=io.BytesIO(responses.content)
    pdf_path=os.path.join(save_path,"123.PDF")
    print(f"{pdf_path}")

    if responses.status_code==200:
        with open(pdf_path,mode='wb') as f:
            f.write(bytes_io.getvalue())
            print(f"{id}.pdf 下载成功！")
    else:
        print(f"{id}.pdf 下载失败, Status code:{responses.status_code}")


if __name__=="__main__":
    pdf_url='https://arxiv.org/pdf/2407.11086'
    save_path=r"D:\desktop\pachong\arxiv\pdf"
    id="arXiv:2407.11086"
    download_pdf(pdf_url,save_path,id)