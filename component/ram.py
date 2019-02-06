"""
RAM 제품 정보 처리
"""
import re

#===== column name list
r_col = ['name', 'manufacturer', 'ddr', 'use', 'count', 'heatsink',
         'dimm', 'capacity', 'clock', 'etc', 'price']
r_dist = ['DDR', '용', 'ea', '포함', 'Dimm', 'GB', 'MHz']
#===== ;

class Ram:
    """
    Ram of computer parts
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
        self._name = 'ram'
        self._dict = {col: "NA" for col in r_col}

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
            # self._dict[r_col[0]] = pcode  # pcode
            self._dict[r_col[0]] = name             # name
            self._dict[r_col[1]] = name_split[0]    # manufacturer

            i = 2  # r_col index (start from 'ddr')

            # specs is string sep by ' / '
            specs = product.find_element_by_css_selector(".prod_spec_set dd").text
            specs = specs.split(" / ")
            for spec in specs:

                # r_col[i] == 'etc'
                if i == len(r_col) - 2:
                    spec = spec.replace(',', '')

                    if self._dict[r_col[i]] == "NA":
                        self._dict[r_col[i]] = spec
                    else:
                        self._dict[r_col[i]] += " / " + spec

                word = re.findall("[^0-9]+", spec)
                num = re.findall("[0-9]+", spec)

                # until r_col[i] == 'etc'
                while (i < len(r_col) - 2):
                    j = i-2

                    if not r_dist[j] in spec:
                        i += 1

                    elif len(num):
                        self._dict[r_col[i]] = spec.replace(r_dist[j], "").replace(",", "")
                        i += 1
                        break
                    else:
                        self._dict[r_col[i]] = spec
                        i += 1
                        break

            price = product.find_element_by_css_selector(".prod_pricelist .price_sect strong").text
            self._dict[r_col[-1]] = price.replace(",", "")

            # filter the data has no price
            if not self._dict[r_col[-1]].isdigit():
                self._dict[r_col[-1]] = 'NA'

            output.append(self._dict.values())
        return output