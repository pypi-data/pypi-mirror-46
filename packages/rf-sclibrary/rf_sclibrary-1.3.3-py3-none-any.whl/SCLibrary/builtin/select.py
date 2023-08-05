# -*- coding:utf-8 -*-
from SCLibrary.base import keyword
from functools import reduce


class SelectKeywords(object):
    @keyword("SELECT ${properties} FROM ${array:[^(WHERE)]}")
    def select_array(self, properties, array):
        """ 返回符合条件的数组 """
        result = []
        if properties == '*':
            return array
        else:
            properties_arr = list(
                map(lambda x: x.strip(), properties.split(',')))
            for item in array:
                prop = {}
                for key in properties_arr:
                    if key in item:
                        prop[key] = item[key]
                    else:
                        prop[key] = None
                result.append(prop)
            return result

    @keyword("SELECTONE ${properties} FROM ${array:[^(WHERE)]}")
    def select_one_array(self, properties, array):
        """ 返回符合条件的第一条数据 """
        return self.select_array(properties, array)[0]

    def condition_parser(self, array, keywords):
        keyword = keywords.pop()

        def intersperse(array, item):
            result = [item] * (len(array) * 2 - 1)
            result[0::2] = array
            return result

        def flatmap(array):
            return reduce(list.__add__, array, [])

        new_array = flatmap(map(lambda item: intersperse(
            item, keyword), map(lambda item: item.split(keyword) if item not in ['!=', '>=', '<='] else [item], array)))
        if len(keywords) == 0:
            return list(filter(lambda item: item != '', new_array))
        else:
            return self.condition_parser(new_array, keywords)

    @keyword("SELECT ${properties} FROM ${array} WHERE ${conditions}")
    def select_array_where(self, properties, array, conditions):
        """ 返回符合条件的数组 """
        items = self.select_array(properties, array)
        keywords = ['>', '<', '=', 'AND', 'and', 'OR', 'or', '!=', '>=', '<=']
        condition_array = self.condition_parser(conditions.split(), keywords)
        operater = {
            '>': lambda x, y: str(x) > str(y),
            '<': lambda x, y: str(x) < str(y),
            '=': lambda x, y: str(x) == str(y),
            '!=': lambda x, y: str(x) != str(y),
            '>=': lambda x, y: str(x) >= str(y),
            '<=': lambda x, y: str(x) <= str(y),
        }

        def fn(item):
            result = True
            mode = 0
            name = None
            op = None
            logic = None
            for condition in condition_array:
                if condition in ['AND', 'and', 'OR', 'or']:
                    mode = 0
                    logic = condition
                elif mode == 0:
                    name = condition
                    mode += 1
                elif mode == 1:
                    op = condition
                    mode += 1
                elif mode == 2:
                    if logic in ['OR', 'or']:
                        if name in item:
                            result |= operater[op](item[name], condition)
                        else:
                            result |= False
                    else:
                        if name in item:
                            result &= operater[op](item[name], condition)
                        else:
                            result &= False
                    mode = 0
                    name = None
                    logic = None
                    op = None

            return result

        return list(filter(fn, items))

    @keyword("SELECTONE ${properties} FROM ${array} WHERE ${conditions}")
    def select_one_array_where(self, properties, array, conditions):
        """ 返回符合条件的第一条数据 """
        return self.select_array_where(properties, array, conditions)[0]
