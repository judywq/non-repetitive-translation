from lib.io import read_data, write_data
import setting


def generate_input_file():
    input_file = setting.wat_ja_my_tagged
    output_file = setting.wat_index_ja_en
    
    df_in = read_data(input_file)
    if "Ja Tagged" in df_in.columns:
        df_in.drop(columns=["Ja Tagged"], inplace=True)
    df_in.rename(columns={"Ja Raw" : "raw", "Ja Tagged Merged": "tagged"}, inplace=True)
    
    write_data(df_in, output_file)
    print(f"Done! Output file: {output_file}")



if __name__ == "__main__":
    generate_input_file()
