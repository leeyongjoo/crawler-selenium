# -*- coding: utf-8 -*-
from selenium import webdriver
from functions import *

class Crawler:
    """
    데이터를 수집하는 크롤러 클래스
    """
    def __init__(self):
        # use Chrome webdriver
        self._browser = webdriver.Chrome()
        # wait 10 minutes
        self._browser.implicitly_wait(10)

    def crawling_to_csv(self, c_url, numOfPages, c_instance, f_instance):
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

            data_list = c_instance.handle_data_list(products)
            f_instance.save_list_to_csv(data_list)
            print(str(a) + " page is completed -" + c_instance._name)
        print(c_instance._name, "is finished!")

    def quit(self):
        """
        close browser
        :return:
        """
        self._browser.quit()

    def crawlingPage(self, url):
        """
        url로부터 page를 가져온 후 반환
        :param url: url address
        :return page: page source
        """
        self._browser.get(url)
        page = self._browser.page_source()

        return page

if __name__ == "__main__":

    searchPageOfDanawa = "http://search.danawa.com/dsearch.php"
    keyword = "cpu"
    pageNum = 1

    url = getUrlofDanawa(searchPageOfDanawa, keyword, pageNum)

    c = Crawler()

    print(c.crawlingPage(url))
    c.quit()