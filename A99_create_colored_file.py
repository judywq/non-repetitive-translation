import pandas as pd
from bs4 import BeautifulSoup
from lib.io import read_data
from lib.utils import convert_backslash_to_slash
import setting


def main():
    # parse_official_ja_en_files()
    # parse_my_tagged_problematic_file()
    # parse_my_tagged_file()
    parse_generated_ja_en_pairs()


def parse_official_ja_en_files():
    ja_file = setting.wat_tagged_ja
    en_file = setting.wat_tagged_en
    output_file = setting.wat_ja_en_official_color
    color_file_pair(ja_file, en_file, output_file)
    print(f"Output saved to: {output_file}")
    

def parse_generated_ja_en_pairs():
    input_file = setting.all_result_official_proof_tagged_filename
    output_file = setting.all_result_official_proof_tagged_annotate_filename
    
    df = read_data(input_file)
    ja_lines = df["tagged"].to_list()
    en_lines = df["tagged_translation"].to_list()
    color_file_pair(ja_lines, en_lines, output_file)
    print(f"Output saved to: {output_file}")
    
    
def parse_my_tagged_problematic_file():
    input_file = setting.wat_ja_my_tagged_problematic
    output_file = setting.wat_ja_my_tagged_problematic_color
    df = read_data(input_file)
    lines = df["Ja Tagged Merged"].to_list()
    color_single_file(lines, output_file)
    print(f"Output saved to: {output_file}")    


def parse_my_tagged_file():
    input_file = setting.wat_ja_my_tagged
    output_file = setting.wat_ja_my_tagged_color
    df = read_data(input_file)
    lines = df["Ja Tagged Merged"].to_list()
    color_single_file(lines, output_file)
    print(f"Output saved to: {output_file}")    


def color_single_file(input_file, output_file):
    output_file = output_file

    df_src = _process_file(input_file)
    # Rename the columns to avoid conflicts when merging
    df_src = df_src.rename(
        columns={
            "Raw text": "Japanese text",
            "Cleaned text": "Cleaned Japanese text",
            "Target tokens": "Japanese tokens",
            # "Tag ref": "Japanese ref",
            "Type": "Japanese type",
            "highlights": "src_highlight",
        }
    )

    # Sort the columns
    df_src = df_src[
        [
            "Sentence ID",
            "Japanese text",
            # "English text",
            "Cleaned Japanese text",
            # "Cleaned English text",
            "Tag ID",
            "Tag ref",
            "Japanese tokens",
            # "English tokens",
            "Japanese type",
            # "English type",
            "src_highlight",
            # "dest_highlight",
        ]
    ]

    highlight_info = [
        {
            "text_column": "Cleaned Japanese text",
            "highlight_column": "src_highlight",
        },
    ]

    save_to_excel(df_src, output_file, highlight_info)


def color_file_pair(src_file, dest_file, output_file):
    output_file = output_file

    df_src = _process_file(src_file)
    # Rename the columns to avoid conflicts when merging
    df_src = df_src.rename(
        columns={
            "Raw text": "Japanese text",
            "Cleaned text": "Cleaned Japanese text",
            "Target tokens": "Japanese tokens",
            # "Tag ref": "Japanese ref",
            "Type": "Japanese type",
            "highlights": "src_highlight",
        }
    )

    df_dest = _process_file(dest_file)
    # Rename the columns to avoid conflicts when merging
    df_dest = df_dest.rename(
        columns={
            "Raw text": "English text",
            "Cleaned text": "Cleaned English text",
            "Target tokens": "English tokens",
            # "Tag ref": "English ref",
            "Type": "English type",
            "highlights": "dest_highlight",
        }
    )

    df_merged = pd.merge(
        df_src, df_dest, on=["Sentence ID", "Tag ID", "Tag ref"], how="outer"
    )
    df_merged.fillna("N/A", inplace=True)

    # Sort the columns
    df_merged = df_merged[
        [
            "Sentence ID",
            "Japanese text",
            "English text",
            "Cleaned Japanese text",
            "Cleaned English text",
            "Tag ID",
            "Tag ref",
            "Japanese tokens",
            "English tokens",
            "Japanese type",
            "English type",
            "src_highlight",
            "dest_highlight",
        ]
    ]

    highlight_info = [
        {
            "text_column": "Cleaned Japanese text",
            "highlight_column": "src_highlight",
        },
        {
            "text_column": "Cleaned English text",
            "highlight_column": "dest_highlight",
        },
    ]

    save_to_excel(df_merged, output_file, highlight_info)


def parse_pair(src, dest, sentence_id):
    src_data = parse_line(
        src, sentence_id, "Japanese text", "Target tokens", "src_highlight"
    )
    dest_data = parse_line(
        dest, sentence_id, "English text", "Translated tokens", "dest_highlight"
    )
    return (src_data, dest_data)


