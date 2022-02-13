import requests
from bs4 import BeautifulSoup as soup
 
url="https://www.naukri.com/analyst-jobs-in-chennai?k=analyst&l=chennai"
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}
page=requests.get(url,headers)

bsobj=soup(page.content,'html.parser')
bsobj.prettify()

print(bsobj)
divs=bsobj.find_all('div',class_='info fleft')
print("divs")
print(divs)
for item in divs:
    title=item.find('a',class_='title fw500 ellipsis').text
    company=item.find('a',class_='subTitle ellipsis fleft').text
    location=item.find('span',class_='ellipsis fleft fs12 lh16 ').text
    try:
        salary=item.find('span',class_='ellipsis fleft fs12 lh16 ').text.strip()
    except:
        salary='Not found'
print(page.status_code)
