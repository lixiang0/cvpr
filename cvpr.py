import requests
import re
import os
import numpy as np
from multiprocessing import Process
import time

html = open('cvpr.html', 'r').read()

header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Mobile Safari/537.36',
}

ips = [line.split(' ') for line in open('result.txt', 'r').readlines()]

if not os.path.exists('pdfs'):
    os.mkdir('pdfs')
pdfs = re.findall(r'<a href="content_CVPR_2020/papers/.*">', html)

tasks=set()

def process(i,pdf,length):
    pry = ips[np.random.randint(0, len(ips))]
    ip=pry[0]
    port=pry[1]
    scheme=pry[3]
    proxy = {f'{scheme}': f'{scheme}://{ip}:{port}'}
    pdf_name=pdf.split('/')[-1]
    pdf = 'http://openaccess.thecvf.com/'+pdf
    # print(pdf,ip)
    try:
        response = requests.get(pdf, headers=header,
                            proxies=proxy, stream=True, timeout=10)
        if response.status_code == 200:
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            print(i,'/',length,':',pdf_name,' done..')
            tasks.remove(i)
            print(f'remain {len(tasks)} downloading task... ')
    except Exception as e:
        # print(e)
        return  

if __name__ == '__main__':
    length=len(pdfs)
    for i,pdf in enumerate(pdfs):
        pdf_url=pdf[9:-2]
        pdf_name=pdf_url.split('/')[-1]
        pdf_path = 'pdfs/'+pdf_name
        if os.path.exists(pdf_path) and os.stat(pdf_path).st_size > 10:
            print(i,'/',length,':',pdf_name,'  exist..')
            continue
        tasks.add(i)
        print(i,'/',length,':',pdf_name,'  downloading....')
        Process(target=process, args=(i,pdf_url,length,)).start()
        time.sleep(5)
        
