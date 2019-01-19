"""
CPU 제품 정보 처리
"""
import re

#===== column name list
c_vol = ['socket', 'nm', 'core', 'thread', 'clock', 'l2', 'l3', 'bit', 'tdp',
         'gpu_name', 'gpu_core']
c_dist = [['인텔', 'AMD'], 'nm', '코어', '개','GHz', 'MB', '', '비트', 'W',
          ['인텔', 'AMD'], 'MHz']
#===== ;

class Cpu:
    pass