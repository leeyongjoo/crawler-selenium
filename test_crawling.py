import component.mainboard
from selenium import webdriver

url_search = "http://search.danawa.com/dsearch.php?tab=goods&limit=90&query="
m_instance = component.mainboard.Mainboard().instance()
numOfPages = 1

# use Chrome webdriver
browser = webdriver.Chrome()
# wait 3 minutes
browser.implicitly_wait(3)

url = url_search + m_instance._name

for a in range(1, numOfPages + 1):
    url = url + "&page=" + str(a)
    browser.get(url)

    # products: list of html tags
    products = browser.find_elements_by_css_selector(
        "div[class='main_prodlist main_prodlist_list'] .prod_main_info")

    data_list = m_instance.handle_data_list(products)
    for data in data_list:
        print(data)

browser.quit()