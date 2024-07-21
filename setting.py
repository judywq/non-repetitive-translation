import os
import datetime

random_seed = 42

DEFAULT_LOG_LEVEL = "INFO"
# DEFAULT_LOG_LEVEL = "DEBUG"

official_model_gpt_3_5_turbo = 'gpt-3.5-turbo'
official_model_gpt_4 = 'gpt-4'
official_model_gpt_4o = 'gpt-4o-2024-05-13'

official_model_sonnet = 'claude-3-5-sonnet-20240620'
DEFAULT_MODEL = official_model_gpt_3_5_turbo

REQUEST_TIMEOUT_SECS = 60

ENABLE_LLM_TAGGING = False
ENABLE_LLM_TAGGING = True

# model_suffix = 'RepTg' # RepTg: Repitition Tagger
model_suffix = 'RepTrans1' # RepTrans: Repitition Translator

base_model_id = 'gpt-3.5-turbo-1106'
# base_model_id = 'ft:gpt-3.5-turbo-0613:waseda-university:eassy-test-2:8CTA9Ik1'

date_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# input_name = 'wat2023'
input_name = 'wmt2024'

if input_name == 'wat2023':
  input_root= 'data/input/wat2023'
  file_prefix = 'wat2023.devtest'
elif input_name == 'wmt2024':
  input_root= 'data/input/wmt2024'
  file_prefix = 'wmt2024.test'

wat_raw_ja = os.path.join(input_root, f'{file_prefix}.raw.ja')
wat_raw_en = os.path.join(input_root, f'{file_prefix}.raw.en')
wat_tagged_ja = os.path.join(input_root, f'{file_prefix}.tagged.ja')
wat_tagged_en = os.path.join(input_root, f'{file_prefix}.tagged.en')

output_root = os.path.join('data', 'output')

global_run_id = 'the-first-run'

finetune_root = os.path.join(output_root, global_run_id)

wat_ja_en_official_color = os.path.join(finetune_root, 'tag', f'{file_prefix}.ja_en.official.color.xlsx')
wat_ja_my_tagged_details = os.path.join(finetune_root, 'tag', f'{file_prefix}.tagged_words_all_detail.xlsx')

wat_ja_my_tagged = os.path.join(finetune_root, 'tag', f'{file_prefix}.ja.mytag.xlsx')
wat_ja_my_tagged_color = os.path.join(finetune_root, 'tag', f'{file_prefix}.ja.mytag.color.xlsx')
wat_ja_my_tagged_color_merged = os.path.join(finetune_root, 'tag', f'{file_prefix}.ja.mytag.merged.color.xlsx')

wat_ja_my_tagged_problematic = os.path.join(finetune_root, 'tag', f'{file_prefix}.ja.mytag.problematic.xlsx')
wat_ja_my_tagged_problematic_color = os.path.join(finetune_root, 'tag', f'{file_prefix}.ja.mytag.problematic.color.xlsx')
wat_ja_my_tagged_problematic_color_merged = os.path.join(finetune_root, 'tag', f'{file_prefix}.ja.mytag.problematic.merged.color.xlsx')

wat_ja_my_tagged_en_translation = os.path.join(finetune_root, 'tag', f'{file_prefix}.ja.mytag.translated.xlsx')
wat_ja_my_tagged_clean = os.path.join(finetune_root, 'tag', f'{file_prefix}.ja.mytag_clean.xlsx')
wat_ja_my_tagged_clean_annotation = os.path.join(finetune_root, 'tag', f'{file_prefix}.ja.mytag_clean.annotation.xlsx')

wat_index_ja_en = os.path.join(finetune_root, 'index', f'{file_prefix}.ja_en.xlsx')
wat_index_ja_en_split = os.path.join(finetune_root, 'index', f'{file_prefix}.ja_en.split.xlsx')
index_train_filename = os.path.join(finetune_root, 'index', 'train.xlsx')
index_val_filename = os.path.join(finetune_root, 'index', 'val.xlsx')
index_test_filename = os.path.join(finetune_root, 'index', 'test.xlsx')

