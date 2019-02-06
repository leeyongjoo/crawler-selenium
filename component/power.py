"""
POWER 제품 정보 처리
"""

import re
#===== column name list
col_list = ['name','manufacturer','standard','w','fan_size','fan_num','pfc','rail',
            'a','4pin_ide','sata','6+2pin_pci-e','as','etc','price']
dist_list = ['','','파워', 'W', 'mm 팬', '개(팬)', 'PFC', '+12V',
	        'A', '4핀 IDE', 'SATA', '6+2핀 PCI-E','무상']
#===== ;

class Power:
    """
    Power of computer parts
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
        self._name = 'power'
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

            if not dist_list[col_index] in specs[0]:
                continue

            # self._dict[col_list[col_index]] = specs[0]; col_index+=1         # standard
            # self._dict[col_list[col_index]] = specs[1]; col_index+=1         # w
            # for spec in specs[2:]:
            for spec in specs:

                for dist_index in range(col_index, len(dist_list)):

                    if dist_list[dist_index] in spec:
                        col_index = dist_index

                        info = spec.replace(dist_list[dist_index], "")
                        info = info.replace(" ", "")

                        if col_index in (3, 8,9,10,11,12):
                            self._dict[col_list[col_index]] = re.findall("[0-9]+", info)[0]
                        else:
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