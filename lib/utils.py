import os
import re
import json
import datetime

from bs4 import BeautifulSoup
from collections import defaultdict
from setting import DEFAULT_LOG_LEVEL

import logging
logger = logging.getLogger(__name__)


def is_all_japanese(text):
    # Hiragana: U+3040 to U+309F
    # Katakana: U+30A0 to U+30FF
    # Kanji: U+4E00 to U+9FAF (CJK Unified Ideographs)    
    japanese_pattern = re.compile(r"^[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]+$")
    return bool(japanese_pattern.match(text))

def get_date_str():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")


def indent_json(json_str, indent=2, ensure_ascii=False):
    return json.dumps(json.loads(json_str), indent=indent, ensure_ascii=ensure_ascii)

def strip_md_block(txt, block_type="json"):
    if txt.startswith(f"```{block_type}"):
    # Strip the markdown code block
        txt = txt[7:-3]
        txt = txt.strip()
    return txt

def job_object_to_dict(job_object):
    return {
        "id": job_object.id,
        "seed": job_object.seed,
        "created_at": job_object.created_at,
        "status": job_object.status,
        "training_file": job_object.training_file,
        "validation_file": job_object.validation_file,
        "model": job_object.model,
        "fine_tuned_model": job_object.fine_tuned_model,
    }

def convert_backslash_to_slash(input_string):
    return input_string.replace("\\", "/")

def convert_slash_to_backslash(input_string):
    return input_string.replace("/", "\\")

def remove_target_type(input_string):
    """Remove the "type" attribute from the <target> tag in the input string.

    Args:
        input_string (str): The input string.
    """
    soup = BeautifulSoup(input_string, "html.parser")
    targets = soup.find_all("target")
    for target in targets:
        del target["type"]
    return str(soup)
    

def format_check(dataset):    
    # Format error checks
    format_errors = defaultdict(int)

    for ex in dataset:
        if not isinstance(ex, dict):
            format_errors["data_type"] += 1
            continue

        messages = ex.get("messages", None)
        if not messages:
            format_errors["missing_messages_list"] += 1
            continue

        for message in messages:
            if "role" not in message or "content" not in message:
                format_errors["message_missing_key"] += 1

            if any(k not in ("role", "content", "name") for k in message):
                format_errors["message_unrecognized_key"] += 1

            if message.get("role", None) not in ("system", "user", "assistant"):
                format_errors["unrecognized_role"] += 1

            content = message.get("content", None)
            if not content or not isinstance(content, str):
                format_errors["missing_content"] += 1

        if not any(message.get("role", None) == "assistant" for message in messages):
            format_errors["example_missing_assistant_message"] += 1
    return format_errors


# Yield successive n-sized 
# chunks from l. 
def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 


def setup_log(level=None, log_path='./log/txt', need_file=True):
    if not level:
        level = logging.getLevelName(DEFAULT_LOG_LEVEL)
    if not os.path.exists(log_path):
        os.makedirs(log_path)    
        
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(filename)s: %(message)s")
    
    handlers = []
    if need_file:
        filename = get_date_str()
        file_handler = logging.FileHandler("{0}/{1}.log".format(log_path, filename))
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(logging.DEBUG)
        handlers.append(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(level=level)
    handlers.append(console_handler)

    # https://stackoverflow.com/a/11111212
    logging.basicConfig(level=logging.DEBUG,
                        handlers=handlers)
