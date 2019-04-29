import re

class Danawa:
    """
    Danawa.com
    """
    searchPageOfDanawa = "http://search.danawa.com/dsearch.php"
    productsSelector = "div[class='main_prodlist main_prodlist_list'] .prod_main_info"

    # 광고제거 여부(goods==제거)
    tab = "goods"
    # 상품 개수(30, 60, 90)
    limit = "90"

    def generateUrl(mainboard, keyword, pageNum, tab=tab, limit=limit):
        """
        :param tab: 광고제거 여부(goods==제거)
        :param limit: 보여지는 상품 개수
        :param keyword: 검색할 키워드
        :param pageNum: 페이지 번호
        :return:
        """
        return mainboard.searchPageOfDanawa + "?" + "tab=" + tab + "&limit=" + limit \
               + "&query=" + keyword + "&page=" + str(pageNum)



# ===== classify
    def classfyComponent(mainboard, keyword, comp, products):
        if keyword == 'cpu':
            return mainboard.classifyCpu(comp, products)
        elif keyword == 'hdd':
            return mainboard.classifyHdd(comp, products)


    def classifyCpu(mainboard, cpu, products):
        """
        html tag List를 받아 제품 List를 반환

        :param cpu: component
        :param products: list of selenium.webdriver.remote.webelement.WebElement
        :return: List 형태의 분류된 정보
        """
        colName = cpu.colName
        colColIdetifier = cpu.colIdentifier

        output = []  # list of row
        for product in products:
            cpu.__init__()  # init dict

            if product == "":
                continue

            name = product.find_element_by_css_selector(".prod_name a").text
            name_split = name.split(" ")
            if name_split[-1] == "(중고)":
                continue

            # pcode = product.find_element_by_css_selector(".relation_goods_unit").get_attribute('id')
            # pcode = re.findall("[0-9]+", pcode)[0]
            #
            # cpu._dict[colName[0]] = pcode            # pcode
            cpu._dict[colName[0]] = name  # name
            cpu._dict[colName[1]] = name_split[0]  # manufacturer

            i = 2  # colName index (start from 'prod_name')

            # specs is string sep by ' / '
            specs = product.find_element_by_css_selector(".prod_spec_set dd").text
            specs = specs.split(" / ")
            for spec in specs:

                # colName[i] == 'etc'
                if i == len(colName) - 2:
                    spec = spec.replace(',', '')

                    if cpu._dict[colName[i]] == "NA":
                        cpu._dict[colName[i]] = spec
                    else:
                        cpu._dict[colName[i]] += " / " + spec

                word = re.findall("[^0-9]+", spec)
                num = re.findall("[0-9]+", spec)

                # until colName[i] == 'etc'
                while (i < len(colName) - 2):

                    j = i - 2  # colColIdetifier index

                    if i == 2:  # 2: socket
                        s_split = spec.split("(")
                        if cpu._dict[colName[1]] == s_split[0]:
                            cpu._dict[colName[i]] = s_split[1].replace(")", "")
                        i += 1
                        break

                    if i == 4:  # 4: core
                        if spec[-2:] == colColIdetifier[j]:
                            cpu._dict[colName[i]] = spec[:2]
                            i += 1
                            break

                    if i == 6:  # 6: clock
                        if word[-1].replace(" ", "") == colColIdetifier[j]:
                            cpu._dict[colName[i]] = spec.replace(colColIdetifier[j], "").replace(" ", "")
                            i += 1
                            break

                    if i == 7:  # 7: l2
                        if word[-1][-1] == 'B':
                            if word[-1][-2] == 'M':
                                cpu._dict[colName[i + 1]] = int(num[0]) * 1024
                            elif word[-1][-2] == 'K':
                                cpu._dict[colName[i + 1]] = num[0]
                            i += 1
                            break
                        elif word[-1][-1] == 'x':
                            if word[-1][0] == 'M':
                                cpu._dict[colName[i + 1]] = int(num[0]) * int(num[1]) * 1024
                            elif word[-1][0] == 'K':
                                cpu._dict[colName[i + 1]] = int(num[0]) * int(num[1])
                            i += 1
                            break
                    if i == 8:  # 8: l3
                        if word[0][-1] == 'B':
                            cpu._dict[colName[i - 1]] = cpu._dict[colName[i]]
                            cpu._dict[colName[i]] = int(num[0]) * 1024
                            i += 1
                            break

                    if i == 9:  # 9: bit
                        if spec[-2:] == colColIdetifier[j]:
                            cpu._dict[colName[i]] = spec[:-2]
                            i += 1
                            break

                    if i == 11:  # 11: gpu_name
                        if spec.split(" ")[0] in colColIdetifier[j]:
                            cpu._dict[colName[i]] = spec
                            i += 1
                            break

                    if colColIdetifier[j] != word[-1]:
                        i += 1

                    elif len(num):
                        cpu._dict[colName[i]] = num[0]
                        i += 1
                        break

            price = product.find_element_by_css_selector(".prod_pricelist .price_sect strong").text
            cpu._dict[colName[-1]] = price.replace(",", "")

            # filter the data has no price
            if not cpu._dict[colName[-1]].isdigit():
                cpu._dict[colName[-1]] = 'NA'

            output.append(cpu._dict.values())
        return output

    def classifyHdd(mainboard, hdd, products):
        """
        html tag List를 받아 제품 List를 반환
        :param products: html tag로 이루어진 여러 제품에 대한 정보 List
        :return output: 정제된 List
        """
        output = [] # list of row
        for product in products:
            hdd.__init__()  # init dict

            if product == "":
                continue

            name = product.find_element_by_css_selector(".prod_name a").text
            name_split = name.split(" ")
            if name_split[-1] == "(중고)":    # except 중고제품
                continue

            col_index = 0  # hdd.colName index

            hdd._dict[hdd.colName[col_index]] = name; col_index+=1             # name
            hdd._dict[hdd.colName[col_index]] = name_split[0]; col_index+=1    # manufacturer

            # specs is string sep by ' / '
            specs = product.find_element_by_css_selector(".prod_spec_set dd").text
            specs = specs.split(" / ")

            if specs[0] == '외장 HDD':        # except 외장하드
                continue

            hdd._dict[hdd.colName[col_index]] = specs[0]; col_index+=1         # type
            hdd._dict[hdd.colName[col_index]] = specs[1]; col_index+=1         # size
            for spec in specs[2:]:

                for dist_index in range(col_index, len(hdd.colIdentifier)):

                    if hdd.colIdentifier[dist_index] in spec:
                        col_index = dist_index

                        if hdd.colName[col_index] == 'capacity':
                            num = spec[:-2]
                            unit = spec[-2:]
                            if unit == 'GB':
                                num = float(num) / 1000
                            hdd._dict[hdd.colName[col_index]] = num

                        elif hdd.colName[col_index] == 'sata':
                            hdd._dict[hdd.colName[col_index]] = spec.replace(" ","")

                        else:
                            info = ''.join(c for c in spec if c not in ' ,').replace(hdd.colIdentifier[dist_index],"")

                            while(info[-1].isalpha()):  # 단위 제거
                                info = info[:-1]

                            hdd._dict[hdd.colName[col_index]] = info
                        break

                    if dist_index == len(hdd.colIdentifier)-1:
                        spec = spec.replace(',', '')

                        if hdd._dict['etc'] == "NA":
                            hdd._dict['etc'] = spec
                        else:
                            hdd._dict['etc'] += " / " + spec


            price = product.find_element_by_css_selector(".prod_pricelist .price_sect strong").text
            hdd._dict[hdd.colName[-1]] = price.replace(",", "")

            # filter the data has no price
            if not hdd._dict[hdd.colName[-1]].isdigit():
                hdd._dict[hdd.colName[-1]] = 'NA'

            output.append(hdd._dict.values())
        return output

    def classifyMainboard(self, mainboard, products):
        """
        html tag List를 받아 제품 List를 반환
        :param products: html tag로 이루어진 여러 제품에 대한 정보 List
        :return output: 정제된 List
        """
        output = [] # list of row
        for product in products:
            mainboard.__init__()  # init dict

            if product == "":
                continue

            name = product.find_element_by_css_selector(".prod_name a").text
            name_split = name.split(" ")
            if name_split[-1] == "(중고)":
                continue

            mainboard._dict[mainboard.colName[0]] = name             # name
            mainboard._dict[mainboard.colName[1]] = name_split[0]    # manufacturer

            # specs is string sep by ' / '
            specs = product.find_element_by_css_selector(".prod_spec_set dd").text
            specs = specs.split(" / ")

            mainboard._dict[mainboard.colName[2]] = specs[0]         # socket
            mainboard._dict[mainboard.colName[3]] = specs[1]         # chipset

            col_index = 4  # mainboard.colName index (start from 'size')

            for spec in specs[2:]:

                dist_index = col_index - 4  # mainboard.colIdentifier index

                num = re.findall("[0-9]+", spec)

                for d_index in range(dist_index, len(mainboard.colIdentifier)):

                    if mainboard.colIdentifier[d_index] in spec:
                        col_index = d_index + 4

                        if mainboard.colName[col_index] in ('size', 'vga_connect', 'output'):
                            mainboard._dict[mainboard.colName[col_index]] = spec.replace(mainboard.colIdentifier[d_index], "")
                        elif not len(num):
                            mainboard._dict[mainboard.colName[col_index]] = spec
                        else:
                            mainboard._dict[mainboard.colName[col_index]] = num[-1]
                        break

                    if d_index == len(mainboard.colIdentifier)-1:
                        spec = spec.replace(',', '')

                        if mainboard._dict['etc'] == "NA":
                            mainboard._dict['etc'] = spec
                        else:
                            mainboard._dict['etc'] += " / " + spec


            price = product.find_element_by_css_selector(".prod_pricelist .price_sect strong").text
            mainboard._dict[mainboard.colName[-1]] = price.replace(",", "")

            # filter the data has no price
            if not mainboard._dict[mainboard.colName[-1]].isdigit():
                mainboard._dict[mainboard.colName[-1]] = 'NA'

            output.append(mainboard._dict.values())
        return output