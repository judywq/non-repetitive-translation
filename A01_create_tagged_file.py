import json
import re
from typing import List
import MeCab
from collections import defaultdict

import pandas as pd
from tenacity import retry, stop_after_attempt
from A99_create_colored_file import color_single_file
from lib.chat import run_model
from lib.io import read_data, read_text_file, write_data
from lib.utils import is_all_japanese, strip_md_block
from lib.tag_merge import merge_word_sequences, update_word_id_and_ref, view_word_list
import setting


class MyWord:
    def __init__(self, surface, pos_tag, lemma):
        self.surface = surface
        self.pos_tag = pos_tag
        self.pos_detail1 = ""
        self.pos_detail2 = ""
        self.pos_detail3 = ""
        self.lemma = lemma
        self.id = -1
        self.ref = -1
        self.prev = None
        self.next = None
        self.sig_dict = {}

    def __str__(self):
        return f"{self.surface} <{self.lemma}, {self.pos_tag}, {self.pos_detail1}, {self.pos_detail2}, {self.pos_detail3}, id:{self.id}, ref:{self.ref}>"

    def __repr__(self):
        return self.__str__()

    def format(self):
        if self.is_repetitive():
            return f"<target id={self.id} ref={self.ref}>{self.surface}</target>"
        else:
            return self.surface

    def clear(self):
        self.id = -1
        self.ref = -1
        self.surface = ""

    def is_repetitive(self):
        return self.id >= 0

    def is_valid_candidate(self):
        return (
            self.surface_ok
            and self.pos_ok
            and self.lemma_ok
            and self.suffix_ok
            and self.prefix_ok
        )

    @property
    def surface_ok(self):
        surface_blacklist = [
            # ("年", "名詞", "接尾", "助数詞"),
            # ("月", "名詞", "接尾", "助数詞"),
            ("月", "名詞", "一般"),
            # ("日", "名詞", "接尾", "助数詞"),
            ]

        def match(w, record: tuple):
            sig = "_".join(record)
            word_sig = "_".join(
                [w.surface, w.pos_tag, w.pos_detail1, w.pos_detail2, w.pos_detail3]
            )
            return word_sig.startswith(sig)

        for record in surface_blacklist:
            if match(self, record):
                return False
            
        return is_all_japanese(self.surface)

    @property
    def lemma_ok(self):
        lemma_blacklist = ["する", "ない"]
        return self.lemma not in lemma_blacklist

    @property
    def pos_ok(self):
        pos_whitelist = [
            ("副詞", "一般"),
            ("動詞", "自立"),
            # ("動詞", "接尾"),
            # ("名詞", "接尾", "一般"),
            ("名詞", "接尾", "形容動詞語幹"),
            ("名詞", "接尾", "人名"),
            ("名詞", "接尾", "地域"),
            ("名詞", "接尾", "特殊"),
            ("名詞", "非自立", "副詞可能"),
            ("名詞", "サ変接続"),
            ("名詞", "ナイ形容詞語幹"),
            ("名詞", "一般"),
            ("名詞", "固有名詞"),
            ("名詞", "副詞可能"),
            ("名詞", "形容動詞語幹"),
            ("形容詞", "自立"),
            ("接頭詞", "名詞接続"),
        ]

        def match(w, record: tuple):
            sig = "_".join(record)
            word_sig = "_".join(
                [w.pos_tag, w.pos_detail1, w.pos_detail2, w.pos_detail3]
            )
            return word_sig.startswith(sig)

        for record in pos_whitelist:
            if match(self, record):
                return True
        return False

    # TODO: refactor these two methods
    @property
    def suffix_ok(self):
        # Always return True for now, do not check suffix
        return True
        if self.is_suffix:
            if not self.prev:
                # A suffix must be preceded by a word
                return False
            #  Remove this word itself from the list of words with the same signature
            same_sig_words = list(
                filter(lambda x: x != self, self.sig_dict[self.signature])
            )
            for other in same_sig_words:
                if not other.prev:
                    continue
                if (
                    other.prev.is_valid_candidate()
                    and self.prev.is_valid_candidate()
                    and other.prev.lemma == self.prev.lemma
                ):
                    return True
            return False
        return True

    @property
    def prefix_ok(self):
        if self.is_prefix:
            if not self.next:
                # A prefix must be followed by a word
                return False
            #  Remove this word itself from the list of words with the same signature
            same_sig_words = list(
                filter(lambda x: x != self, self.sig_dict[self.signature])
            )
            for other in same_sig_words:
                if not other.next:
                    continue
                if (
                    other.next.is_valid_candidate()
                    and self.next.is_valid_candidate()
                    and other.next.lemma == self.next.lemma
                ):
                    return True
            return False
        return True

    @property
    def is_prefix(self):
        return self.pos_tag == "接頭詞"

    @property
    def is_suffix(self):
        return self.pos_detail1 == "接尾"

    # @property
    # def signature(self):
    #     if self.lemma == "*":
    #         return f"{self.surface}_{self.pos_tag}_{self.pos_detail1}"
    #     return f"{self.lemma}_{self.pos_tag}_{self.pos_detail1}"

    @property
    def signature(self):
        if self.lemma == "*":
            return self.surface
        return self.lemma


