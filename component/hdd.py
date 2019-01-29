"""
HDD 제품 정보 처리
"""
import re

#===== column name list
col_list = ['name','manufacturer','type','size','capacity','sata','rpm','buffer',
            'thickness','noise','as','etc','price']
dist_list = ['','','','','TB','SATA3','RPM','메모리','두께:','소음(유휴/탐색):','년']
#===== ;

class Hdd:
    """
    Mainboard of computer parts

    Singleton Pattern
    refer to http://yamalab.tistory.com/74
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
        self._name = 'hdd'
        self._dict = {col: "NA" for col in col_list}

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
            if name_split[-1] == "(중고)":    # except 중고제품
                continue

            col_index = 0  # col_list index

            self._dict[col_list[col_index]] = name; col_index+=1             # name
            self._dict[col_list[col_index]] = name_split[0]; col_index+=1    # manufacturer

            # specs is string sep by ' / '
            specs = product.find_element_by_css_selector(".prod_spec_set dd").text
            specs = specs.split(" / ")

            if specs[0] == '외장 HDD':        # except 외장하드
                continue

            self._dict[col_list[col_index]] = specs[0]; col_index+=1         # type
            self._dict[col_list[col_index]] = specs[1]; col_index+=1         # size
            for spec in specs[2:]:

                # dist_index = col_index - 4  # dist_list index

                for dist_index in range(col_index, len(dist_list)):

                    if dist_list[dist_index] in spec:
                        col_index = dist_index

                        # if col_list[col_index] == 'sata':   #SATA3
                        #     self._dict[col_list[col_index]] = info.replace(" ", "")
                        #     break

                        info = ''.join(c for c in spec if c not in ' ,'+dist_list[dist_index])

                        word = re.findall("[0-9^]+", info)
                        info = info.replace(word[-1], "")

                        self._dict[col_list[col_index]] = info
                        break

                    if dist_index == len(dist_list)-1:
                        spec = spec.replace(',', '')

                        if self._dict['etc'] == "NA":
                            self._dict['etc'] = spec
                        else:
                            self._dict['etc'] += " / " + spec


            price = product.find_element_by_css_selector(".prod_pricelist .price_sect strong").text
            self._dict[col_list[-1]] = price.replace(",", "")

            # filter the data has no price
            if not self._dict[col_list[-1]].isdigit():
                self._dict[col_list[-1]] = 'NA'

            output.append(self._dict.values())
        return output