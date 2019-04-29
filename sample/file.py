import os
import csv
from time import localtime,strftime

# file class
class File:
    """
    파일 생성,저장 메소드 관리
    """

    csv_path = './csv/'

    def __init__(self):
        pass

    def isExistPath(self, path):
        if os.path.exists(path):
            return True
        return False

    def isExistFile(self, file):
        if os.path.isfile(file):
            return True
        return False

    def generateDirPath(self, *dirs):
        path = "./"

        for d in dirs:
            if not self.isExistPath(d):
                os.mkdir(dir)
                path += dir + "/"

        return path

    def generateFileName(self, keyword):

    def saveKeywordListToCsv(self, keyword, data_list):
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




    # =====
