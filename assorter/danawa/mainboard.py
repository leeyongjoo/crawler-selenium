# -*- coding: utf-8 -*-
"""
MAINBOARD 제품 정보 처리
"""
import re

#===== column name list
col_list = ['name', 'manufacturer', 'socket', 'chipset', 'size', 'phase',
         'ddr', 'capacity', 'vga_connet', 'pcie_slot', 'sata3', 'm_2_slot',
         'output', 'ps_2', 'usb_2_0', 'usb_3_1_1', 'usb_3_1_2', 'etc', 'price']
dist_list = ['cm', '페이즈', 'DDR', 'GB', 'VGA 연결: ', 'PCIe 슬롯: ', 'SATA3: ',
         'M.2 슬롯: ', 'ch', 'PS/2: ', 'USB 2.0: ', 'USB 3.1 Gen 1: ', 'USB 3.1 Gen 2: ']
#===== ;

class Mainboard:
    """
    Mainboard of computer parts
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
        self._name = 'mainboard'
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
            if name_split[-1] == "(중고)":
                continue

            self._dict[col_list[0]] = name             # name
            self._dict[col_list[1]] = name_split[0]    # manufacturer

            # specs is string sep by ' / '
            specs = product.find_element_by_css_selector(".prod_spec_set dd").text
            specs = specs.split(" / ")

            self._dict[col_list[2]] = specs[0]         # socket
            self._dict[col_list[3]] = specs[1]         # chipset

            col_index = 4  # col_list index (start from 'size')

            for spec in specs[2:]:

                dist_index = col_index - 4  # dist_list index

                num = re.findall("[0-9]+", spec)

                for d_index in range(dist_index, len(dist_list)):

                    if dist_list[d_index] in spec:
                        col_index = d_index + 4

                        if col_list[col_index] in ('size', 'vga_connect', 'output'):
                            self._dict[col_list[col_index]] = spec.replace(dist_list[d_index], "")
                        elif not len(num):
                            self._dict[col_list[col_index]] = spec
                        else:
                            self._dict[col_list[col_index]] = num[-1]
                        break

                    if d_index == len(dist_list)-1:
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