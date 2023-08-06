import os

from clausewitz.hoi4_parsing.parse_def import Dictionary

round_degree = 5


def get_item_dict(root_path: str, file_list: list) -> dict:
    file_path_list = list_item_path(root_path, file_list)
    item_dict = {}
    for file_path in file_path_list:
        item_dict.update(get_item(file_path))

    return item_dict


def list_item_path(root_path: str, file_list: list) -> list:
    path_list = []
    for item in file_list:
        path_list.append(os.path.join(root_path, item))

    return path_list


def get_item(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf_8_sig') as file:
        str_ = file.read()
    res = Dictionary.parseString(str_)
    res_dict = {k: v.asDict() for k, v in res[0].items()}

    return res_dict


def round_sum(stat: list):
    return round(sum(stat), round_degree)


def round_min(stat: list):
    return round(min(stat), round_degree)


def round_max(stat: list):
    return round(max(stat), round_degree)


def round_util(stat):
    return round(stat, round_degree)


def trans_dict(in_dict: dict) -> dict:
    out_dict = {}
    for a in in_dict:
        for b in in_dict[a]:
            if b not in out_dict:
                out_dict[b] = {}
            out_dict[b][a] = in_dict[a][b]
    return out_dict


def sum_for_result_with_func(func, *avgs, n: int):
    _list = []
    for i in range(n):
        _list.append(func(*avgs))
    result = sum(_list)

    return result
