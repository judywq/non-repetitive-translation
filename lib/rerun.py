import setting
from lib.io import read_data

def get_rerun_index_list():
    df = read_data(setting.all_result_rerun_filename)
    # get rows that "rerun" is not empty
    df = df[df["rerun"].astype(bool)]
    # get the "Sentence ID" column and convert it to a list
    rerun_index_list = list(set(df["Sentence ID"].apply(lambda x: x-1).tolist()))
    rerun_index_list.sort()
    return rerun_index_list
