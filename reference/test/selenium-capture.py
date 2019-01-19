from selenium import webdriver

url_vga = "http://prod.danawa.com/list/?cate=112753"

# PhantomJS 드라이버 추출하기 --- (※1)
browser = webdriver.Chrome()
# 3초 대기하기 --- (※2)
browser.implicitly_wait(3)
# URL 읽어 들이기 --- (※3)
browser.get(url_vga)
# 화면을 캡처해서 저장하기 --- (※4)


products = browser.find_elements_by_css_selector(".prod_main_info .prod_info")
for product in products:
    if product == "":
        continue
    print("-", product.text)
# browser.save_screenshot("Website.png")

# 브라우저 종료하기 --- (※5)
# browser.quit()