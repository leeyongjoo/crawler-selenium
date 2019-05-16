from sample import crawler
from sample.items import cpu,hdd,mainboard,power,ram,vga
import etc.time

# 검색할 상품의 개수
numProductforSearch = 900

def doCrawlingDataAndSaveFileOften(components, dnw, file):
    crl = crawler.Crawler()  # 크롤러 생성(크롬창 띄우기)

    for comp in components:
        # 키워드 이름
        keyword = comp.__class__.__name__.lower()

        # 파일경로, 파일 이름
        dirs = ["csv"] + [keyword]
        dirPath = file.generateDirPath(dirs)
        fileName = file.generateFile(dirPath, keyword, etc.time.getYMD_HM(), 'csv')

        # cpu 는 2 page 까지만...(200개의 상품을 넘어가면 가격이 있는 상품이 얼마 없음)
        if comp is cpu.Cpu.instance():
            numpageforSearch = 2
        else:
            numpageforSearch = int(numProductforSearch / int(dnw.limit))

        for pageNum in range(1, numpageforSearch + 1):
            # connecting url
            url = dnw.generateUrl(keyword, pageNum)

            # parsing data
            products = crl.parseElementsByCssSelector(url, dnw.productsSelector)

            # classfying data
            productDataList = dnw.classfyComponent(keyword, comp, products)

            # saving data
            file.saveListToCsv(productDataList, dirPath, fileName)
    crl.quit()

def doCrawlingDataAndSaveFileOnce(components, dnw, file):
    crl = crawler.Crawler()  # 크롤러 생성(크롬창 띄우기)

    for comp in components:
        # 키워드 이름
        keyword = comp.__class__.__name__.lower()

        # 파일경로, 파일 이름
        dirs = ["csv"] + [keyword]
        dirPath = file.generateDirPath(dirs)
        fileName = file.generateFile(dirPath, keyword, etc.time.getYMD_HM(), 'csv')

        output = []

        # cpu 는 2 page 까지만...(200개의 상품을 넘어가면 가격이 있는 상품이 얼마 없음)
        if comp is cpu.Cpu.instance():
            numpageforSearch = 2
        else:
            numpageforSearch = int(numProductforSearch / int(dnw.limit))

        for pageNum in range(1, numpageforSearch + 1):
            # connecting url
            url = dnw.generateUrl(keyword, pageNum)

            # parsing data
            products = crl.parseElementsByCssSelector(url, dnw.productsSelector)

            # classfying data
            productDataList = dnw.classfyComponent(keyword, comp, products)

            output += productDataList

        # saving data
        file.saveListToCsv(output, dirPath, fileName)
    crl.quit()

def doCrawlingDataComponents(components, dnw):
    crl = crawler.Crawler()  # 크롤러 생성(크롬창 띄우기)

    for comp in components:
        # 키워드 이름
        keyword = comp.__class__.__name__.lower()

        # cpu 는 2 page 까지만...(200개의 상품을 넘어가면 가격이 있는 상품이 얼마 없음)
        if comp is cpu.Cpu.instance():
            numpageforSearch = 2
        else:
            numpageforSearch = int(numProductforSearch / int(dnw.limit))

        for pageNum in range(1, numpageforSearch + 1):
            # connecting url
            url = dnw.generateUrl(keyword, pageNum)

            # parsing data
            products = crl.parseElementsByCssSelector(url, dnw.productsSelector)

            # classfying data
            productDataList = dnw.classfyComponent(keyword, comp, products)
    crl.quit()

def doCrawlingDataOneComponent(comp, dnw):
    crl = crawler.Crawler()  # 크롤러 생성(크롬창 띄우기)

    # 키워드 이름
    keyword = comp.__class__.__name__.lower()

    # cpu 는 2 page 까지만...(200개의 상품을 넘어가면 가격이 있는 상품이 얼마 없음)
    if comp is cpu.Cpu.instance():
        numpageforSearch = 2
    else:
        numpageforSearch = int(numProductforSearch / int(dnw.limit))

    for pageNum in range(1, numpageforSearch + 1):
        # connecting url
        url = dnw.generateUrl(keyword, pageNum)

        # parsing data
        products = crl.parseElementsByCssSelector(url, dnw.productsSelector)

        # classfying data
        productDataList = dnw.classfyComponent(keyword, comp, products)
    crl.quit()

def printCrawlingDataOneComponentOnePage(comp, dnw):
    crl = crawler.Crawler()  # 크롤러 생성(크롬창 띄우기)

    # 키워드 이름
    keyword = comp.__class__.__name__.lower()

    # connecting url
    url = dnw.generateUrl(keyword, 1)

    # parsing data
    products = crl.parseElementsByCssSelector(url, dnw.productsSelector)

    # classfying data
    productDataList = dnw.classfyComponent(keyword, comp, products)
    print(productDataList)

    crl.quit()