from sample import danawa, crawler, db
from sample.items import cpu,hdd,mainboard,power,ram,vga
import sample.file
import etc.time
import etc.progressBar
import multiprocessing


# 검색할 상품의 개수
numProductforSearch = 900

def doCrawlingDataAndSaveFile(components, dnw, file):
    crl = crawler.Crawler() # 크롤러 생성(크롬창 띄우기)

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
            numpageforSearch = 5

        for pageNum in range(1, numpageforSearch+1):
            # print progressBar
            etc.progressBar.printProgress(pageNum, numpageforSearch, keyword, 'Complete', 1, 50)

            # connecting url
            url = dnw.generateUrl(keyword, pageNum)

            # parsing data
            products = crl.parseElementsByCssSelector(url, dnw.productsSelector)

            # classfying data
            productDataList = dnw.classfyComponent(keyword, comp, products)

            # saving data
            file.saveListToCsv(productDataList, dirPath, fileName)
    crl.quit()

def doCrawlingDataAndSaveFileOneComp(comp, dnw, file):
    crl = crawler.Crawler() # 크롤러 생성(크롬창 띄우기)

    # 키워드 이름
    keyword = comp.__class__.__name__.lower()

    # 파일경로, 파일 이름
    dirs = ["csv"] + [keyword]
    dirPath = file.generateDirPath(dirs)
    fileName = file.generateFile(dirPath, keyword, etc.time.getYMD_HM(), 'csv')

    # cpu 는 1 page 까지만...(100개의 상품을 넘어가면 가격이 있는 상품이 얼마 없음)
    if keyword == 'cpu':
        numpageforSearch = 1
    else:
        numpageforSearch = 5

    for pageNum in range(1, numpageforSearch+1):
        # connecting url
        url = dnw.generateUrl(keyword, pageNum)

        # parsing data
        products = crl.parseElementsByCssSelector(url, dnw.productsSelector)

        # classfying data
        productDataList = dnw.classfyComponent(keyword, comp, products)

        # saving data
        file.saveListToCsv(productDataList, dirPath, fileName)

        # print progressBar
        etc.progressBar.printProgress(pageNum, numpageforSearch, keyword, 'Complete', 1, 50)

    # save to DataBase
    db.makeCtl(dirPath, fileName, keyword)
    db.saveDB(keyword)

    crl.quit()

def main():
    # 객체 생성
    dnw = danawa.Danawa()
    f = sample.file.File()

    # 각 부품 객체 생성
    components = []
    components.append(cpu.Cpu.instance())
    components.append(hdd.Hdd.instance())
    components.append(mainboard.Mainboard.instance())
    components.append(power.Power.instance())
    components.append(ram.Ram.instance())
    components.append(vga.Vga.instance())

    processes = []
    for comp in components:
        # 크롤링, 파일 저장
        p = multiprocessing.Process(target=doCrawlingDataAndSaveFileOneComp, args=(comp, dnw, f))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()