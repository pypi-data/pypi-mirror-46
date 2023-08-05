import csv
import os
from pprint import pprint


class Csv:
    """
        用于对csv格式的文件的加载, 生成, 打印.

        example
        -------
        读取
        c = Csv()
        c.load('data1.csv')
        c.print_list()
        输出如下:
        [['name', 'age', 'sex'],
         ['japan', '20', 'man'],
         ['taibei', '103', 'femail'],
         ['russia', '43', 'man']]

        也可以:
        c = Csv(data1.csv)

        生成一个csv的文件:
        data = [['name', 'age', 'sex'],
                ['japan', '20', 'man'],
                ['taibei', '103', 'femail'],
                ['russia', '43', 'man']]
        c = Csv()
        c.make(data, filename='name1.csv')

        将会在本地目录下生成一个name1.csv的文件, 内容为data中的内容
        """
    def __init__(self, file=None):
        self.rowNum = 0
        self.colNum = 0
        self.data = list()
        if file:
            if not os.path.isfile(file):
                raise FileNotFoundError('文件{}不存在'.format(file))
            else:
                self.load(file)

    def load(self, file: str):
        """'
        file:   str, 表示要加载的文件
        """
        if not os.path.isfile(file):
            raise FileNotFoundError('文件不存在或不是文件')

        if not file.endswith('.csv'):
            raise TypeError('文件格式不正确, 必须以.csv结尾')

        with open(file, 'r') as f:
            self.data = list(csv.reader(f))
            self.rowNum = len(self.data)
            self.colNum = len(self.data[0])

        print(f'文件{file}加载完毕～')

    def make(self, data, filename='name1.csv'):
        """生成一个excel文件"""
        if not filename.endswith('.csv'):
            raise TypeError(f'{filename}格式不对,不是以csv结尾')
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f)
            # for _list in data:
            #     csv_writer.writerow(_list)
            csv_writer.writerows(data)

    def __str__(self):
        return str(vars(self))

    def print_list(self):
        pprint(self.data)
