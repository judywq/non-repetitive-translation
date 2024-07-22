from collections import defaultdict
import re
from bs4 import BeautifulSoup
from lib.io import read_data, write_data, write_text_file
from lib.tag_merge import merge_proof_reading_result
from lib.utils import convert_slash_to_backslash
import setting

import logging

logger = logging.getLogger(__name__)

def tag_original_ja_text():
    
    input_file = setting.all_result_official_proof_tagged_filename
    ja_output_file = setting.final_result_ja_tag_filename
    en_output_file = setting.final_result_en_trans_filename
    
    df_in = read_data(input_file)

    ja_tag_lines = []
    en_raw_lines = []
    for index, row in df_in.iterrows():
        # if index < 16:
            # continue
        try:
            ja_tagged = row["tagged"]
            is_tagged = row["is_tagged"]
            raw_translation = row["raw_translation"]
            proof_reading = row["proof_reading"]
            
            if is_tagged:
                # print(f"Processing row [{index+1}/{len(df_in)}]: {ja_tagged[:50]}...")
                final_translation = merge_proof_reading_result(raw_translation, proof_reading)
                en_targets = final_translation["targets"]
                ja_tagged_updated = tag_back_ja(ja_tagged, en_targets)
                ja_tagged_updated = remove_double_quotes_in_target(ja_tagged_updated)
                ja_tagged_updated = convert_slash_to_backslash(ja_tagged_updated)

                en_translation = final_translation["en_translation"]
            else:
                ja_tagged_updated = ja_tagged
                en_translation = raw_translation

            ja_tag_lines.append(ja_tagged_updated)
            en_raw_lines.append(en_translation)

        except Exception as e:
            print(f"Error processing row {index}: {e}")

    write_text_file("\n".join(ja_tag_lines), ja_output_file)
    write_text_file("\n".join(en_raw_lines), en_output_file)
    print("Done!")
    print(f"Japanese tagged file saved to: {ja_output_file}")
    print(f"English translation file saved to: {en_output_file}")

def remove_double_quotes_in_target(text):
    # Define a regular expression pattern to find <target> content
    target_pattern = re.compile(r'(<target[^>]*>)')

    def remove_quotes(match):
        content = match.group(1)
        
        # Remove double quotes from the content
        content = content.replace('"', '')

        return content

    # Substitute the matches with double quotes removed
    result = re.sub(target_pattern, remove_quotes, text)
    return result



def tag_back_ja(ja_tagged, en_targets):
    ja_soup = BeautifulSoup(ja_tagged, "html.parser")
    ja_targets = ja_soup.find_all("target")

    target_groups = defaultdict(list)
    first_non_f_type = None
    for target in en_targets:
        if target["type"] == "c":
            # Ignore consistent (c) type targets
            continue
        if target["type"] == "f" and not first_non_f_type:
            first_non_f_type = target["type"]
        target_groups[target["id"]].append(target)
    
    tmp = defaultdict(dict)
    for target_id, targets in target_groups.items():
        if len(targets) <= 1:
            # Skip if there is only one target
            continue
        for i, target in enumerate(targets):
            if target["type"] == "f":
                # set the type of first_occurence (f) to the first non f type
                target["type"] = first_non_f_type
            tmp[target["id"]][target["ref"]] = target
    
    for ja_target in ja_targets:
        en_target = tmp.get(ja_target["id"], {}).get(ja_target["ref"], {})
        if not en_target:
            ja_target.replaceWithChildren()
        else:
            ja_target["type"] = en_target["type"]
    
    return str(ja_soup)
    

def test():
    data0 = {
        "ja_tagged": "<target id=0 ref=0>朝鮮半島</target>情勢では、閣僚が4月の南北<target id=1 ref=0>首脳会談</target>と6月の米朝<target id=1 ref=1>首脳会談</target>に「歓迎」の意を表明し、<target id=0 ref=1>朝鮮半島</target>の非核化の実現へ取り組みを続けるよう求めている。",
        "targets": [
            {
            "id": "0",
            "ref": "0",
            "ja_element": "朝鮮半島",
            "en_element": "Korean Peninsula",
            "type": "f",
            "subtype": "lt"
            },
            {
            "id": "1",
            "ref": "0",
            "ja_element": "首脳会談",
            "en_element": "summit",
            "type": "f",
            "subtype": "lt"
            },
            {
            "id": "1",
            "ref": "1",
            "ja_element": "首脳会談",
            "en_element": "summit",
            "type": "c",
            "subtype": "lt"
            },
            {
            "id": "0",
            "ref": "1",
            "ja_element": "朝鮮半島",
            "en_element": "region",
            "type": "s",
            "subtype": "syn"
            }
        ]
    }
    
    data = data0
    
    ja_tagged = data['ja_tagged']
    targets = data['targets']
    result = tag_back_ja(ja_tagged, targets)
    print(result)

    

if __name__ == "__main__":
    tag_original_ja_text()
    # test()
