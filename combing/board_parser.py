import requests
import func
import re
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement

req = requests.get('http://shopping.naver.com/search/all.nhn?origQuery=%EB%A9%94%EC%9D%B8%EB%B3%B4%EB%93%9C&pagingIndex=1&pagingSize=40&productSet=model&viewType=list&sort=rel&frm=NVSHMDL&query=%EB%A9%94%EC%9D%B8%EB%B3%B4%EB%93%9C')
html = req.text
soup = BeautifulSoup(html, 'lxml')
my_titles = soup.find_all("div", "info")

prod_board = Element("prod")
for title in my_titles:
    # board_title
    if title.find('a').get('title'):
        board = Element("board")
        prod_board.append(board)
        board.attrib["title"] = title.find('a').get('title')
    # min_price
        SubElement(board, "minprice").text = title.find('span', class_='price').em.span.get_text()
    # MAX_price
        SubElement(board, "maxprice").text = title.find('span', class_='price').strong.span.get_text()
    # socket
        SubElement(board, "socket").text = title.find(text=re.compile(r'소켓'))[5:]
    # standard
        SubElement(board, "std").text = title.find(text=re.compile(r'규격'))[5:]
    # vga_slot
        SubElement(board, "vgaslot").text = title.find(text=re.compile(r'VGA 슬롯'))[9:]
    # MAX_memory
        SubElement(board, "maxmem").text = title.find(text=re.compile(r'최대 메모리'))[9:]

func.indent(prod_board)
func.createXml(prod_board, "board")