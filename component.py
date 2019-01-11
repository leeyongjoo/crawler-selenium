import re

#===== column name
v_col = ['name', 'type', 'nm', 'coreclock', 'b_coreclock', 'sp',
           'pcie_v1', 'pcie_v2', 'pcie_x', 'gddr', 'memoryclock', 'volume', 'bus']

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

            i = 1
            specs = product.find_element_by_css_selector(".prod_spec_set dd").text
            specs = specs.split(" / ")
            for spec in specs:
                k = re.findall("[a-zA-Z]+", spec)
                v = re.findall("[0-9]+", spec)

                if i == len(v_col): break
                if not len(v): continue
                else:
                    if len(v) == 1:
                        self.d[v_col[i]] = ''.join(v)
                        i += 1
                    else:
                        for a in v:
                            self.d[v_col[i]] = a
                            i+=1



            self.printData()

    def printData(self):
        print("name:" + self.d[v_col[0]])
        print(" - specs")
        for col in v_col[1:]:
            print("\t" + col + " : " + str(self.d[col]))