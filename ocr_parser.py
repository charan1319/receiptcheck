import os
import pandas as pd
import numpy as np

def parse_files(ocr_directory_path="Bill.com/ocr/"):
    ocr_filenames = set()
    for name in os.listdir(ocr_directory_path):
        if name.endswith(".csv"):
            ocr_filenames.add(name)

    ocr_columns = ["x1","y1","x2","y2","x3","y3","x4","y4","TEXT"]
    ocr_parsed = {}
    for filename in ocr_filenames:
        cur_ocr = [[] for i in range(9)]
        with open(f"{ocr_directory_path}{filename}") as csv_file:
            for line in csv_file:
                for idx, num in enumerate(line[:-1].split(',', 8)):
                    cur_ocr[idx].append(num)

        for i in range(8):
            cur_ocr[i] = np.asarray(cur_ocr[i], dtype=float)

        df = pd.DataFrame(data={col: cur_data_col for col, cur_data_col in zip(ocr_columns, cur_ocr)})
        ocr_parsed[filename[:-4]] = df
    return ocr_parsed