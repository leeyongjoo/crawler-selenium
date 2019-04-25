# -*- coding: utf-8 -*-
"""
VGA 제품 정보 처리
"""
import re

#===== column name list
v_col = ['name', 'manufacturer', 'prod_name', 'nm', 'clock', 'b_clock',
         'sp', 'PCIe', 'gddr', 'memory_c', 'memory_v', 'memory_b', 'etc', 'price']
v_dist = ['nm', '', '', '개', '', 'GDDR', 'MHz', 'GB', '-bit', '']
#===== ;

class Vga:
    """
    VGA of computer parts
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
        self._name = 'vga'
        self._dict = {col: "NA" for col in v_col}

    def get_name(self):
        return self._name

    def handle_data_list(self, products):
        """
        html tag List를 받아 제품 List를 반환
        :param products: html tag로 이루어진 여러 제품에 대한 정보 List
        :return output: 정제된 List
        """
        output = [] # list of row
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
            # self._dict[v_col[0]] = pcode  # pcode
            self._dict[v_col[0]] = name             # name
            self._dict[v_col[1]] = name_split[0]    # manufacturer

            i = 2  # v_col index (start from 'prod_name')

            # specs is string sep by ' / '
            specs = product.find_element_by_css_selector(".prod_spec_set dd").text
            specs = specs.split(" / ")
            for spec in specs:

                # v_col[i] == 'etc'
                if i == len(v_col) - 2:
                    spec = spec.replace(',', '')

                    if self._dict[v_col[i]] == "NA":
                        self._dict[v_col[i]] = spec
                    else:
                        self._dict[v_col[i]] += " / " + spec

                word = re.findall("[^0-9]+", spec)
                num = re.findall("[0-9]+", spec)

                # until v_col[i] == 'etc'
                while (i < len(v_col) - 2):

                    if i == 2:  # 2: prod_name
                        if spec.find(" ") != -1:
                            self._dict[v_col[i]] = ''.join(spec.split(" ")[1:])
                        i += 1
                        break

                    if not len(num):
                        i += 1
                        continue

                    if i == 4:  # 4: clock , 5: b_clock
                        if len(num) > 1:
                            self._dict[v_col[i]] = num[0];
                            i += 1
                            self._dict[v_col[i]] = num[1];
                            i += 1
                            break
                        else:
                            if len(word) == 1:
                                self._dict[v_col[i]] = num[0]
                            elif len(word) == 2:
                                self._dict[v_col[i + 1]] = num[0]
                            i += 2
                            break

                    if i == 7:  # 7: PCIe
                        if spec[:4] == "PCIe":
                            self._dict[v_col[i]] = spec[4:]
                        i += 1
                        break

                    if v_dist[i - 3] != word[0]:
                        i += 1

                    elif len(num):
                        self._dict[v_col[i]] = num[0]
                        i += 1
                        break

            price = product.find_element_by_css_selector(".prod_pricelist .price_sect strong").text
            self._dict[v_col[-1]] = price.replace(",", "")

            # filter the data has no price
            if not self._dict[v_col[-1]].isdigit():
                self._dict[v_col[-1]] = 'NA'

            output.append(self._dict.values())
        return output