dataset_train_filename = os.path.join(finetune_root, 'dataset', 'train.jsonl')
dataset_val_filename = os.path.join(finetune_root, 'dataset', 'val.jsonl')
dataset_test_filename = os.path.join(finetune_root, 'dataset', 'test.jsonl')

file_id_filename = os.path.join(finetune_root, 'ids', 'file-id.json')
job_id_filename = os.path.join(finetune_root, 'ids', 'job-id.json')
test_result_filename = os.path.join(finetune_root, 'results', 'test-result-finetuned.xlsx')
test_result_filename_proof = os.path.join(finetune_root, 'results', 'test-result-finetuned.proof.xlsx')
test_result_official_filename = os.path.join(finetune_root, 'results', 'test-result.{model}.temp-{temp}.xlsx')
test_result_official_checked_filename = os.path.join(finetune_root, 'results', 'test-result-{model}.checked.xlsx')
all_result_official_filename = os.path.join(finetune_root, 'results', 'all-result.xlsx')
all_result_official_clean_filename = os.path.join(finetune_root, 'results', 'all-result.manual_clean.xlsx')
all_result_official_proof_filename = os.path.join(finetune_root, 'results', 'all-result.proof.xlsx')
all_result_official_proof_tagged_filename = os.path.join(finetune_root, 'results', 'all-result.proof.tagged.xlsx')
all_result_official_proof_tagged_ja_tagged_filename = os.path.join(finetune_root, 'results', 'all-result.proof.tagged.ja_tagged.xlsx')
final_result_ja_tag_filename = os.path.join(finetune_root, 'results', f'{file_prefix}.mytag.ja.txt')
final_result_en_trans_filename = os.path.join(finetune_root, 'results', f'{file_prefix}.myraw.en.txt')
all_result_official_proof_tagged_ja_tagged_txt_filename = os.path.join(finetune_root, 'results', f'{file_prefix}.mytag.ja.txt')
all_result_official_proof_tagged_annotate_filename = os.path.join(finetune_root, 'results', 'all-result.proof.tagged.color.xlsx')
all_result_official_proof_judge_filename = os.path.join(finetune_root, 'results', 'all-result.proof.judge.xlsx')
all_result_official_proof_judge_check_filename = os.path.join(finetune_root, 'results', 'all-result.proof.judge.check.xlsx')

all_result_rerun_filename = os.path.join(finetune_root, 'rerun', 'all-result.proof.tagged.color.1.xlsx')

num_per_group = {
    'train': 100,
    'val': 20,
    'test': 40
}


system_message_short = """You are a professional Japanese-English translator of news articles.
Please translate the Japanese text and respond in this JSON format:
{
  "en_translation": ".......",
  "targets": [
    {
      "id": "0",
      "ref": "0",
      "ja_element": "...",
      "en_element": "...",
      "type": "...",
      "subtype": "..."
    },
    {
      "id": "0",
      "ref": "1",
      "ja_element": "...",
      "en_element": "...",
      "type": "...",
      "subtype": "..."
    }
  ]
}
"""

system_message_with_example = """You are a professional Japanese-English translator of news articles.
You will be given a Japanese sentence where the repeated word/phrase (elements) are tagged with a `target` xml-like markup element.
The tags include a unique ID of the repeated element and a ref number indicating the number of occurrence of the element in the Japanese text.
Both ID and ref numbers start from 0. 

Your task is to translate the Japanese sentence into English while reducing the redundancy in the Japanese text, along with the detailed translation of each element.
Besides, you should categorize the strategy you used in handling each repeated elements.
There are strategies ("type") and sub-strategies ("subtype") used in reducing redundancy in translation. 

The types include:
1. "substitution"(s): a different translation of the repeated element is adopted in the current occurrence as compared to that in a previous occurence. Please pay attention that using derivatives and different inflected forms of the same stems is not considered substitution. 
2. "reduction"(r): ommiting the translation of the repeated element in the current occurrence. 
3. "first occurrence"(f): this is the first time this element occurred.
4. "consistent translations"(c): the Japanese element should be translated into the same English element

The subtypes include:
- "literal translation"(lt)
- "ellipsis"(el)
- "semantic pleonasm"(sp)
- "sharing heads"(sh)
- "synonym"(syn)
- "non-literal translation"(nlt)
- "pronouns/pro-verbs"(pro)

Your response should be in a JSON format like follows:
{
  "en_translation": ".......",
  "targets": [
    {
      "id": "0",
      "ref": "0",
      "ja_element": "...",
      "en_element": "...",
      "type": "...",
      "subtype": "..."
    },
    {
      "id": "0",
      "ref": "1",
      "ja_element": "...",
      "en_element": "...",
      "type": "...",
      "subtype": "..."
    }
  ]
}
"""

