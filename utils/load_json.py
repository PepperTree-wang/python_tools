#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/23 13:37
# @Author  : Wang Zixv
# @Site    : 
# @File    : load_json.py
# @Software: PyCharm

import json

json_path = "E:\\TEMP\\haixin\\distsnce_result_test_20220222\\tube_dif_result_path\\result.txt"

with open(json_path,"r") as f:
    json = json.loads(f.read())
print(json)
for j in json:
    print(j["bias"])

j = 20
for i in range(j):
    print(i)
