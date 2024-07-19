import requests
from bs4 import BeautifulSoup
import time
import csv
import json




def scrape_arxiv(field,number_of_papers,progress_callback=None):
    base_url='https://arxiv.org'
    search_url=f"{base_url}/search/?query={field}&searchtype=all&source=header"


    papers=[]
    page_number=0

    while len(papers) < number_of_papers:
        request_url=search_url+ f"&start={page_number*50}"
        print(f"FEtching page{page_number + 1} from URL:{request_url}...")
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
            }
        responses=requests.get(request_url,headers=headers)
        if responses.status_code!=200:
            print(f"Failed to retrieve page {page_number + 1}")
            break

        soup=BeautifulSoup(responses.text,'html.parser')
        results=soup.find_all('li',class_='arxiv-result')

        if not results:
            print(f"No results found on page {page_number + 1}")
            break

        for result in results:
            title_element=result.find('p',class_='title')
            authors_element=result.find('p',class_='authors')
            abstract_element=result.find('p',class_='abstract')

            list_title_element=result.find('p',class_='list-title')
            if list_title_element:
                link_element=list_title_element.find('a')
                if link_element and 'href' in link_element.attrs:
                    paper_url=link_element['href']
                    paper_id= link_element.text.strip()

            if title_element and authors_element and abstract_element:
                paper={
                    ''
                    'title':title_element.text.strip(),
                    'author':authors_element.text.strip(),
                    'abstract':abstract_element.text.strip(),
                    'url':paper_url,
                    'id':paper_id
                }
                papers.append(paper)
                if len(papers) >= number_of_papers:
                    break

                if progress_callback:
                    progress=(len(papers)/number_of_papers)*100
                    progress_callback(progress)

        page_number +=1
        time.sleep(15)
    return papers
    

def save_to_csv(papers,filename):
    keys=papers[0].keys()
    with open(filename,"w",newline='',encoding='utf-8') as output_file:
        dict_writer=csv.DictWriter(output_file,fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(papers)

def save_to_json(papers,filename):
    with open(filename,'w',encoding='utf-8') as output_file:
        json.dump(papers,output_file,ensure_ascii=False,indent=4)


#测试

if __name__ =="__main__":
    field='cv'
    number_of_papers= 5
    papers=scrape_arxiv(field,number_of_papers)
    #save_to_csv(papers,'arxiv_papers.csv')       #保存至csv文件中
    #save_to_json(papers,'arxiv_papers.json')     #保存至json文件中
    
    for paper in papers:
        print(f"title:{paper['title']}")
        print(f"authors:{paper['author']}")
        print(f"abstract:{paper['abstract']}")
        print(f"url:{paper['url']}")
        print(f"id:{paper['id']}")
        print('-'*80)