system_message_translate_tagged_langchain = """### TASK DESCRIPTION
This task focuses on lexical choice in machine translation, especially choice regarding repeated words in a source sentence. Generally, the repetition of the same words can create a monotonous or awkward impression in English, and it should be appropriately avoided. Typical workarounds in monolingual writing are to (1) remove redundant terms if possible (reduction) or (2) use alternative words such as synonyms as substitutes (substitution). These techniques are also observed in human translations. Here are some examples, which are all not contained in the test set of this task:
Table 1. Examples of translations with reduction and substitution from Jiji Japanese–English news articles. For comparison, the consistent translations are also included.
Type  Japanese  Consistent translation (Ja→En)  English (Original)  Subtype
Reduction 耐震化を済ませていない４９４団体に今後の対応を尋ねたところ、改修するのは７０団体、建て替えは２６５団体 、移転が１１団体だった。  When the 494 organizations that had not yet completed earthquake proofing were asked about their future measures, 70 organizations opted for retrofitting, 265 chose rebuilding, and 11 selected relocation.  Of the 494 unprepared municipalities, 70 are set to carry out repairs, 265 will construct new buildings and 11 are planning relocation. Ellipsis: In the original English sentence, a noun ellipsis occurs, e.g., "70 municipalities" is expressed as "70."
  開発費を参加国間で分担できるため、国産団体に比べて費用を安く抑えることが可能となる。  Since development expenses can be shared among participating countries, it will be possible to keep costs lower than domestic development.  It will allow the government to cut spending compared with full domestic development by sharing costs with partner countries. Semantic pleonasm: "costs" is used instead of "development costs" in the original English sentence probably because it is contextually inferable.
  同社はニューヨーク州のヨンカース工場と中西部ネブラスカ州のリンカーン工場で車両の製造や試験を行う。 The company will manufacture and test vehicles at its Yonkers, New York, factory and its Lincoln, Nebraska, factory in the Midwest. Kawasaki Rail Car will build and test the subway cars at its facilities in Yonkers and in Lincoln, Nebraska.  Sharing heads: The two nouns ("facility") are merged into one and the noun head is shared by the two prepositional phrases. Although strictly they are not reduced, we also consider these examples to be a type of reduction.
Substitution  農作物への影響が心配されるが、農林水産省は「（首都圏などでは）積雪が長引かなかったので大きな影響はない」（園芸作物課）とみている。 There are concerns about the impact on crops, but an official at the Horticultural Crops Division of the Ministry of Agriculture, Forestry and Fisheries (MAFF) said, "the snowfall (in the Tokyo metropolitan area and other regions) was not prolonged, so there will be no major impact."  Although many people are worried about the effects of harsh cold on crops, an official of Japan’s agricultural ministry predicted that there will be no significant impact, as the snow did not stay for long in areas such as the Tokyo metropolitan area. Synonym: Words with similar meaning are typically used for substitution.
  物質を構成する素粒子の振る舞いは「標準理論」で説明されるが、宇宙の全質量の４分の１を占める「暗黒物質」など説明できない部分もある。 The Standard theory explains the behavior of elementary particles, which make up matter, but it cannot explain some things, such as dark matter, which makes up one quarter of the mass of the universe.  The so-called Standard Model explains the behavior of elementary particles, the fundamental building blocks of matter. But the theory leaves some mysteries, such as dark matter which is thought to make up about a quarter of the mass of the universe. Non-literal translation: Repeated words are sometimes translated in a non-literal manner.
  当時、テニス部の生徒６人とコーチがコートで練習をしており、生徒の１人がボールを拾おうとしたところ、隣のコートにパラシュート状の物があることに気付いたという。  At the time, six students and the coach from the tennis club were reportedly practicing on the court when one of the students went to pick up a ball and noticed a parachute-like object on the adjacent court. At the time, the student was practicing tennis with five other students and one coach at another court next to the one where the parachute was found. Pronouns/Pro-verbs: Repeated words are sometimes substituted with pronouns or pro-verbs, such as "it" and "do so."

### Requirements
The requirements this task include the following:
• Maintaining the balance between translation quality and controlling the output: The translation quality can be degraded when the non-repetitive style is inappropriately enforced.
• Avoiding bias toward high-frequency bilingual word pairs: use strategies such as contexualized non-literal translation.
• Predicting which words can be reduced or substituted appropriately depending on the context within the sentence.
• Do not assume the gender of anonymous persons such as "〇〇〇〇氏". Translate them as "Mr./Ms. 〇〇〇〇"
• If at the beginning of the sentence, there is a header showing the location of the news, the date and the branch of the Jiji press, such as "ソウル、1月24日（時事通信）--" or "ソウル、1月24日（ソウル時事）--", there is no need to reduce redundancy for the country name/location in the header or in the Japanese sentence.

### INPUT and OUTPUT
The input will be a Japanese text with repeated elements tagged. Each element is assigned a unique ID and a ref number indicating the number of occurrence in the Japanese text. Both ID and ref numbers start from 0. 
As a professional translator in news articles, your job is to translate the Japanese text into English while trying to avoid redundancy in the tagged repeated elements. Then, please list the corresponding translation, strategies ("type") and sub-strategies ("subtype") used in reducing redundancy in translation.
The types are as follows: 
1. "first occurrence" (f): the translation of the repeated element occurred for the first time in the English sentence; 
2. "consistency" (c): the translation of the repeated element in the current occurrence is the same with a previous occurrence; 
3. "substitution" (s): the translation of the repeated element in the current occurrence differs from a previous occurence. The determination of "substitution" or "consistency" is basically based on the word stem. For example, conversions between voice (e.g., "attack" and "be attacked"), tense (e.g., "study" and "studied") and parts of speech (e.g., "problematic" and "problem") are not considered to be substitutions. Conversions to idioms (e.g., "visit" and "pay a visit") are an exception and are handled as substitutions.
4. "reduction" (r): the translation of the repeated element in the current occurrence is omitted. 

The subtypes include:
1. "literal translation"(lt)
2.  "ellipsis"(el)
3.  "semantic pleonasm"(sp)
4.  "sharing heads"(sh)
5. "synonym"(syn)
6.  "non-literal translation"(nlt)
7. "pronouns/pro-verbs"(pro)

For "ellipsis", "semantic pleonasm", "sharing heads", "synonym", "non-literal translation", "pronouns/pro-verbs", refer to TASK DESCRIPTION above.

### Example
Return the output in JSON format and NOTHING ELSE. The following is an example:
Input: 準備を済ませていない494<target id=0 ref=0>団体</target>のうち、改修を予定しているのは70<target id=0 ref=1>団体</target>、新庁舎を建設するのは265<target id=0 ref=2>団体</target>、移転を予定しているのが11<target id=0 ref=3>団体</target>である。
Output: 
{{
  "en_translation": "Of the 494 unprepared municipalities, 70 are set to carry out repairs, 265 will construct new buildings and 11 are planning relocation.",
  "targets": [
    {{
      "id": "0",
      "ref": "0",
      "ja_element": "団体",
      "en_element": "municipalities",
      "type": "f",
      "subtype": "lt"
    }},
    {{
      "id": "0",
      "ref": "1",
      "ja_element": "団体",
      "en_element": "N/A",
      "type": "r",
      "subtype": "el"
    }},
    {{
      "id": "0",
      "ref": "2",
      "ja_element": "団体",
      "en_element": "N/A",
      "type": "r",
      "subtype": "el"
    }},
    {{
      "id": "0",
      "ref": "3",
      "ja_element": "団体",
      "en_element": "N/A",
      "type": "r",
      "subtype": "el"
    }}
  ]
}}
"""


