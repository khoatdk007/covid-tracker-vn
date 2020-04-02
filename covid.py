# -*- coding: utf-8 -*-
from sys import argv
import requests
import json
import sys
from texttable import Texttable
import urllib3
urllib3.disable_warnings()

provinces_code = {"HÀ NỘI": "01","HÀ GIANG": "02","CAO BẰNG": "04","BẮC KẠN": "06","TUYÊN QUANG": "08","LÀO CAI": "10","ĐIỆN BIÊN": "11","LAI CHÂU": "12","SƠN LA": "14","YÊN BÁI": "15","HOÀ BÌNH": "17","THÁI NGUYÊN": "19","LẠNG SƠN": "20","QUẢNG NINH": "22","BẮC GIANG": "24","PHÚ THỌ": "25","VĨNH PHÚC": "26","BẮC NINH": "27","HẢI DƯƠNG": "30","HẢI PHÒNG": "31","HƯNG YÊN": "33","THÁI BÌNH": "34","HÀ NAM": "35","NAM ĐỊNH": "36","NINH BÌNH": "37","THANH HÓA": "38","NGHỆ AN": "40","HÀ TĨNH": "42","QUẢNG BÌNH": "44","QUẢNG TRỊ": "45","THỪA THIÊN HUẾ": "46","ĐÀ NẴNG": "48","QUẢNG NAM": "49","QUẢNG NGÃI": "51","BÌNH ĐỊNH": "52","PHÚ YÊN": "54","KHÁNH HÒA": "56","NINH THUẬN": "58","BÌNH THUẬN": "60","KON TUM": "62","GIA LAI": "64","ĐẮK LẮK": "66","ĐẮK NÔNG": "67","LÂM ĐỒNG": "68","BÌNH PHƯỚC": "70","TÂY NINH": "72","BÌNH DƯƠNG": "74","ĐỒNG NAI": "75","BÀ RỊA - VŨNG TÀU": "77","HỒ CHÍ MINH": "79","LONG AN": "80","TIỀN GIANG": "82","BẾN TRE": "83","TRÀ VINH": "84","VĨNH LONG": "86","ĐỒNG THÁP": "87","AN GIANG": "89","KIÊN GIANG": "91","CẦN THƠ": "92","HẬU GIANG": "93","SÓC TRĂNG": "94","BẠC LIÊU": "95","CÀ MAU": "96"}
argv_input = argv
argv_input.pop(0)
input_province = ' '.join(argv_input).upper()

if len(input_province) == 0:
    url = 'https://ncov.moh.gov.vn/web/guest/trang-chu'
    x = requests.get(url, verify=False)
    covid_info_raw_string = x.text[(x.text.find('[{"name":"Ha Noi"') + 1):(x.text.find('success: function(data)') - 12)].replace('},{', '}|{').split('|')
    covid_info_dict = []
    for i in covid_info_raw_string:
        if 'bbb' in i or 'aaaaa' in i or '--' in i: #avoid having trash values
            continue 
        covid_info_dict.append(json.loads(i))

    table = Texttable()
    table.add_row(['Rank', 'Province/City', 'Total Cases', 'Total Deaths', 'Recovered', 'Active'])
    covid_info_dict = sorted(covid_info_dict, key = lambda i: int(i['soCaNhiem']), reverse = True)
    for i in range(1, len(covid_info_dict)):
        if int(covid_info_dict[i]['soCaNhiem']) == 0: continue
        table.add_row([i, list(provinces_code.keys())[list(provinces_code.values()).index(covid_info_dict[i]['ma'])], 
                        covid_info_dict[i]['soCaNhiem'], covid_info_dict[i]['tuVong'], covid_info_dict[i]['binhPhuc'],
                        int(covid_info_dict[i]['soCaNhiem']) - int(covid_info_dict[i]['binhPhuc']) - int(covid_info_dict[i]['tuVong'])])
    table.add_row(['', 'VIỆT NAM', covid_info_dict[0]['soCaNhiem'], covid_info_dict[0]['tuVong'], covid_info_dict[0]['binhPhuc'],
                        int(covid_info_dict[0]['soCaNhiem']) - int(covid_info_dict[0]['binhPhuc']) - int(covid_info_dict[0]['tuVong'])])
    print(table.draw())
elif not input_province in provinces_code:
    print("Province/City '{}' not found.".format(input_province))
    print("Please enter full province/city name!")
    exit()
else:
    url = 'https://ncov.moh.gov.vn/web/guest/trang-chu'
    x = requests.get(url, verify=False)

    covid_info_raw_string = x.text[(x.text.find('[{"name":"Ha Noi"') + 1):(x.text.find('success: function(data)') - 12)].replace('},{', '}|{').split('|')
    input_province_code = provinces_code[input_province]
    result = None
    vn_result = None
    for i in covid_info_raw_string:
        if 'bbb' in i or 'aaaaa' in i or '--' in i: #avoid having trash values
            continue 
        info = json.loads(i)
        if info['ma'] == input_province_code:
            result = info
        if info['ma'] == 'VNALL':
            vn_result = info
        if vn_result and result:
            break
        
    if result == None:
        table = Texttable()
        table.add_rows([['Province/City', 'Total Cases', 'Total Deaths', 'Recovered', 'Active'],
                        [input_province, 0, 0, 0, 0],
                        ['Việt Nam', vn_result['soCaNhiem'], vn_result['tuVong'], vn_result['binhPhuc'], int(vn_result['soCaNhiem']) - int(vn_result['binhPhuc']) - int(vn_result['tuVong'])]])
        print(table.draw())
    else:
        table = Texttable()
        table.add_rows([['Province/City', 'Total Cases', 'Total Deaths', 'Recovered', 'Active'],
                        [input_province, result['soCaNhiem'], result['tuVong'], result['binhPhuc'], int(result['soCaNhiem']) - int(result['binhPhuc']) - int(result['tuVong'])],
                        ['Việt Nam', vn_result['soCaNhiem'], vn_result['tuVong'], vn_result['binhPhuc'], int(vn_result['soCaNhiem']) - int(vn_result['binhPhuc']) - int(vn_result['tuVong'])]])
        print(table.draw())
