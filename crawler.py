from selenium import webdriver
import re
import component

url_search = "http://search.danawa.com/dsearch.php?tab=goods&query="

url_vga = url_search + "vga"
# url_vga += "&page=2"

# use Chrome webdriver
browser = webdriver.Chrome()

# wait 3 minutes
browser.implicitly_wait(3)
# URL connect
browser.get(url_vga)


# filtering & make csv
f = open("vga.csv", "w")

products = browser.find_elements_by_css_selector("div[class='main_prodlist main_prodlist_list'] .prod_main_info")

vga = component.VGA()
vga.preprocessData(products)



# save...
# browser.save_screenshot("Website.png")

# close browser
browser.quit()