from A01_create_tagged_file import create_tagged_files
from A02_generate_input_file import generate_input_file
from A03_translate_with_llm import translate_files
from A04_proof_read_with_llm import proof_read_files
from A05_tag_translated_sentence import tag_translated_files
from A06_tag_original_ja_text import tag_original_ja_text
from A99_create_colored_file import parse_generated_ja_en_pairs

def main():
    create_tagged_files()
    generate_input_file()
    translate_files()
    proof_read_files()
    tag_translated_files()
    parse_generated_ja_en_pairs()
    tag_original_ja_text()


if __name__ == "__main__":
    main()