def convert_to_word_list(text):
    word_list = generate_word_list_with_mecab(text)
    if setting.ENABLE_LLM_TAGGING:
        any_repetitive = any(map(lambda x: x.is_repetitive(), word_list))    
        if not any_repetitive:
            print(f"No tags found, use llm: {text[:50]}")
            # No repetitive words found, use llm
            try:
                tmp = generate_word_list_with_llm(text)
            except Exception as e:
                print(f"Error tagging with llm: {e}")
                tmp = None
            if tmp:
                word_list = tmp

    return word_list

# https://www.geeksforgeeks.org/python-program-to-split-a-string-by-the-given-list-of-strings/
def split_text_with_delimiters(text, delimiters):
    temp = re.split(rf"({'|'.join(delimiters)})", text)
    result = [ele for ele in temp if ele] 
    return result


@retry(stop=stop_after_attempt(3))
def generate_word_list_with_llm(text):
    use_model = "sonnet"
    system_message = setting.system_message_tagging_ja_langchain
    temperature = 1
    user_message = text
    
    response = run_model(use_model, system_message, user_message, temperature)
    response = strip_md_block(response)
    json_object = json.loads(response)
    targets = json_object["targets"]
    if len(targets) == 0:
        raise Exception("No targets found")
    target_tokens = [t["target_token"] for t in targets]
    surface_to_id = {t["target_token"]: int(t["id"]) for t in targets}
    words = split_text_with_delimiters(text, target_tokens)
    word_list = []
    for i, surface in enumerate(words):
        w = MyWord(surface=surface, pos_tag="", lemma="")
        w.id = surface_to_id.get(surface, -1)
        word_list.append(w)
    word_list = update_word_id_and_ref(word_list)
    return word_list


def generate_word_list_with_mecab(text):
    # Initialize MeCab
    mecab = MeCab.Tagger("-Ochasen")

    # Parse the text and tokenize
    node = mecab.parseToNode(text)

    # Dictionary to store signature occurrences
    sig_dict = defaultdict(list)
    processed_sigs = []
    family_id = 0
    word_list: List[MyWord] = []

    while node:
        surface = node.surface
        if surface:
            # 表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
            features = node.feature.split(",")
            pos_tag = features[0]
            pos_detail1 = features[1]
            pos_detail2 = features[2]
            pos_detail3 = features[3]
            lemma = features[6]

            w = MyWord(surface=surface, pos_tag=pos_tag, lemma=lemma)
            w.pos_detail1 = pos_detail1
            w.pos_detail2 = pos_detail2
            w.pos_detail3 = pos_detail3
            w.sig_dict = sig_dict
            if word_list:
                w.prev = word_list[-1]
                word_list[-1].next = w

            sig_dict[w.signature].append(w)
            word_list.append(w)
        node = node.next

    family_id = 0
    for w in word_list:
        # print(w)
        if not w.is_valid_candidate():
            w.id = -1
            continue
        if w.signature in processed_sigs:
            continue
        valid_words = list(
            filter(lambda x: x.is_valid_candidate(), sig_dict[w.signature])
        )
        valid_count = len(valid_words)
        if valid_count > 1:
            for tmp_w in valid_words:
                tmp_w.id = family_id
                # print(f"Repetitive word: {tmp_w}")
            family_id += 1
        # del sig_dict[w.signature]
        processed_sigs.append(w.signature)

    # view_word_list(word_list)
    word_list = update_word_id_and_ref(word_list)
    return word_list


