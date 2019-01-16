import re
import csv

#===== column name
v_col = ['name', 'manufacturer', 'type', 'prod_name', 'nm', 'clock', 'b_clock', 'sp',
           'PCIe', 'gddr', 'memory_c', 'memory_v', 'memory_b', 'etc', 'price']
v_dist = ['nm', '', '', '개', '', 'GDDR', 'MHz', 'GB', '-bit', '']
#===== ;

# VGA
class VGA:
    def __init__(self):
        self.d = {col:"NA" for col in v_col}

    """
    param 
    param 
    desc
    """
    def preprocessListData(self, products):

        for product in products:
            if product == "":
                continue

            name = product.find_element_by_css_selector(".prod_name a").text
            name_split = name.split(" ")
            if name_split[-1] == "(중고)":
                continue

            self.d[v_col[0]] = name             # name
            self.d[v_col[1]] = name_split[0]    # manufacturer
            self.d[v_col[2]] = 'vga'            # type

            i = 3   # v_col index (start from 'prod_name')

            # string sep by '/'
            specs = product.find_element_by_css_selector(".prod_spec_set dd").text
            specs = specs.split(" / ")
            for spec in specs:

                # v_col[i] == 'etc'
                if i == len(v_col)-2:
                    if self.d[v_col[i]] == "NA":
                        self.d[v_col[i]] = spec
                    else:
                        self.d[v_col[i]] += " / " + spec

                word = re.findall("[^0-9]+", spec)
                num = re.findall("[0-9]+", spec)

                # until v_col[i] == 'etc'
                while(i < len(v_col)-2):

                    if not len(num):
                        i+=1
                        continue

                    if i == 3:  # 3: prod_name
                        if spec.find(" ") != -1:
                            self.d[v_col[i]] = ''.join(spec.split(" ")[1:])
                        i += 1
                        break

                    if i == 5:  # 5: clock , 6: b_clock
                        if len(num) > 1:
                            self.d[v_col[i]] = num[0]; i += 1
                            self.d[v_col[i]] = num[1]; i += 1
                            break
                        else:
                            if len(word) == 1:
                                self.d[v_col[i]] = num[0]
                            elif len(word) == 2:
                                self.d[v_col[i+1]] = num[0]
                            i += 2
                            break

                    if i == 8:    # 8: PCIe
                        if spec[:4] == "PCIe":
                            self.d[v_col[i]] = spec[4:]
                        i += 1
                        break

                    if v_dist[i-4] != word[0]:
                        i += 1

                    elif len(num):
                        self.d[v_col[i]] = num[0]
                        i += 1
                        break

            price = product.find_element_by_css_selector(".prod_pricelist .price_sect strong").text
            self.d[v_col[-1]] = price.replace(",", "")

            self.saveDataToCSV()
            self.d = {col: "NA" for col in v_col}   # init dict


    def printData(self):
        print("- name : " + self.d[v_col[0]])
        for col in v_col[1:]:
            print(col + " : " + str(self.d[col]))

    def saveDataToCSV(self):
        f = open('output.csv', 'a', encoding='utf-8', newline='')
        wr = csv.writer(f)

        col_list = []
        for col in v_col:
            col_list.append(self.d[col])

        wr.writerow(col_list)
        f.close()
