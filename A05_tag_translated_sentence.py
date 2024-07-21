from collections import defaultdict
import re
import json
from time import sleep
import pandas as pd
from lib.chat import run_model, models
from lib.io import read_data, write_data
from lib.tag_merge import merge_proof_reading_result
from lib.utils import indent_json, setup_log, strip_md_block
import setting

import logging

logger = logging.getLogger(__name__)

def tag_translated_files():

    # input_file = setting.test_result_filename
    # output_file = setting.test_result_filename_proof
    # output_file = output_file.replace(".xlsx", f".{use_model}.temp-{temperature}.xlsx")
    
    # input_file = setting.test_result_official_filename.format(model="sonnet", temp=1)
    
    input_file = setting.all_result_official_proof_filename
    output_file = setting.all_result_official_proof_tagged_filename
    
    df_in = read_data(input_file)

    for index, row in df_in.iterrows():
        # if index < 16:
            # continue
        try:
            ja_text = row["tagged"]
            raw_translation = row["raw_translation"]
            proof_reading = row["proof_reading"]

            print(f"Processing row [{index+1}/{len(df_in)}]: {ja_text[:50]}...")
            
            final_translation = merge_proof_reading_result(raw_translation, proof_reading)

            tagged_translation = add_xml_markup(final_translation["en_translation"], final_translation["targets"])
            df_in.at[index, f"tagged_translation"] = tagged_translation
            
        except Exception as e:
            print(f"Error processing row {index}: {e}")

    write_data(df_in, output_file)
    print("Done!")


def add_xml_markup(text, targets):
    """ Add XML markup to the text based on the targets. Replace all targets in the text. """
    # Sort targets by their order in the text to replace them in sequence
    # target_indices = [(m.start(), m.end(), target) 
    #                   for target in targets 
    #                   for m in re.finditer(f'\\b{target["en_element"]}\\b', text)]
    # target_indices.sort()
    
    def check_range_ok(start, end, pool):
        if len(pool) == 0:
            return ("append", -1)
        new_length = end - start
        for i, tuple in enumerate(pool):
            s, e, _ = tuple
            old_length  = e - s
            
            if new_length > old_length and start <= s and end >= e:
                # new element is longer than the old one and starts before the old one
                return ("replace", i)
            if new_length <= old_length and start >= s and end <= e:
                # new element is shorter or equal to the old one and is contained in the old one
                return ("skip", i)
        # no overlap
        return ("append", -1)
            
    target_indices = []
    for target in targets:
        en_element = target["en_element"]
        if en_element.lower() in ["", "n/a"]:
            # skip empty or N/A elements
            continue
        for m in re.finditer(f'\\b{en_element}\\b', text, flags=re.IGNORECASE):
            result = check_range_ok(m.start(), m.end(), target_indices)
            if result[0] == "replace":
                target_indices[result[1]] = (m.start(), m.end(), target)
            elif result[0] == "append":
                target_indices.append((m.start(), m.end(), target))
            else:
                print(f"==> Warning: Skipping target '{target['en_element']}' at [{m.start()},{m.end()}] because it is already covered.")
                pass
    target_indices.sort()
            
    # Replace from the end to maintain correct indices
    for start, end, target in reversed(target_indices):
        # en_element = target['en_element']
        original_text = text[start:end]
        markup = f'<target id="{target["id"]}" ref="{target["ref"]}" type="{target["type"]}" subtype="{target["subtype"]}">{original_text}</target>'
        text = text[:start] + markup + text[end:]
    
    return text


def add_xml_markup_old(text, targets):
    """ Add XML markup to the text based on the targets. Replace as many targets as possible in order. """
    same_en_elements_mapping = defaultdict(list)
    for target in targets:
        en_element = target['en_element']
        same_en_elements_mapping[en_element].append(target)
    
    # sort targets with the ref in each group

    for en_element, same_en_element_list in same_en_elements_mapping.items():
        matches = list(re.finditer(f'\\b{en_element}\\b', text))
        
        if len(matches) != len(same_en_element_list) and en_element.lower() != "n/a":
            print(f"==> Warning: Number of occurrences of '{en_element}' not match: text [{len(matches)}] <-> targets [{len(same_en_element_list)}].")
        
        count = min(len(matches), len(same_en_element_list))
        # Replace from the end to maintain correct indices
        for i in range(count-1, -1, -1):
            target = same_en_element_list[i]
            match = matches[i]
            start, end = match.start(), match.end()
            # Create the markup string for the current target
            markup = f'<target id="{target["id"]}" ref="{target["ref"]}" type="{target["type"]}" subtype="{target["subtype"]}">{en_element}</target>'
            text = text[:start] + markup + text[end:]
    
    return text

def test():
    data0 = {
        "en_translation": "'If we spread this message across Japan, similar initiatives might emerge somewhere,' says ○○○○. 'We hope to see such movements arise, and for that to happen, the athletes must really do their best.'",
        "targets": [
            {
                "id": "0",
                "ref": "0",
                "ja_element": "出",
                "en_element": "emerge",
                "type": "f",
                "subtype": "lt"
            },
            {
                "id": "0",
                "ref": "1",
                "ja_element": "出",
                "en_element": "arise",
                "type": "s",
                "subtype": "syn"
            }
        ]
    }
    
    data1 = {
        "en_translation": "This is a test and another test.",
        "targets": [
            {
                "id": "0",
                "ref": "0",
                "en_element": "test",
                "type": "f",
                "subtype": "lt"
            },
            {
                "id": "0",
                "ref": "1",
                "en_element": "test",
                "type": "s",
                "subtype": "syn"
            }
        ]
    }
    
    data2 = {
  "en_translation": "Seoul, January 24 (Jiji Press) -- A spokesperson for the South Korean presidential office on Wednesday welcomed Japanese Prime Minister Shinzo Abe's plan to visit South Korea during next month's PyeongChang Winter Olympics. || The spokesperson stated, 'We hope to work closely with the Japanese government to ensure that Prime Minister Abe's visit leads to the development of a future-oriented relationship between our two countries.'",
  "targets": [
    {
      "id": "0",
      "ref": "0",
      "ja_element": "韓",
      "en_element": "South Korea",
      "type": "f",
      "subtype": "lt"
    },
    {
      "id": "0",
      "ref": "1",
      "ja_element": "韓",
      "en_element": "visit",
      "type": "s",
      "subtype": "nlt"
    }
  ]
}
    
    data3 = {
  "en_translation": "Evacuation advisories and orders were issued to many residents in Hiroshima City and areas affected by heavy rains that occurred earlier this month.",
  "targets": [
    {
      "id": "0",
      "ref": "0",
      "ja_element": "避難",
      "en_element": "evacuation",
      "type": "f",
      "subtype": "lt"
    },
    {
      "id": "0",
      "ref": "1",
      "ja_element": "避難",
      "en_element": "N/A",
      "type": "r",
      "subtype": "el"
    }
  ]
}
    
    data = data3
    
    en_translation = data['en_translation']
    targets = data['targets']
    result = add_xml_markup(en_translation, targets)

    print(result)

    

if __name__ == "__main__":
    # setup_log()
    tag_translated_files()
    # test()