system_message_proof_reader_langchain = """You are a professional Japanese-English translation proofreader in the field of news articles. You will be presented with a Japanese text with repeated elements tagged ("ja_text"), its English translation ("en_translation"), the corresponding translation of each occurrence of every repeated element ("targets"), and the types and subtypes of strategies used to reduce redundancy in translating the repeated elements. 

The types include:
1. "first occurrence" (f): the translation of the repeated element occurred for the first time in the English sentence; 
2. "consistency" (c): the translation of the repeated element in the current occurrence is the same with a previous occurrence; 
3. "substitution" (s): the translation of the repeated element in the current occurrence differs from a previous occurence. The determination of "substitution" or "consistency" is basically based on the word stem. For example, conversions between voice (e.g., "attack" and "be attacked"), tense (e.g., "study" and "studied") and parts of speech (e.g., "problematic" and "problem") are not considered to be substitutions. Conversions to idioms (e.g., "visit" and "pay a visit") are an exception and are handled as substitutions.
4. "reduction" (r): the translation of the repeated element in the current occurrence is omitted. 

The subtypes include:
- "literal translation"(lt)
- "ellipsis"(el)
- "semantic pleonasm"(sp)
- "sharing heads"(sh)
- "synonym"(syn)
- "non-literal translation"(nlt)
- "pronouns/pro-verbs"(pro)

For "ellipsis", "semantic pleonasm", "sharing heads", "synonym", "non-literal translation", "pronouns/pro-verbs", here are some examples:
Table 1. Examples of translations with reduction and substitution from Jiji Japanese–English news articles. For comparison, the consistent translations are also included.
Type  Japanese  Consistent translation (Ja→En)  English (Original)  Subtype and description
Reduction 耐震化を済ませていない４９４団体に今後の対応を尋ねたところ、改修するのは７０団体、建て替えは２６５団体 、移転が１１団体だった。  When the 494 organizations that had not yet completed earthquake proofing were asked about their future measures, 70 organizations opted for retrofitting, 265 chose rebuilding, and 11 selected relocation.  Of the 494 unprepared municipalities, 70 are set to carry out repairs, 265 will construct new buildings and 11 are planning relocation. Ellipsis: In the original English sentence, a noun ellipsis occurs, e.g., "70 municipalities" is expressed as "70."
  開発費を参加国間で分担できるため、国産団体に比べて費用を安く抑えることが可能となる。  Since development expenses can be shared among participating countries, it will be possible to keep costs lower than domestic development.  It will allow the government to cut spending compared with full domestic development by sharing costs with partner countries. Semantic pleonasm: "costs" is used instead of "development costs" in the original English sentence probably because it is contextually inferable.
  同社はニューヨーク州のヨンカース工場と中西部ネブラスカ州のリンカーン工場で車両の製造や試験を行う。 The company will manufacture and test vehicles at its Yonkers, New York, factory and its Lincoln, Nebraska, factory in the Midwest. Kawasaki Rail Car will build and test the subway cars at its facilities in Yonkers and in Lincoln, Nebraska.  Sharing heads: The two nouns ("facility") are merged into one and the noun head is shared by the two prepositional phrases. Although strictly they are not reduced, we also consider these examples to be a type of reduction.
Substitution  農作物への影響が心配されるが、農林水産省は「（首都圏などでは）積雪が長引かなかったので大きな影響はない」（園芸作物課）とみている。 There are concerns about the impact on crops, but an official at the Horticultural Crops Division of the Ministry of Agriculture, Forestry and Fisheries (MAFF) said, "the snowfall (in the Tokyo metropolitan area and other regions) was not prolonged, so there will be no major impact."  Although many people are worried about the effects of harsh cold on crops, an official of Japan’s agricultural ministry predicted that there will be no significant impact, as the snow did not stay for long in areas such as the Tokyo metropolitan area. Synonym: Words with similar meaning are typically used for substitution.
  物質を構成する素粒子の振る舞いは「標準理論」で説明されるが、宇宙の全質量の４分の１を占める「暗黒物質」など説明できない部分もある。 The Standard theory explains the behavior of elementary particles, which make up matter, but it cannot explain some things, such as dark matter, which makes up one quarter of the mass of the universe.  The so-called Standard Model explains the behavior of elementary particles, the fundamental building blocks of matter. But the theory leaves some mysteries, such as dark matter which is thought to make up about a quarter of the mass of the universe. Non-literal translation: Repeated words are sometimes translated in a non-literal manner.
  当時、テニス部の生徒６人とコーチがコートで練習をしており、生徒の１人がボールを拾おうとしたところ、隣のコートにパラシュート状の物があることに気付いたという。  At the time, six students and the coach from the tennis club were reportedly practicing on the court when one of the students went to pick up a ball and noticed a parachute-like object on the adjacent court. At the time, the student was practicing tennis with five other students and one coach at another court next to the one where the parachute was found. Pronouns/Pro-verbs: Repeated words are sometimes substituted with pronouns or pro-verbs, such as "it" and "do so."

Based on your expertise, you need to proofread the translation by doing the following:
1. for elements tagged with the type of "first occurrence" ("f"), where the translation of the repeated element occurred explicitly for the first time in the English sentence and thus redundancy reduction is not necessary, decide whether the target translation, the types and subtypes of strategies are appropriate. 
2. for elements tagged with the type of "consistency" ("c"), where the same translation is adopted for multiple occurrences, decide whether the redundancy can be further removed by adopting another expression. Please note sometimes consistency can be retained to ensure clarity in translation, such as the translation of job titles. Based on the context, if you think it is possible to further remove redundancy, please modify the translation and add relevant type and subtype of strategy. 
3. for elements tagged with the type of "substitution" ("s"), check if the substitution shares any word of the same stem or lemma with any word in any other occurrences (for compound words, any part of the compound should not overlap with any words in other occurrences. For example, "sub-optimal" and "optimal" are considered redundancy). If there are still shared stems or lemmas, i.e., redundancy, in substitution, change the substitution to another expression to avoid repeating words of the same stem or lemma.
4. for "reduction" ("r"), decide whether the target translation, types and subtypes are appropriate. 

Apart from the above mentioned scenarios, please refrain from making minor changes to the translations, types and subtypes unless the original translation has grammar mistakes and/or deviates significantly from the meaning in the Japanese sentence. Also, if the original translation has already reduced redundancy but you think further changes, please make sure your change will not introduce redundancy (consistent translations or words of the same stem/lemma) again.

If no changes are needed, return the following in JSON and NOTHING ELSE:
{{
  "changed": "No"
}}

If changes are necessary, return the updated sentence translation and translations of the targets together with relevant types and subtypes in JSON and NOTHING ELSE:
{{
  "changed": "Yes",
  "en_translation_updated": ".......",
  "targets_updated": [
    {{
      "id": "0",
      "ref": "0",
      "ja_element": "...",
      "en_element": "...",
      "type": "...",
      "subtype": "..."
    }},
    {{
      "id": "0",
      "ref": "1",
      "ja_element": "...",
      "en_element": "...",
      "type": "...",
      "subtype": "..."
    }},
    ...
  ]
}}
"""

