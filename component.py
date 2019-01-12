import re

#===== column name
v_col = ['name', 'manufacturer', 'type', 'prod', 'nm', 'clock', 'b_clock', 'sp',
           'PCIe', 'gddr', 'memory_c', 'memory_v', 'memory_b', 'etc']
v_dist = ['nm', '', '', '개', '', 'GDDR', 'MHz', 'GB', '-bit', '']
#==========

# VGA
class VGA:
    def __init__(self):
        self.d = {col:"NA" for col in v_col}

    def initData(self):
        self.d = {col:"NA" for col in v_col}

    def setData(self, products):

        for product in products:
            if product == "":
                continue

            self.d[v_col[0]] = product.find_element_by_css_selector(".prod_name a").text
            self.d[v_col[1]] = self.d[v_col[0]].split(" ")[0]
            self.d[v_col[2]] = 'vga'

            i = 3
            specs = product.find_element_by_css_selector(".prod_spec_set dd").text
            specs = specs.split(" / ")
            for spec in specs:


                if i == 3:
                    if spec.find(" ") != -1:
                        self.d[v_col[i]] = ''.join(spec.split(" ")[1:])
                    i += 1
                    continue

                word = re.findall("[^0-9]+", spec)
                num = re.findall("[0-9]+", spec)


                # 특정 형식
                if i == 5:  # 5:clock 6:b_clock
                    if len(num) > 1:
                        self.d[v_col[i]] = num[0]; i += 1
                        self.d[v_col[i]] = num[1]; i += 1
                    else:
                        if len(word) == 1:
                            self.d[v_col[i]] = num[0]
                        else:
                            self.d[v_col[i+1]] = num[0]
                        i += 2

                elif i == 8:    # 8:PCIe
                    if spec[:4] == "PCIe":
                        self.d[v_col[i]] = spec[4:]
                    i += 1



                elif i < len(v_col)-1:

                    if v_dist[i-4] != word[0]:
                        i += 1

                    elif len(num):
                        self.d[v_col[i]] = num[0]
                        i += 1

                elif i == len(v_col)-1:
                    if self.d[v_col[i]] == "NA":
                        self.d[v_col[i]] = spec
                    else:
                        self.d[v_col[i]] += " / " + spec

            self.printData()
            self.initData()


    def printData(self):
        print("- name : " + self.d[v_col[0]])
        for col in v_col[1:]:
            print(col + " : " + str(self.d[col]))