def format_tagged_text(word_list):
    result_list = []
    for w in word_list:
        result_list.append(w.format())
    return "".join(result_list)


def tag_repetitive_words(text):
    return format_tagged_text(convert_to_word_list(text))

def strip_header(text):
    delimiter = "--"
    header = ""
    if delimiter in text:
        # split by the first delimiter
        header = text.split(delimiter)[0]
        header += delimiter
        # remove the header
        text = text.replace(header, "")
    return (header, text)


def process_file(input_file, tag_output_file, color_output_file, color_output_file_merged, filter_index=None):
    lines = list(filter(lambda x: x, read_text_file(input_file).split("\n")))
    if filter_index:
        # get only problematic sentences
        lines = [lines[i] for i in filter_index]
    header_list, text_list = list(zip(*map(strip_header, lines)))
    list_of_word_list = list(map(convert_to_word_list, text_list))
    tagged_lines = list(map(format_tagged_text, list_of_word_list))
    # tagged_lines = list(map(tag_repetitive_words, lines))
    
    # Merge back the headers
    assert len(header_list) == len(tagged_lines)
    tagged_lines = [f"{header_list[i]}{tagged_lines[i]}" for i in range(len(header_list))]

    list_of_merged_word_list = list(map(merge_word_sequences, list_of_word_list))
    tagged_lines_merged = list(map(format_tagged_text, list_of_merged_word_list))
    
    # Merge back the headers
    assert len(header_list) == len(tagged_lines_merged)
    tagged_lines_merged = [f"{header_list[i]}{tagged_lines_merged[i]}" for i in range(len(header_list))]

    df = pd.DataFrame(
        {
            "Ja Raw": lines,
            "Ja Tagged": tagged_lines,
            "Ja Tagged Merged": tagged_lines_merged,
        }
    )
    write_data(df, tag_output_file)
    print(f"Tagged file is saved to {tag_output_file}")

    df = read_data(tag_output_file)
    lines = df["Ja Tagged"].to_list()
    color_single_file(lines, color_output_file)
    print(f"Colored file saved to: {color_output_file}")

    lines = df["Ja Tagged Merged"].to_list()
    color_single_file(lines, color_output_file_merged)
    print(f"Colored file (merged) saved to: {color_output_file_merged}")


def create_tagged_files():
    input_file = setting.wat_raw_ja
    tag_output_file = setting.wat_ja_my_tagged
    color_output_file = setting.wat_ja_my_tagged_color
    color_output_file_merged = setting.wat_ja_my_tagged_color_merged
    process_file(input_file, tag_output_file, color_output_file, color_output_file_merged)


def check_problematic():
    problem_sent_ids = [
        33,
        37,
        45,
        51,
        80,
        83,
        108,
        112,
        126,
        212,
        215,
        326,
        332,
        367,
        427,
    ]
    problem_index = [i - 1 for i in problem_sent_ids]
    
    input_file = setting.wat_raw_ja
    tag_output_file = setting.wat_ja_my_tagged_problematic
    color_output_file = setting.wat_ja_my_tagged_problematic_color
    color_output_file_merged = setting.wat_ja_my_tagged_problematic_color_merged
    
    process_file(input_file, tag_output_file, color_output_file, color_output_file_merged, problem_index)
  

