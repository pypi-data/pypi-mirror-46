# -*- coding: UTF-8 -*-
class Property:
    properties = {}

    def __init__(self, arg):
        if isinstance(arg, str):
            self.get_from_file(arg)
        else:
            self.get_from_json(arg)

    def get_from_json(self, json_val):
        self.properties = dict(json_val)

    def get_from_file(self, file_path):
        try:
            config = open(file_path, 'r')
            for line in config:
                if line.find('=') > 0:
                    strs = line.replace('\n', '').split('=')
                    key, value = strs[0], strs[1]
                    self.properties[key] = value
                else:
                    raise Exception('config file format error')
        except Exception as e:
            print('配置文件读取出现问题')
            raise e
        else:
            config.close()

    def get_property(self, key):
        return self.properties[key]
