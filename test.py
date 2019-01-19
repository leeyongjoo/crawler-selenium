import numpy as np
import pandas as pd

v_col = ['name', 'manufacturer', 'prod_name', 'nm', 'clock', 'b_clock',
         'sp', 'PCIe', 'gddr', 'memory_c', 'memory_v', 'memory_b', 'etc', 'price']

data = pd.read_csv('./csv/vga/vga_190119_2326.csv', names=v_col)
