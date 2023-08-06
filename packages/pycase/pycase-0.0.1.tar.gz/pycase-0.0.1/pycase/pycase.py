# -*- coding: utf-8 -*-

# @Date    : 2019-05-26
# @Author  : Peng Shiyu

import argparse


def convert_upper(text):
    text = text.title()
    return text.replace("_", "")


def convert_lower(text):
    lst = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            lst.append("_")
        lst.append(char)

    return "".join(lst).lower()


def main():
    parser = argparse.ArgumentParser()

    # 定义参数
    parser.add_argument("-c", help="转换小写还是大写")
    parser.add_argument("-s", help="要转换的字符串")

    # 解析
    args = parser.parse_args()
    if args.c == "upper":
        print(convert_upper(args.s))
    elif args.c == "lower":
        print(convert_lower(args.s))
    else:
        print("参数不正确，-c 或者 -s")


if __name__ == '__main__':
    main()