def test_one():
    # Example usage
    text = "ソウル、1月24日（時事通信）--韓国大統領府報道官は水曜日、日本の安倍晋三首相が来月の平昌冬季五輪に合わせて訪韓する計画であることに対して歓迎の意を示した。 || 報道官は、「われわれは、安倍首相の訪韓が二国間の未来志向的な関係の発展につながるよう日本政府と緊密に協力していくことを望んでいる」と発言した。"
    # text = "この減少は、米国債の金利上昇により日本政府が保有する債券の時価評価額が減少した結果である。 || さらに、対ドルでユーロ安が進み、政府保有のユーロ建て資産のドル換算額が減少した。"
    # text = "「昔から鉄道で旅をしていた || 。思い出をたどりながら、新幹線中心の旅をしたいと思った」と妻と一緒にツアーに参加した〇〇〇〇さん（70）は語った。"
    # text = "一方、10.7%が日本に「その危険はない」と考えているか、「どちらかといえばその危険がない」と思っていると話した。"
    # text =  "〇〇〇〇さんは「米国とその人々の能力は素晴らしいが、それを人を死なせることには使ってほしくない」と呼び掛けた。 || 〇〇〇〇さんは「米国の能力を平和を実現するために使ってほしい」と強調した。"
    # text = "飲食を認めない喫煙室でのみ喫煙を認める。"
    # text = "回答した104人のうち26人が「ストーカー行為をしていると思っていない」と回答した。"
    # text = "だが民間調査機関インテージによると、缶酎ハイ市場ではアルコール度数7～9%の製品のシェアが2017年に缶酎ハイ市場の50%強を占め、7年間で2.5倍に拡大した。"
    # text = "多くの自治体が寄付者に返礼品を贈っており、人々は豪華な返礼品を目当てに寄付を行っている。"
    # text = "民進党の小西洋之氏は、小野寺氏に辞任を要求。||小野寺氏は「（調査に）厳正に対応していきたい」と述べ、辞任を否定した。"
    # text = "外国パック旅行費は、日本人旅行者の人気旅行先の台湾での宿泊費が上がったことを受けて、11.7%上昇した。"
    # text = "JEMAの担当者は白物家電について、「機能を絞った低価格製品、高価格な高機能製品とも好調だ」と述べている。"
    # text = "〇〇〇〇さんは同組織に拘束されているとみられる。||同組織は、日本政府などに〇〇〇〇さんの解放交渉を求める狙いがあるとみられる。"
    # text = "考案者は国文学、漢文学、日本史学、東洋史学などの学者とみられる。"
    text = "日ロは2016年の首脳会談で、18年を日ロの交流年に指定した。1月24日, 1月24日"
    text = "福井、8月25日（時事通信）--政府は土曜日、関西電力の大飯原発と高浜原発（いずれも中部地方福井県）で重大事故が起きたと想定し、総合防災訓練を行った。"
    text = "専門家の1人は、鑑定した110個の遺骨の中で日本人のDNA型は5個、フィリピン人の型が54個だったと報告。"
    text = "金曜日早朝、親王ご夫妻はワルシャワ大や同国の旧市街、旧王宮をそれぞれ視察。"

    header, text = strip_header(text)
    word_list = convert_to_word_list(text)
    tagged_text = header + format_tagged_text(word_list)
    word_list_merged = merge_word_sequences(word_list)

    tagged_text_merged = header + format_tagged_text(word_list_merged)
    print(tagged_text)
    print(tagged_text_merged)


def test_split():
    text = "ソウル、1月24日（時事通信）--韓国大統領府報道官は水曜日、日本の安倍晋三首相が来月の平昌冬季五輪に合わせて訪韓する計画であることに対して歓迎の意を示した。 || 報道官は、「われわれは、安倍首相の訪韓が二国間の未来志向的な関係の発展につながるよう日本政府と緊密に協力していくことを望んでいる」と発言した。"
    delimiters = ["韓国", "日"]
    result = split_text_with_delimiters(text, delimiters)
    print(result)


if __name__ == "__main__":
    create_tagged_files()
    # check_problematic()
    # test_one()
    # test_split()
