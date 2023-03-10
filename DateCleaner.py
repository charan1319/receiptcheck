from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import os
import datetime
import ocr_parser
from calendar import month_name

# userData = pd.read_csv('Bill.com/Users.csv')



def get_current_format(date_str, current_formats):
    # print("IN FUNCTION")
    flag = False
    current_format = None
    # print("STRING IN GET FORMAT", date_str)

    for format in current_formats:
        try:
            flag = bool(datetime.datetime.strptime(date_str, format))
            if flag:
                current_format = format
                return current_format
        except ValueError:
            continue    

    # for format in current_formats:
    #     # print("CHECKING FORMAT", format)
    #     try:
    #         # print("SHEEEE", format)
    #         # print(date_str, format)
    #         # if date_str:
    #         flag = bool(datetime.datetime.strptime(date_str, format))
    #         print("CHECKING FORMAT", format)
    #         print("flag", flag)
    #         if flag:
    #             current_format = format
    #             print("IN FUNCTION", current_format)
    #             return current_format
    #     except ValueError:    
    #         print("NAH", format)
    #         # print("got here", format)
    #         # continue

def convert_to_format(date_str, current_format, required_format):
    if current_format:
        reformatted_string = datetime.datetime.strptime(date_str, current_format).strftime(required_format)
        ans = reformatted_string.replace("-0","-")
        return ans
        
        

def get_reformatted_strings():
    required_format_1 = '%Y-%m-%d'
    required_format_2 = '%Y-%d-%m'
    current_formats = {'%d-%m-%y', '%d-%m-%Y', '%d-%b-%y', '%d-%B-%y', '%d-%b-%Y', '%d-%B-%Y', '%d-%^b-%y', '%d-%^B-%y', '%d-%^b-%Y', '%d-%^B-%Y', '%d/%m/%y', '%d/%m/%Y', '%d/%b/%y', '%d/%B/%y', '%d/%b/%Y', '%d/%B/%Y', '%d/%^b/%y', '%d/%^B/%y', '%d/%^b/%Y', '%d/%^B/%Y', '%d %m %y', '%d %m %Y', '%d %b %y', '%d %B %y', '%d %b %Y', '%d %B %Y', '%d %^b %y', '%d %^B %y', '%d %^b %Y', '%d %^B %Y'}
    dir = 'Bill.com/ocr/'

    parsed_ocr_dict = ocr_parser.parse_files()
    # print("LENGTH", len(parsed_ocr_dict))
    # document_id_list = []
    mapping = dict()
    # for name in os.listdir(dir):
    for name in parsed_ocr_dict.keys():
        # if name.endswith(".csv"):
        converted_string_list = []
        # stripped_name = name.replace('.csv','')
        OCR_CSV = parsed_ocr_dict[name]
        # OCR_CSV = pd.read_csv(dir + '/' + name, names=["x1","y1","x2","y2","x3","y3","x4","y4","TEXT"], engine='python', on_bad_lines='skip')

        OCR_CSV_STRING = OCR_CSV.to_string()
        numeric_re = '\d{2}[,\s/-]\d{2}[,\s/-]\d+'
        alphanumeric_re_1 = '\s(Jan|JAN|Feb|FEB|Mar|MAR|Apr|APR|May|MAY|Jun|JUN|Jul|JUL|Aug|AUG|Sep|SEP|Oct|OCT|Nov|NOV|Dec|DEC)[a-zA-Z.,-]*[,\s/-]?(\d{1,2})?[,\s/-]?\d+'
        alphanumeric_re_2 = '\s(\d{1,2})?[,\s/-]?(Jan|JAN|Feb|FEB|Mar|MAR|Apr|APR|May|MAY|Jun|JUN|Jul|JUL|Aug|AUG|Sep|SEP|Oct|OCT|Nov|NOV|Dec|DEC)[a-zA-Z.,-]*[,\s/-]?\d+'
        reg = numeric_re + '|' + alphanumeric_re_1 + '|' + alphanumeric_re_2

        dates = re.search(reg, OCR_CSV_STRING)
        # print("MAIN EXTRACTED DATE", dates)
        if dates:
            date_str = dates.group(0)
            # print("FILE", name)
            # print("EXTRACTED DATE", dates.group(0))
            # print("ENTERING FUNCTION")
            current_format = get_current_format(date_str, current_formats)
            # print("EXITING FUNCTION")
            # print("CURRENT FORMAT", current_format)
            # YYYY-MM-DD
            converted_string_1 = convert_to_format(date_str, current_format, required_format_1)
            # YYYY-DD-MM
            converted_string_2 = convert_to_format(date_str, current_format, required_format_2)
            # print("CONVERTED DATE", converted_string)
            # print(converted_string)
            # document_id_list.append(stripped_name)
            converted_string_list.append(converted_string_1)
            converted_string_list.append(converted_string_2)
            mapping[name] = converted_string_list
        else:
            date_str = None
            mapping[name] = date_str    
    # print(mapping)
    # return document_id_list, converted_string_list
    # print(len(mapping))                
    return mapping

# print(get_reformatted_strings())
# document_id_list, converted_string_list = get_reformatted_strings()
# mapping = get_reformatted_strings()
def create_pd_df(mapping):
    d = {'Document ID': [k for k in mapping.keys()], 'Dates': [v for v in mapping.values()]}
    # df = pd.DataFrame(mapping)
    # # nested_list = [document_id_list, converted_string_list]
    # # print(len(nested_list))
    # d = {'Document ID': document_id_list, 'Converted Date': converted_string_list}
    # df = pd.DataFrame(data=d)
    # df.to_csv('dates.csv', encoding='utf-8', index=False)
    # return df
    df = pd.DataFrame.from_dict(data=d)
    # df.to_csv('new_formatted.csv', encoding='utf-8', index=False)
    return df
# print(create_pd_df(document_id_list, converted_string_list))
# print(get_reformatted_strings())
# print(create_pd_df(mapping))