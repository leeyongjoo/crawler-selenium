import os
import csv
from time import localtime,strftime

csv_path = './csv/'

class File:
    """
    파일 생성,저장 메소드 관리
    """
    def __init__(self, path, fileName):
        self.fpath_fname = None

    def create_csv(self, c_name, col_list=None):
        """
        component 이름과 현재시각을 파일명으로 하는 CSV 파일 생성
        :param c_name: component name
        :param col_list: column names list
        :return:
        """
        if not os.path.exists(csv_path):
            os.mkdir(csv_path)

        fpath = csv_path + c_name + "/"
        fname = c_name + strftime("_%y%m%d_%H%M.csv", localtime())
        self.fpath_fname = fpath + fname

        if not os.path.exists(fpath):
            os.mkdir(fpath)

        # create csv and save col_names to csv
        f = open(self.fpath_fname, 'w', encoding='utf-8', newline='')
        # wr = csv.writer(f)
        # wr.writerow(col_list)
        f.close()

    def save_list_to_csv(self, data_list):
        """
        data_list 내용을 만들어둔 파일에 저장
        :param data_list: data list
        :return:
        """
        # save data to csv
        f = open(self.fpath_fname, 'a', encoding='utf-8', newline='')
        wr = csv.writer(f)
        for row in data_list:
            wr.writerow(row)
        f.close()

    #===========================================04.25
    def saveListToCSV(self, data_list):
        """
        data_list 내용을 만들어둔 파일에 저장
        :param data_list: data list
        :return:
        """
        # save data to csv
        f = open(self.fpath_fname, 'a', encoding='utf-8', newline='')
        wr = csv.writer(f)
        for row in data_list:
            wr.writerow(row)
        f.close()