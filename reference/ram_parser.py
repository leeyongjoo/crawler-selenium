import requests
import func
import re
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement

req = requests.get('http://shopping.naver.com/search/all.nhn?origQuery=ram&pagingIndex=1&pagingSize=40&productSet=model&viewType=list&sort=rel&frm=NVSHMDL&query=ram')
html = req.text
soup = BeautifulSoup(html, 'lxml')
my_titles = soup.find_all("div", "info")

prod_ram = Element("prod")
for title in my_titles:
    # ram_title
    if title.find('a').get('title'):
        ram = Element("ram")
        prod_ram.append(ram)
        ram.attrib["title"] = title.find('a').get('title')
    # min_price
        SubElement(ram, "minprice").text = title.find('span', class_='price').em.span.get_text()
    # MAX_price
        SubElement(ram, "maxprice").text = title.find('span', class_='price').strong.span.get_text()
    # type
        SubElement(ram, "type").text = title.find(text=re.compile(r'메모리방식'))[8:]
    # clock
        SubElement(ram, "clock").text = title.find(text=re.compile(r'버스 클럭'))[8:]
    # module
        SubElement(ram, "module").text = title.find(text=re.compile(r'PC 레이팅'))[9:]

func.indent(prod_ram)
func.createXml(prod_ram, "ram")