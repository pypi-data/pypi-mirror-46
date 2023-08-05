import sys

from . import utils


class An2Cn():
    def __init__(self):
        self.conf = utils.get_default_conf()
    
    def an2cn(self, input_data="defalut_key", is_cap=False):
        # 将数字转化为字符串
        if not isinstance(input_data, str):
            input_data = self.convert_number_to_string(input_data)

        # 检查数据是否有效
        self.check_input_data_is_valid(input_data)

        # 切割整数部分和小数部分
        split_result = input_data.split(".")
        len_split_result = len(split_result)
        if len_split_result == 1:
            # 不包含小数的输入
            integer_data = split_result[0]
            output = self.integer_convert(integer_data, is_cap)
        elif len_split_result == 2:
            # 包含小数的输入
            integer_data = split_result[0]
            decimal_data = split_result[1]
            output = self.integer_convert(integer_data, is_cap) + self.decimal_convert(decimal_data, is_cap)
        else:
            raise ValueError("输入格式错误：{}！".format(input_data))

        return output

    def an2cn_shell(self, input_data="defalut_key", is_cap=False):
        len_argv = len(sys.argv)
        if len_argv == 1:
            if input_data == "defalut_key":
                raise Exception("请在an2cn后输入需要转化的阿拉伯数字！")
            else:
                return input_data, is_cap
        elif len_argv == 2:
            input_an = sys.argv[1]
        elif len_argv == 3:
            input_an = sys.argv[1]
            if sys.argv[2] == "cap":
                is_cap = True
            else:
                raise Exception("参数2错误，如果你想使用大写功能，参数2应为cap！")
        else:
            raise Exception("an2cn后的参数过多！")

        return  self.an2cn(input_an, is_cap)

    @staticmethod
    def check_input_data_is_valid(check_data):
        # 检查输入数据是否在规定的字典中
        all_check_keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
        for data in check_data:
            if data not in all_check_keys:
                raise ValueError("输入的数据不在转化范围内：{}！".format(data))
    
    @staticmethod
    def convert_number_to_string(number_data):
        # python 会自动把 0.00005 转化成 5e-05，因此 str(0.00005) != "0.00005"
        string_data = str(number_data)
        if "e" in string_data:
            string_data_list = string_data.split("e")
            string_key = string_data_list[0]
            string_value = string_data_list[1]
            if string_value[0] == "-":
                string_data = "0." + "0"*(int(string_value[1:])-1) + string_key
            else:
                string_data = string_key + "0"*int(string_value)

        return string_data

    def integer_convert(self, integer_data, is_cap):
        if is_cap:
            numeral_list = self.conf["number_capital"]
            unit_list = self.conf["unit_capital"]
        else:
            numeral_list = self.conf["number"]
            unit_list = self.conf["unit"]

        # 去除前面的 0，比如 007 => 7
        integer_data = str(int(integer_data))

        len_integer_data = len(integer_data)
        
        if len_integer_data > len(unit_list):
            raise ValueError("超出数据范围，最长支持 16 位")

        output_an = ""
        for i, d in enumerate(integer_data):
            if int(d):
                output_an += numeral_list[int(d)] + unit_list[len_integer_data - i - 1]
            else:
                if not (len_integer_data - i - 1) % 4:
                    output_an += numeral_list[int(d)] + unit_list[len_integer_data - i - 1]
                
                if i > 0 and not output_an[-1] == "零":
                    output_an += numeral_list[int(d)]

        output_an = output_an.replace("零零", "零").replace("零万", "万").replace("零亿", "亿").replace("亿万", "亿").strip("零")

        # 解决「一十几」和「壹拾几」问题
        if output_an[:2] in ["一十", "壹拾"]:
            output_an = output_an[1:]
            
        # 0 - 1 之间的小数
        if not output_an:
            output_an = "零"
            
        return output_an


    def decimal_convert(self, decimal_data, is_cap):
        len_decimal_data = len(decimal_data) 

        if len_decimal_data > 15:
            print("warning: 小数部分长度为{}，超过15位有效精度长度，将自动截取前15位！".format(len_decimal_data))
            decimal_data = decimal_data[:15]

        if is_cap:
            numeral_list = self.conf["number_capital"]
        else:
            numeral_list = self.conf["number"]
        
        if len_decimal_data:
            output_an = "点"
        else:
            output_an = ""

        for data in decimal_data:
            output_an += numeral_list[int(data)]

        return output_an
