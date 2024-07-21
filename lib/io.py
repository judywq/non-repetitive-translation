from enum import Enum
import os
import pandas as pd
import json



def read_text_file(file_path):
    content = ""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content

def write_text_file(content, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def save_to_jsonl(dataset, file_path):
    path = os.path.dirname(file_path)
    if path:
        os.makedirs(path, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        for record in dataset:
            json_line = json.dumps(record)
            file.write(json_line + '\n')


def save_to_json(json_obj, file_path, indent=4):
    path = os.path.dirname(file_path)
    if path:
        os.makedirs(path, exist_ok=True)
    with open(file_path, 'w') as file:
        json.dump(json_obj, file, indent=indent)


def read_data(path, keep_default_na=False) -> pd.DataFrame:
    df = None
    _type = parse_file_type(path)
    if _type == FileType.CSV:
        df = pd.read_csv(path, keep_default_na=keep_default_na)
    elif _type == FileType.EXCEL:
        df = pd.read_excel(path, keep_default_na=keep_default_na)
    return df


def write_data(df: pd.DataFrame, filename: str):
    path = os.path.dirname(filename)
    if path:
        os.makedirs(path, exist_ok=True)
    _type = parse_file_type(filename)
    if _type == FileType.CSV:
        df.to_csv(filename, index=None)
    elif _type == FileType.EXCEL:
        df.to_excel(filename, index=None)


class FileType(Enum):
    CSV = 'csv'
    EXCEL = 'excel'
    
type_ext_map = {
    FileType.CSV: ['csv'],
    FileType.EXCEL: ['xls', 'xlsx'],
}

def parse_file_type(path):
    ext = (path.split('.')[-1]).lower()
    
    for _type, type_list in type_ext_map.items():
        if ext in type_list:
            return _type

    return None


################
# Test
################

def test_io():
    path = 'data/input/keywords.xlsx'
    df = read_data(path)
    print(df)
    
    out_path = 'data/output/test.xlsx'
    write_data(df, out_path)


if __name__ == '__main__':
    test_io()
    