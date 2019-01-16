from selenium import webdriver
import component

url_search = "http://search.danawa.com/dsearch.php?tab=goods&limit=90&query="
num_page = 1    # 90 * pages

# use Chrome webdriver
browser = webdriver.Chrome()
# wait 3 minutes
browser.implicitly_wait(3)

# crawling

#===== test
f = open('output.csv', 'w', encoding='utf-8', newline='')
f.close
#=====;

vga = component.VGA()

for a in range(1,num_page+1):
    url_vga = url_search + "vga"
    url_vga += "&page=" + str(a)  #page = 1
    browser.get(url_vga)

    # products: list of product info
    products = browser.find_elements_by_css_selector("div[class='main_prodlist main_prodlist_list'] .prod_main_info")
    vga.preprocessListData(products)

    print(str(a) + "page is completed!")


# save...
# browser.save_screenshot("Website.png")

# close browser
browser.quit()