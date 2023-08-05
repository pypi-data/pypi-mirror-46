# coding=utf-8
import csv

import pkg_resources
from gensim.parsing.preprocessing import strip_non_alphanum, strip_numeric, strip_multiple_whitespaces
from gensim import utils

from pyvi import ViTokenizer
import json

LIST_SENTENCE = 'list_sentence'
WORD = 'word'
ACRONYM = { "đc": "được", "ntn": "như thế nào", "cccm": "các cụ các mợ", "cmt": "bình luận", "ib": "nhắn tin",
            "mn": "mọi người", "vn": "việt nam", "nyc": "người yêu cũ", "ko": "không", "k": "không",
            "nx": "nhận xét", "sđt": "số điện thoại", "fa": "độc thân", "ox": "ông xã", "bx": "bà xã",
            "nc": "nước", "ny": "người yêu", "fb": "facebook", "hcm": "hồ chí minh", "mk": "mật khẩu",
            "tk": "tài khoản", "acc": "tài khoản", "pw": "mật khẩu", "rep": "trả lời", "sn": "sinh nhật",
            "snvv": "sinh nhật vui vẻ", "hpbd": "chúc mừng sinh nhật", "lm": "làm", "atm": "cây rút tiền",
            "mm": "may mắn", "bn": "bao nhiêu", "cocc": "con ông cháu cha"}


with open(pkg_resources.resource_filename(__name__, 'vietnamese-stopwords-dash.txt'), 'r', encoding="utf-8") as f:
    stopwords = f.readlines()
    stop_set = set(m.strip() for m in stopwords)
    STOP_WORD = frozenset(stop_set)


def remove_stopword(s):
    s = utils.to_unicode(s)
    return " ".join(w for w in s.split() if w not in STOP_WORD)


def replace_acronym(s):
    for word in ACRONYM:
        s = s.replace(' '+word+' ', ' '+ACRONYM[word]+' ')
    return s


def clean_text_file(url_file=''):
    data_list = []
    try:
        with open(url_file, 'r+', encoding='utf-8') as data_file:
            data = csv.reader(data_file)
            for row in data:
                i = 0
                for sentence in row:
                    if i == 0:
                        word = sentence
                        sentence_parse = []
                    else:
                        try:
                            contents_parsed = strip_non_alphanum(sentence).lower().strip()  # Xóa các ký tự đặc biệt
                            contents_parsed = strip_numeric(contents_parsed)  # Xóa các ký tự đặc biệt không phải chữ hoặc
                            contents_parsed = replace_acronym(contents_parsed)  # replace từ viết tắt
                            contents_parsed = ViTokenizer.tokenize(contents_parsed)  # phân từ đơn từ ghép
                            contents_parsed = remove_stopword(contents_parsed)  # xóa các từ có trong stop word
                            contents_parsed = strip_multiple_whitespaces(contents_parsed)  # Chuẩn hóa để mỗi từ cách nhau một khoảng trắng
                            sentence_parse.append(contents_parsed)

                        except Exception as e:
                            return str(e)
                    i += 1

                if row:
                    data_list.append({LIST_SENTENCE: sentence_parse, WORD: word})

        return json.dumps(data_list)
    except Exception as e:
        return json.dumps(str(e))
    
    
def clean_text_json(json_data):
    data_list = []
    try:
        for keyword in json_data:
            sentence_parse = []
            for sentence in keyword[LIST_SENTENCE]:
                contents_parsed = strip_non_alphanum(sentence).lower().strip()  # Xóa các ký tự đặc biệt
                contents_parsed = strip_numeric(contents_parsed)  # Xóa các ký tự đặc biệt không phải chữ hoặc
                contents_parsed = replace_acronym(contents_parsed)  # replace từ viết tắt
                contents_parsed = ViTokenizer.tokenize(contents_parsed)  # phân từ đơn từ ghép
                contents_parsed = remove_stopword(contents_parsed)  # xóa các từ có trong stop word
                contents_parsed = strip_multiple_whitespaces(
                    contents_parsed)  # Chuẩn hóa để mỗi từ cách nhau một khoảng trắng
                sentence_parse.append(contents_parsed)

            data_list.append({LIST_SENTENCE: sentence_parse, WORD: keyword[WORD]})

        return json.dumps(data_list)
    except Exception as e:
        return json.dumps(str(e))


def clean_text(sentence=''):

    try:
        contents_parsed = strip_non_alphanum(sentence).lower().strip()  # Xóa các ký tự đặc biệt
        contents_parsed = strip_numeric(contents_parsed)  # Xóa các ký tự đặc biệt không phải chữ hoặc
        contents_parsed = replace_acronym(contents_parsed)  # replace từ viết tắt
        contents_parsed = ViTokenizer.tokenize(contents_parsed)  # phân từ đơn từ ghép
        contents_parsed = remove_stopword(contents_parsed)  # xóa các từ có trong stop word
        contents_parsed = strip_multiple_whitespaces(contents_parsed)  # Chuẩn hóa để mỗi từ cách nhau một khoảng trắng
        return json.dumps(contents_parsed)
    except Exception as e:
        return json.dumps(str(e))


