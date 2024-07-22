import json
import os
from time import sleep
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from lib.chat import run_model
from lib.io import read_data, write_data
from lib.rerun import get_rerun_index_list
from lib.utils import strip_md_block
import setting

# use_model = "gpt4o"
use_model = "sonnet"
temperature = 1
system_message_tagged = setting.system_message_translate_tagged_langchain
system_message_non_tagged = setting.system_message_translate_non_tagged

IS_RERUN = False
# IS_RERUN = True


def check_tag(text):
    return "target" in text


def _translate(input_file, output_file, input_col='input', output_col='raw_translation'):

    if os.path.exists(output_file):
        print(f"Output file already exists: {output_file}")
        df_in = read_data(output_file)
    else:
        df_in = read_data(input_file)
    
    if IS_RERUN:
        rerun_index_list = get_rerun_index_list()
        print(f"Rerun with {len(rerun_index_list)} items...")

    for index, row in df_in.iterrows():
        if IS_RERUN:
            # Is rerun, then check if the row is in the rerun list
            if index not in rerun_index_list:
                print(f"Row {index} not in rerun list. Skipping...")
                continue
        else:
            # Not a rerun, then check if the output column is already filled
            if output_col in row and row[output_col]:
                # print(f"Row {index} already translated. Skipping...")
                continue
        try:
            ja_text = row[input_col]
            is_tagged = check_tag(ja_text)
            user_message = ja_text
            print(f"Translating row [{index+1}/{len(df_in)}]: {user_message[:50]}...")
            if is_tagged:
                response = run_model(use_model, system_message_tagged, user_message, temperature)
            else:
                response = run_model(use_model, system_message_non_tagged, user_message, temperature)

            response = strip_md_block(response)
            df_in.at[index, output_col] = response
            df_in.at[index, "is_tagged"] = is_tagged

            # Save progress after each row
            if index % 10 == 0:  # Save every 10 rows to reduce frequent I/O operations
                print(f"Saving progress at row {index}")
                write_data(df_in, output_file)
        except Exception as e:
            print(f"Error processing row {index}: {e}")

        if (index + 1) % 60 == 0:
            sleep(10)

    write_data(df_in, output_file)
    print("Done!")    

def translate_files():    
    # system_message = setting.system_message_short

    # input_file = setting.index_test_filename
    # output_file = setting.test_result_official_filename.format(model=use_model, temp=temperature)
    input_file = setting.wat_index_ja_en
    output_file = setting.all_result_official_filename
    
    _translate(input_file, output_file, input_col='tagged')


if __name__ == "__main__":
    translate_files()
