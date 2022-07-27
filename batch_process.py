import ast
import os
from os.path import join as pjoin
import sys
import re
from selenium import webdriver
import time




def isolate(lineno,file):
    output = []
    flag = False
    lib_import = True
    tabs = 0
    with open(file,'r') as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            if lib_import:
                if line.startswith('import '):
                    output.append(line)
                    continue
                if line.startswith('from ') and ' import ' in line:
                    output.append(line)
                    continue
            if i == lineno-1:
                flag = True
                lib_import = False
                if 'self, ' in line:
                    line.replace('self, ','')
                tabs = line.find('def ')
                output.append(line)
                continue
            if flag:
                if 'def ' in line or 'class ' in line:
                    if 'def ' in line:
                        dist = line.find('def ')
                    else:
                        dist = line.find('class ')
                    if dist <= tabs:
                        flag = False
                        break
                else:
                    output.append(line)
    with open(file,'w') as f:
        f.writelines(output)
  
def parse_request(request):
    file_path,url = request.split(' ')
    file_store,file_index = file_path.split('/')
    os.makedirs(pjoin(os.getcwd(),file_store),exist_ok=True)
    download_file(url)
    os.system('unzip {} -d {}'.format(pjoin(tmp_path,'*.zip'),tmp_path))
    os.system('rm {}'.format(pjoin(tmp_path,'*.zip')))
    os.system('mv {} {}'.format(pjoin(tmp_path,'*.py'),pjoin(os.getcwd(),file_store,file_index+'.py')))
    ln = url.split('#')[-1]
    ln.strip('\n')
    ln = ln[1:]
    isolate(int(ln),pjoin(os.getcwd(),file_store,file_index+'.py'))
def download_file(url):
    file_url = url.split('#')[0]
    # svn_url = re.sub('blob/+\w+/+','trunk/',file_url)
    global browser
    browser.get('https://minhaskamal.github.io/DownGit/#/home')
    time.sleep(5)
    browser.find_element('xpath','/html/body/div/div/div/div[4]/input').send_keys(file_url)
    time.sleep(2)
    browser.find_element('xpath','/html/body/div/div/div/div[5]/button[2]').click()
    time.sleep(5)
    # browser.close()
      
                
tmp_path = pjoin(os.getcwd(),'tmp')
os.makedirs(tmp_path,exist_ok=True)
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs',{'profile.default_content_settings.popups':0,'download.default_directory':tmp_path})
PROXY='127.0.0.1:1080'
options.add_argument('--proxy-server=%s' % PROXY)
browser = webdriver.Chrome(options=options)    
    
with open('./urls.txt','r') as f:
    files = f.read()
    files = files.split('\n')
    files = [file for file in files if len(file)>0]
    for file in files:
        parse_request(file)
browser.quit()