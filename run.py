from sample import danawa, crawler
from sample.items import cpu,hdd



def main():
    # 객체 생성
    dnw = danawa.Danawa()
    
    #TODO thread, file 추가

    # 각 부품 객체 생성
    component = []
    component.append(cpu.Cpu.instance())
    # component.append(hdd.Hdd.instance())
    # component.append(cpu.Cpu.instance())
    # component.append(cpu.Cpu.instance())
    # component.append(cpu.Cpu.instance())
    # component.append(cpu.Cpu.instance())

    # vga = vga.Vga.instance()
    # ram = ram.Ram.instance()
    # mainboard = mainboard.Mainboard.instance()
    # power = power.Power.instance()

    # 검색할 상품의 개수, 검색할 페이지의 개수
    numProductforSearch = 900
    # numpageforSearch = int(numProductforSearch / int(dnw.limit))

    # 상품의 css selector
    productsSelector = dnw.productsSelector

    for comp in component:
        crawler = crawler.Crawler()
        keyword = comp.__class__.__name__.lower()

        # cpu 는 2 page 까지만...(200개의 상품을 넘어가면 가격이 있는 상품이 얼마 없음)
        if comp is cpu.Cpu.instance():
            numpageforSearch = 2
        else:
            numpageforSearch = int(numProductforSearch / int(dnw.limit))

        for pageNum in range(1, numpageforSearch+1):
            url = dnw.generateUrl(keyword, pageNum)

            # parsing data
            products = crawler.parseElementsByCssSelector(url, productsSelector)
            productDataList = dnw.classfyComponent(keyword, comp, products)

            # saving data
            for a in productDataList:
                print(a)
        crawler.quit()



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