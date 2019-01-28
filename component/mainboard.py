"""
MAINBOARD 제품 정보 처리
"""
import re

#===== column name list
m_col = ['name', 'manufacturer', 'socket', 'chipset', 'size', 'phase',
         'ddr', 'capacity', 'vga_connet', 'pcie_slot', 'sata3', 'm_2_slot',
         'ps_2', 'usb_2_0', 'usb_3_1_1', 'usb_3_1_2', 'etc', 'price']
m_dist = ['cm', '페이즈', 'DDR', 'GB', 'VGA 연결: ', 'PCIe 슬롯: ', 'SATA3: ',
          'M.2 슬롯: ', 'PS/2: ', 'USB 2.0: ', 'USB 3.1 Gen 1: ', 'USB 3.1 Gen 2: ']
#===== ;

class Mainboard:
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
        self._name = 'mainboard'
        self._dict = {col: "NA" for col in m_col}

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

            self._dict[m_col[0]] = name             # name
            self._dict[m_col[1]] = name_split[0]    # manufacturer

            # specs is string sep by ' / '
            specs = product.find_element_by_css_selector(".prod_spec_set dd").text
            specs = specs.split(" / ")

            self._dict[m_col[2]] = specs[0]         # socket
            self._dict[m_col[3]] = specs[1]         # chipset

            m_col_index = 4  # m_col index (start from 'size')

            for spec in specs[2:]:

                m_dist_index = m_col_index - 4  # m_dist index

                num = re.findall("[0-9]+", spec)

                for d_index in range(m_dist_index, len(m_dist)):

                    if m_dist[d_index] in spec:
                        m_col_index = d_index + 4

                        if m_col_index == 8: # 8: vga_connect
                            self._dict[m_col[m_col_index]] = spec.replace(m_dist[d_index], "")
                        else:
                            self._dict[m_col[m_col_index]] = num[-1]
                        break

                    if d_index == len(m_dist)-1:
                        spec = spec.replace(',', '')

                        if self._dict['etc'] == "NA":
                            self._dict['etc'] = spec
                        else:
                            self._dict['etc'] += " / " + spec


            price = product.find_element_by_css_selector(".prod_pricelist .price_sect strong").text
            self._dict[m_col[-1]] = price.replace(",", "")

            # filter the data has no price
            if not self._dict[m_col[-1]].isdigit():
                self._dict[m_col[-1]] = 'NA'

            output.append(self._dict.values())
        return output