import requests
import func
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement

req = requests.get('http://hs.ac.kr/sites/kor/index.do')
html = req.text
soup = BeautifulSoup(html, 'lxml')
print(soup.prettify())
my_titles = soup.find_all('div','next_page')

#for title in my_titles:
 #   print(title.get_text())