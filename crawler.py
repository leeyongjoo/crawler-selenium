from selenium import webdriver
import component.cpu
import component.vga
import file

# url: danawa.com / tab: ad / limit: number of products / query: something to search
url_search = "http://search.danawa.com/dsearch.php?tab=goods&limit=90&query="

class Crawler:
    """
    데이터를 수집하는 크롤러 클래스
    """
    def __init__(self):
        # use Chrome webdriver
        self._browser = webdriver.Chrome()
        # wait 3 minutes
        self._browser.implicitly_wait(3)

    def crawling(self, c_url, numOfPages, c_instance, f_instance):
        """
        url에서 데이터를 수집하여 csv파일에 저장
        :param c_url: url about component
        :param numOfPages: number of pages
        :param c_instance: component class instance
        :param f_instance: file class instance
        :return:
        """
        for a in range(1, numOfPages + 1):
            url = c_url + "&page=" + str(a)
            self._browser.get(url)

            # products: list of html tags
            products = self._browser.find_elements_by_css_selector(
                "div[class='main_prodlist main_prodlist_list'] .prod_main_info")

            data_list = c_instance.handleDataList(products)
            f_instance.saveListToCSV(data_list)
            print(str(a) + " page is completed -" + c_instance._name)

    def quit(self):
        """
        close browser
        :return:
        """
        self._browser.quit()



if __name__ == "__main__":
    file1 = file.File()
    crawler1 = Crawler()

    # 1) vga of computer parts
    # vga1 = component.vga.Vga.instance()
    # file1.createCSV(vga1._name)
    #
    # url_vga = url_search + vga1._name
    # pages_vga = 9
    #
    # crawler1.crawling(url_vga, pages_vga, vga1, file1)
    # crawler1.quit()

    # 2) vga of computer parts
    cpu1 = component.cpu.Cpu.instance()
    file1.createCSV(cpu1._name)

    url_cpu = url_search + cpu1._name
    pages_cpu = 2

    crawler1.crawling(url_cpu, pages_cpu, cpu1, file1)
    crawler1.quit()