def parse_line(line, sentence_id):
    # Initialize a list to hold the extracted information
    extracted_info = []

    soup = BeautifulSoup(line, "html.parser")
    targets = soup.find_all("target")
    
    if len(targets) == 0:
        extracted_info.append({
                "Sentence ID": sentence_id,
                "Raw text": line,
                "Cleaned text": line,
                "Tag ID": -1,
                "Target tokens": "N/A",
                "Tag ref": -1,
                "Type": "N/A",
                "highlights": "",
            })
        return extracted_info

    # Get the cleaned text without tags
    # cleaned_text = soup.text

    cleaned_text = str(soup)
    positions = []

    for target in targets:
        tag_id = target.get("id")
        target_text = target.text

        # Get the cleaned text without tags
        start_index = cleaned_text.find(str(target))
        end_index = start_index + len(target_text)
        pos = f"{tag_id}@{start_index}:{end_index}"
        positions.append(pos)
        # Replace the first occurrence of the markup with the plain text
        cleaned_text = cleaned_text.replace(str(target), target_text, 1)

    to_highlight = ",".join(positions)

    for target in targets:
        tag_id = target.get("id")
        tag_ref = target.get("ref")
        tag_type = target.get("type")
        target_text = target.text

        extracted_info.append(
            {
                "Sentence ID": sentence_id,
                "Raw text": line,
                "Cleaned text": cleaned_text,
                "Tag ID": tag_id,
                "Target tokens": target_text,
                "Tag ref": tag_ref,
                "Type": tag_type,
                "highlights": to_highlight,
            }
        )

    return extracted_info


def _process_file(file_path_or_lines):
    if isinstance(file_path_or_lines, str):
        with open(file_path_or_lines, "r", encoding="utf-8") as file:
            content = convert_backslash_to_slash(file.read())
            lines = content.split("\n")
    else:
        lines = file_path_or_lines

    all_extracted_info = []

    for line_no, line in enumerate(lines):
        sentence_id = line_no + 1
        extracted_info = parse_line(line=line, sentence_id=sentence_id)
        all_extracted_info.extend(extracted_info)
        # break

    df = pd.DataFrame(all_extracted_info)
    return df


def save_to_excel(df, output_path, highlight_info):

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(output_path, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="Output")

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    # https://www.excelsupersite.com/what-are-the-56-colorindex-colors-in-excel/
    red_font = workbook.add_format({"bold": True, "font_color": "red"})
    blue_font = workbook.add_format({"bold": True, "font_color": "blue"})
    green_font = workbook.add_format({"bold": True, "font_color": "green"})
    magenta_font = workbook.add_format({"bold": True, "font_color": "magenta"})
    brown_font = workbook.add_format({"bold": True, "font_color": "brown"})
    # cyan_font = workbook.add_format({"bold": True, "font_color": "cyan"})
    lime_font = workbook.add_format({"bold": True, "font_color": "lime"})
    navy_font = workbook.add_format({"bold": True, "font_color": "navy"})
    yellow_font = workbook.add_format({"bold": True, "font_color": "#FF9900"})
    dark_blue_font = workbook.add_format({"bold": True, "font_color": "#33CCCC"})
    light_green_color = workbook.add_format({"bold": True, "font_color": "#99CC00"})
    highlight_fonts = [
        red_font,
        blue_font,
        green_font,
        magenta_font,
        brown_font,
        light_green_color,
        dark_blue_font,
        navy_font,
        lime_font,
        yellow_font,
    ]
    worksheet = writer.sheets["Output"]

    # Iterate through the DataFrame and write the cleaned text with formatting
    for index, row in df.iterrows():
        pandas_row = index + 1  # Pandas index starts from 0, Excel from 1

        for info in highlight_info:
            text_column = info["text_column"]
            highlight_column = info["highlight_column"]
            cleaned_text = row[text_column]
            highlight = row[highlight_column]
            pandas_column = df.columns.get_loc(
                text_column
            )  # Convert column name to column index

            highlight_parts(
                worksheet,
                pandas_row,
                pandas_column,
                cleaned_text,
                highlight,
                highlight_fonts,
            )

    writer.close()


def highlight_parts(worksheet, row, col, content, positions, highlight_fonts):
    """
    Highlights designated parts of a cell's text with red color.

    Parameters:
    - worksheet: the worksheet to work on
    - row: the row number of the cell
    - col: the column number of the cell
    - content: a string to write into the cell
    - positions: a string specifying ranges to highlight, in the format "tag_id@xx:xx,tag_id@xx:xx"
    - highlight_fonts: a list of format object to apply to the highlighted parts
    """
    if not positions or pd.isna(positions) or not ":" in positions:
        # worksheet.write(row, col, content)
        return
    # Parse the positions
    highlights = []
    position_list = positions.split(",")
    for pos in position_list:
        tag_id, range = pos.split("@")
        start, end = range.split(":")
        highlights.append((int(tag_id), int(start), int(end)))
    # highlights = [
    #     (int(tag_id), int(start), int(end)) for tag_id, range in (pos.split("@") for pos in position_list)
    # ]

    # Start building the rich string
    rich_string = []

    last_end = 0
    for tag_id, start, end in highlights:
        # Append text before the highlighted part
        if last_end < start:
            rich_string.append(content[last_end:start])

        highlight_font = highlight_fonts[tag_id % len(highlight_fonts)]
        # Append the highlighted part
        rich_string.append(highlight_font)
        rich_string.append(content[start:end])  # do not include the character at 'end'

        last_end = end

    # Append any remaining text after the last highlighted part
    if last_end < len(content):
        rich_string.append(content[last_end:])

    # Write the rich string to the cell
    worksheet.write_rich_string(row, col, *rich_string)


def test_parse_line():
    sent = """The National Police Agency noted that while the overall number of <target id="0" ref="1" type="s" subtype="syn">scams</target> has decreased due to a significant reduction in refund <target id="0" ref="0" type="f" subtype="lt">fraud</target>, 'It's me' <target id="0" ref="1" type="s" subtype="syn">scams</target> are on the rise, indicating the situation remains extremely serious."
    """
    sent_id = 0
    
    result = parse_line(sent, sent_id)
    print(result)

if __name__ == "__main__":
    main()
    # test_parse_line()