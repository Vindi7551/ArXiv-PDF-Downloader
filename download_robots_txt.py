#此文件用来自动获取网站的robots.txt


import requests
import os

def sanitize_filename(url):
    # 移除非法字符，只保留字母、数字、下划线和点
    return ''.join(c if c.isalnum() or c in {'_', '.'} else '_' for c in url)

def download_robots_txt(url, save_path):
    try:
        robots_url = f"{url}/robots.txt"
        response = requests.get(robots_url)
        if response.status_code == 200:
            # 使用清理函数处理URL，生成安全的文件名
            safe_filename = sanitize_filename(url) + '_robots.txt'
            full_path = os.path.join(save_path, safe_filename)
            os.makedirs(save_path, exist_ok=True)
            with open(full_path, 'w') as file:
                file.write(response.text)
            print(f"'robots.txt' has been downloaded and saved as {full_path}.")
        else:
            print(f"Failed to download 'robots.txt'. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage
download_robots_txt('https://arxiv.org',r'D:\desktop\pachong')
