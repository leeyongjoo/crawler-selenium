import requests
import func
import re
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement

req = requests.get('http://shopping.naver.com/search/all.nhn?origQuery=cpu&pagingIndex=1&pagingSize=40&productSet=model&viewType=list&sort=rel&frm=NVSHMDL&query=cpu')
html = req.text
soup = BeautifulSoup(html, 'lxml')
my_titles = soup.find_all("div", "info")

prod_cpu = Element("prod")
for title in my_titles:
    # cpu_title
    if title.find('a').get('title'):
        cpu = Element("cpu")
        prod_cpu.append(cpu)
        cpu.attrib["title"] = title.find('a').get('title')
    # min_price
        SubElement(cpu, "minprice").text = title.find('span', class_='price').em.span.get_text()
    # MAX_price
        SubElement(cpu, "maxprice").text = title.find('span', class_='price').strong.span.get_text()
    # socket
        SubElement(cpu, "socket").text = title.find(text=re.compile(r'소켓'))[5:]
    # core
        SubElement(cpu, "core").text = title.find(text=re.compile(r'코어 형태'))[8:]
    # clock
        SubElement(cpu, "clock").text = title.find(text=re.compile(r'동작 클럭'))[8:]
    # power
        SubElement(cpu, "power").text = title.find(text=re.compile(r'설계 전력'))[8:]
    # L3_cache
        SubElement(cpu, "cache").text = title.find(text=re.compile(r'캐시'))[8:]
        # etc
        etcs = title.find_all('a', title=re.compile(r'부가기능'))
        my_etc = ""
        for etc in etcs:
            my_etc += etc.get_text() + ", "
        if my_etc is not "":
            SubElement(cpu, "etc").text = my_etc
        else:
            SubElement(cpu, "etc").text = " "

func.indent(prod_cpu)
func.createXml(prod_cpu, "cpu")