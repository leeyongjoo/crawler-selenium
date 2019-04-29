from sample import danawa, crawler
from sample.items import cpu,hdd,mainboard,power
import sample.file
import sample.time

# 검색할 상품의 개수, 검색할 페이지의 개수
numProductforSearch = 900

def doCrawlingDataAndSaveFile(components, dnw, file, selector):
    crl = crawler.Crawler()
    for comp in components:
        # 크롤러 생성(크롬창 띄우기)


        # 키워드 이름
        keyword = comp.__class__.__name__.lower()

        # 파일경로, 파일 이름
        dirs = ["csv"] + [keyword]
        dirPath = file.generateDirPath(dirs)
        fileName = file.generateFile(dirPath, keyword, sample.time.getYMD_HM(), 'csv')

        # cpu 는 2 page 까지만...(200개의 상품을 넘어가면 가격이 있는 상품이 얼마 없음)
        if comp is cpu.Cpu.instance():
            numpageforSearch = 2
        else:
            numpageforSearch = int(numProductforSearch / int(dnw.limit))

        for pageNum in range(1, numpageforSearch+1):
            # connecting url
            url = dnw.generateUrl(keyword, pageNum)

            # parsing data
            products = crl.parseElementsByCssSelector(url, selector)

            # classfying data
            productDataList = dnw.classfyComponent(keyword, comp, products)

            # saving data
            file.saveListToCsv(productDataList, dirPath, fileName)
    crl.quit()

def main():
    # 객체 생성
    dnw = danawa.Danawa()
    file = sample.file.File()
    
    #TODO thread, file 추가

    # 각 부품 객체 생성
    components = []
    components.append(cpu.Cpu.instance())
    components.append(hdd.Hdd.instance())
    # components.append(cpu.Cpu.instance())
    # components.append(cpu.Cpu.instance())
    # components.append(cpu.Cpu.instance())
    # components.append(cpu.Cpu.instance())

    # 상품의 css selector
    productsSelector = dnw.productsSelector



    doCrawlingDataAndSaveFile(components, dnw, file, productsSelector)



    # crawlers = []
    # threads = []
    #
    # for com in assorters:
    #     c = Crawler()
    #     f = file.File()
    #     f.create_csv(com._name)
    #
    #     url = url_search + com.get_name()
    #     if com.get_name() == 'cpu':
    #         pages = 3
    #     else:
    #         pages = 9
    #
    #     t = Thread(target=c.crawling_to_csv, args=(url, pages, com, f))
    #     threads.append(t)
    #     crawlers.append(c)
    #
    # for t in threads:
    #     t.start()
    # for t in threads:
    #     t.join()
    #
    # for c in crawlers:
    #     c.quit()

if __name__ == "__main__":
    main()