import os
from xml.etree.ElementTree import ElementTree

DIR_WEIGHTS = './parsed_xml/'

if not os.path.exists(DIR_WEIGHTS):
    os.mkdir(DIR_WEIGHTS)

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def createXml(t, n):   #n.xml 생성
    ElementTree(t).write("parsed_xml\\" + n + ".xml" , encoding="utf-8", xml_declaration=True)