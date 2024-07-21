import json
import os
from time import sleep
import pandas as pd
from lib.chat import run_model, models
from lib.io import read_data, write_data
from lib.rerun import get_rerun_index_list
from lib.utils import indent_json, setup_log, strip_md_block
import setting

import logging

logger = logging.getLogger(__name__)

# use_model = "gpt4o"
use_model = "sonnet"
temperature = 1

IS_RERUN = False
# IS_RERUN = True


def proof_read_files():
    system_message = setting.system_message_proof_reader_langchain

    # input_file = setting.all_result_official_filename
    input_file = setting.all_result_official_filename
    output_file = setting.all_result_official_proof_filename
    
    df_src = read_data(input_file)
    
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
            if "proof_reading" in row and row["proof_reading"]:
                # print(f"Row {index} already proof read. Skipping...")
                continue
        # if index < 21:
        # continue
        try:
            ja_text = row["tagged"]
            
            raw_translation = row["raw_translation"]
            is_tagged = row["is_tagged"]
            # HACK: use the df_src instead
            # raw_translation = df_src.at[index, "raw_translation"]
            print(f"Processing row [{index+1}/{len(df_in)}]: {ja_text[:50]}...")
            
            if not is_tagged:
                df_in.at[index, f"proof_reading"] = raw_translation
            else:
                json_dict = json.loads(raw_translation)
                json_dict["ja_text"] = ja_text
                user_message = json.dumps(json_dict, ensure_ascii=False)

                proof_read_response = run_model(use_model, system_message, user_message, temperature)
                proof_read_response = strip_md_block(proof_read_response)
                print(f"Proof read response: {proof_read_response[:50]}")
                df_in.at[index, f"proof_reading"] = proof_read_response
                
                indented_raw_response = indent_json(raw_translation)
                df_in.at[index, "raw_translation"] = indented_raw_response

            # Save progress after each row
            if index % 10 == 0:  # Save every 10 rows to reduce frequent I/O operations
                print(f"Saving progress at row {index}")
                write_data(df_in, output_file)
        except Exception as e:
            print(f"Error processing row {index}: {e}")

        if index % 60 == 0:
            sleep(10)

    write_data(df_in, output_file)
    print("Done!")



if __name__ == "__main__":
    # setup_log()
    proof_read_files()