system_message_judge_langchain = """You are a professional Japanese-English translator for a news agency. You need to compare two translations for the same Japanese sentence to decide which version is better. In the Japanese sentences, there are repeated elements, and as such, both translations aim to translate the sentence while reducing the redundancy in translation. The input format is as follows:
{{
  "ja_text": "The Japanese sentence here",
  "translations": [
    {{
      "version": "v1",
      "en_translation": "English translation version 1"
    }},
    {{
      "version": "v2",
      "en_translation": "English translation version 2"
    }}
  ]
}}

When deciding which version is better, please considered the following criteria in descending order of importance:
1. Grammatical accuracy. A translation containing grammar errors should not be adopted.
2. Lexical diversity. For the repeated elements in Japanese, the better translation should try to avoid using expressions that include words of the same stem or lemma in translation (such as "test" and "testing"; "max" and "maximum"; "sub-optimal" and "optimal"). Synonyms are acceptable for lexical diversity. However, there is no need to consider translation other than the tagged elements.
3. Expressiveness. The better translation should use more appropriate wording to capture the exact meaning of the Japanese sentence.

Return your decision in JSON format based on the following example:

{{
  "better": "version number",
  "reason": "Your reason here."
}}
"""


system_message_check = """You are a professional Japanese-English translation proofreader in the field of news articles. You will be presented with a Japanese text with repeated elements tagged ("ja_text"), its English translation ("en_translation"), the corresponding translation of each occurrence of every repeated element ("targets"), and the types and subtypes of strategies used to reduce redundancy in translating the repeated elements. The following is an input template:

{{
  "ja_text": "....."
  "en_translation": "...."
  "targets": [
    {{
      "id": "0",
      "ref": "0",
      "ja_element": "...",
      "en_element": "...",
      "type": "...",
      "subtype": "..."
    }},
    {{
      "id": "0",
      "ref": "1",
      "ja_element": "...",
      "en_element": "...",
      "type": "...",
      "subtype": "..."
    }},
    ...
  ]
}}

The types include:
1. "first occurrence" (f): the translation of the repeated element occurred for the first time in the English sentence; 
2. "consistency" (c): the translation of the repeated element in the current occurrence is the same with a previous occurrence; 
3. "substitution" (s): the translation of the repeated element in the current occurrence differs from a previous occurrence. The determination of "substitution" or "consistency" is basically based on the word stem. Words of the same lemma/stem with a previous occurrence (e.g., "problem" and "problematic") are not considered substitution but consistency. Also, compound words that contain part of the same lemma/stem with a previous occurrence (e.g., "sub-optimal" and "optimal") are not considered substitution but consistency as both contain the lemma "optimal".
4. "reduction" (r): the translation of the repeated element in the current occurrence is omitted. 

The subtypes include:
- "literal translation"(lt)
- "ellipsis"(el)
- "semantic pleonasm"(sp)
- "sharing heads"(sh)
- "synonym"(syn)
- "non-literal translation"(nlt)
- "pronouns/pro-verbs"(pro)

Based on your trained knowledge, please decide whether the types and subtypes are correctly assigned in each case. Do not make any change to the translation of the sentences or the targets. Return your output in JSON using the following format. Please do not include information other than required. 

If no changes are needed, return the following in JSON and NOTHING ELSE:
{{
"changed": "No"
}}

If changes are necessary, return updated types and subtypes in JSON and NOTHING ELSE as follows:
{{
  "changed": "Yes"
  "targets": [
    {{
      "id": "0",
      "ref": "0",
      "ja_element": "...",
      "en_element": "...",
      "type": "...",
      "subtype": "..."
    }},
    {{
      "id": "0",
      "ref": "1",
      "ja_element": "...",
      "en_element": "...",
      "type": "...",
      "subtype": "..."
    }},
    ...
  ]
}}
"""

system_message_tagging_ja_langchain = """You wil be given a Japanese sentence.
Return all the repeated elements with concrete meanings in the Japanese sentence as a JSON object and NOTHING ELSE. 
If there is more than one repeated element (target), number them accordingly. Here is an example:

Japanese sentence: 
"民進党の小西洋之氏は、小野寺氏に辞任を要求。 || 小野寺氏は「（調査に）厳正に対応していきたい」と述べ、辞任を否定した。"

Output:
{{
  "targets": [
    {{
      "id": "0",
      "target_token": "辞任"
    }},
    ...
  ]
}}
"""


system_message_translate_non_tagged = """You are a professional Japanese-English translation proofreader in the field of news articles. 
Please translate the given Japanese sentence into English.
Do not assume the gender of anonymous persons such as "〇〇〇〇氏". Translate them as "Mr./Ms. 〇〇〇〇"
"""
