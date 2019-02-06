"""
CPU 제품 정보 처리
"""
import re

#===== column name list
c_col = ['name', 'manufacturer', 'socket', 'nm', 'core', 'thread', 'clock',
         'l2', 'l3', 'bit', 'tdp', 'gpu_name', 'gpu_core', 'etc', 'price']
c_dist = ['', 'nm', '코어', '개', 'GHz', 'B', 'B', '비트', 'W',
          ['인텔', 'AMD'], 'MHz']
#===== ;

class Cpu:
    """
    CPU of computer parts
    """
    _instance = None

    @classmethod
    def _get_instance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._get_instance
        return cls._instance

    def __init__(self):
        self._name = 'cpu'
        self._dict = {col: "NA" for col in c_col}

    def get_name(self):
        return self._name

    def handle_data_list(self, products):
        """
        html tag List를 받아 제품 List를 반환
        :param products: html tag로 이루어진 여러 제품에 대한 정보 List
        :return output: 정제된 List
        """
        output = []  # list of row
        for product in products:
            self.__init__()  # init dict

            if product == "":
                continue

            name = product.find_element_by_css_selector(".prod_name a").text
            name_split = name.split(" ")
            if name_split[-1] == "(중고)":
                continue

            # pcode = product.find_element_by_css_selector(".relation_goods_unit").get_attribute('id')
            # pcode = re.findall("[0-9]+", pcode)[0]
            #
            # self._dict[c_col[0]] = pcode            # pcode
            self._dict[c_col[0]] = name             # name
            self._dict[c_col[1]] = name_split[0]    # manufacturer

            i = 2  # c_col index (start from 'prod_name')

            # specs is string sep by ' / '
            specs = product.find_element_by_css_selector(".prod_spec_set dd").text
            specs = specs.split(" / ")
            for spec in specs:

                # c_col[i] == 'etc'
                if i == len(c_col) - 2:
                    spec = spec.replace(',', '')

                    if self._dict[c_col[i]] == "NA":
                        self._dict[c_col[i]] = spec
                    else:
                        self._dict[c_col[i]] += " / " + spec

                word = re.findall("[^0-9]+", spec)
                num = re.findall("[0-9]+", spec)

                # until c_col[i] == 'etc'
                while (i < len(c_col) - 2):

                    j = i - 2  # c_dist index

                    if i == 2:  # 2: socket
                        s_split = spec.split("(")
                        if self._dict[c_col[1]] == s_split[0]:
                            self._dict[c_col[i]] = s_split[1].replace(")", "")
                        i += 1
                        break

                    if i == 4:  # 4: core
                        if spec[-2:] == c_dist[j]:
                            self._dict[c_col[i]] = spec[:2]
                            i+=1
                            break

                    if i == 6:  # 6: clock
                        if word[-1].replace(" ", "") == c_dist[j]:
                            self._dict[c_col[i]] = spec.replace(c_dist[j], "").replace(" ", "")
                            i+=1
                            break

                    if i == 7:  # 7: l2
                        if word[-1][-1] == 'B':
                            if word[-1][-2] == 'M':
                                self._dict[c_col[i+1]] = int(num[0]) * 1024
                            elif  word[-1][-2] == 'K':
                                self._dict[c_col[i + 1]] = num[0]
                            i+=1
                            break
                        elif word[-1][-1] == 'x':
                            if word[-1][0] == 'M':
                                self._dict[c_col[i+1]] = int(num[0]) * int(num[1]) * 1024
                            elif  word[-1][0] == 'K':
                                self._dict[c_col[i+1]] = int(num[0]) * int(num[1])
                            i+=1
                            break
                    if i == 8:  # 8: l3
                        if word[0][-1] == 'B':
                            self._dict[c_col[i-1]] = self._dict[c_col[i]]
                            self._dict[c_col[i]] = int(num[0]) * 1024
                            i+=1
                            break

                    if i == 9: # 9: bit
                        if spec[-2:] == c_dist[j]:
                            self._dict[c_col[i]] = spec[:-2]
                            i+=1
                            break

                    if i == 11: # 11: gpu_name
                        if spec.split(" ")[0] in c_dist[j]:
                            self._dict[c_col[i]] = spec
                            i+=1
                            break

                    if c_dist[j] != word[-1]:
                        i += 1

                    elif len(num):
                        self._dict[c_col[i]] = num[0]
                        i += 1
                        break

            price = product.find_element_by_css_selector(".prod_pricelist .price_sect strong").text
            self._dict[c_col[-1]] = price.replace(",", "")

            # filter the data has no price
            if not self._dict[c_col[-1]].isdigit():
                self._dict[c_col[-1]] = 'NA'

            output.append(self._dict.values())
        return output