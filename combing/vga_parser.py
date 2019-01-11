import requests
import combing.func as func
import re
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement

req = requests.get('http://shopping.naver.com/search/all.nhn?origQuery=%EA%B7%B8%EB%9E%98%ED%94%BD%EC%B9%B4%EB%93%9C&pagingIndex=1&pagingSize=40&productSet=model&viewType=list&sort=rel&frm=NVSHMDL&query=%EA%B7%B8%EB%9E%98%ED%94%BD%EC%B9%B4%EB%93%9C')
html = req.text
soup = BeautifulSoup(html, 'lxml')
my_titles = soup.find_all("div", "info")

prod_vga = Element("prod")
for title in my_titles:
    # vga_title
    if title.find('a').get('title') or "":
        vga = Element("vga")
        prod_vga.append(vga)
        vga.attrib["title"] = title.find('a').get('title')
        # min_price
        SubElement(vga, "minprice").text = title.find('span', class_='price').em.span.get_text()
        # MAX_price
        SubElement(vga, "maxprice").text = title.find('span', class_='price').strong.span.get_text()
        # memory
        SubElement(vga, "mem").text = title.find(text=re.compile(r'메모리 :'))[6:]
        # clock
        SubElement(vga, "clock").text = title.find(text=re.compile(r'GPU 클럭'))[9:]
        # interface
        SubElement(vga, "interface").text = title.find(text=re.compile(r'인터페이스'))[8:]

func.indent(prod_vga)
func.createXml(prod_vga, "vga")