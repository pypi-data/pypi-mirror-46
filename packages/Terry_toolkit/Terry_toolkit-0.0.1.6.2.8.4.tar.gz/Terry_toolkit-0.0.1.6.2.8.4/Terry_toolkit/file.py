# -*- coding: utf-8 -*-
# 对文件进行预处理
import os



class File:
    def __init__(self):
        pass
    # 遍历目录文件夹
    def file_List(self, path, type='txt'):
        """
        遍历目录文件夹

        >>> file_List('/home/','txt')


        """
        files = []
        for file in os.listdir(path):

            if file.endswith("." + type):
                print(path+file)
                files.append(path+file)
        return files
    #打开文件
    def open_file(self, file):
        """

        多编码兼容打开文件

        >>> open_file('a.txt'):
        """
        print('open_file',file)
        if os.path.isfile(file):
            print('open_file 存在',file)
            try:
                fileObj = open(file, encoding='utf-8').read()  # 读入文件
                print('utf8',file)
            except:
                fileObj = open(file, encoding='gbk').read()  # 读入文件
                print('尝试gbk打开',file)
            print('open_file 成功',file)
            return fileObj
        else:
            print('open_file 失败',file)
            return False
    # 清理多余的换行空格等
    def clear(self, string):
        """Summary of class here.

        Longer class information....
        Longer class information....

        Attributes:
            likes_spam: A boolean indicating if we like SPAM or not.
            eggs: An integer count of the eggs we have laid.
        """

        # return string.strip()
        # for line in string.readlines():
        # string = re.sub('[\n]+', '\n', string)
        string = string.replace('\n', '').replace(
            '\n\n', '\n').replace('\r\n', '\n').replace('   ', '\n')
        # string = string.replace('\n\n', ' ').replace('\n', '')
        string = re.sub(' +', ' ', string)
        return string
