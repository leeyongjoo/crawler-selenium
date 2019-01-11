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
vga.setData(products)

# for product in products:
#     if product == "":
#         continue
#     f.write(product.find_element_by_css_selector(".prod_name a").text)
#
#     specs = product.find_element_by_css_selector(".prod_spec_set dd").text
#     specs = specs.split(" / ")
#     for spec in specs:
#         s = re.findall("[a-zA-Z]+", spec)
#         d = re.findall("[0-9]+", spec)
#
#         if not len(d):
#             continue
#         else:
#             f.write(",")
#             # f.write(''.join(s))
#             if len(d) > 1:
#                 f.write(str(d))
#             else:
#                 f.write(''.join(d))
#     f.write("\n")
#
# f.close()

    # print("- name: ", product.find_element_by_css_selector(".prod_name a").text)
    # print("- spec: ", end="")
    # specs = product.find_element_by_css_selector(".prod_spec_set dd").text
    # specs = specs.split(" / ")
    # for spec in specs:
    #     s = re.findall("[a-zA-Z]+", spec)
    #     d = re.findall("[0-9]+", spec)
    #
    #     if not len(s) or not len(d):
    #         continue
    #     else:
    #         print(s[0], end="")
    #         print(d, end="")
    #         print(",", end="")
    # print("")


# save...
# browser.save_screenshot("Website.png")

# close browser
browser.quit()