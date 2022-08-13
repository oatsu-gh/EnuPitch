#!/usr/bin/env python3
# Copyright (c) 2022 oatsu
"""
ENUNUで合成したf0をUTAUのピッチ曲線としてフィードバックする。
"""

from math import log2
from pprint import pprint
from typing import List

import utaupy

FRAME_PERIOD = 5  # ms
CONCERT_PITCH = 440
F0_FLOOR = 32


def load_f0(path_f0):
    """f0のファイルを読み取る
    """
    with open(path_f0, 'r', encoding='utf-8') as f:
        f0_list = list(map(float, f.read().splitlines()))
    return f0_list


def notenum2hz(notenum: int, concert_pitch) -> float:
    """UTAUの音階番号を周波数に変換する
    """
    return concert_pitch * (2 ** ((notenum - 69) / 12))


def get_base_f0_list(note: utaupy.ust.Note, frame_period: int, concert_pitch) -> List[float]:
    """UTAUのノートから、基準となる周波数を取得する。

    1msにつき1要素のリストを返す。
    """
    # 周波数に変換
    f0 = notenum2hz(note.notenum, concert_pitch)
    # 数msにつき1要素のリストにして返す
    f0_list = [f0] * round(note.length_ms / frame_period)
    return f0_list


def devide_pby_for_each_note(pby_list, ust: utaupy.ust.Ust, frame_period: int):
    """PBYを各ノートごとに分配しやすいように、2次元リストに変換する。
    """
    # 各ノートのf0点数
    number_of_f0_samples_in_each_note = [
        round(note.length_ms / frame_period) for note in ust.notes
    ]
    # ノートごとに分割したf0リストを格納するリスト
    pby_list_2d = []
    # ノートごとにf0をリストとして取り出していく
    slice_start = 0
    slice_end = 0
    for n in number_of_f0_samples_in_each_note:
        slice_end += n
        pby_list_2d.append(pby_list[slice_start - 1:slice_end])
        slice_start += n

    # ちゃんとノートごとに分割されているかチェック
    assert len(pby_list_2d) == len(ust.notes)

    return pby_list_2d


def devide_pbw_for_each_note(pby_list, ust: utaupy.ust.Ust, frame_period: int):
    """PBWを各ノートごとに分配しやすいように、2次元リストに変換する。
    """
    # 各ノートのf0点数
    number_of_f0_samples_in_each_note = [
        round(note.length_ms / frame_period) for note in ust.notes
    ]
    # ノートごとに分割したf0リストを格納するリスト
    l_2d = []
    # ノートごとにf0をリストとして取り出していく
    slice_start = 0
    slice_end = 0
    for n in number_of_f0_samples_in_each_note:
        slice_end += n
        l_2d.append(pby_list[slice_start - 1:slice_end])
        slice_start += n

    # ちゃんとノートごとに分割されているかチェック
    assert len(l_2d) == len(ust.notes)

    return l_2d


def test():
    """Test
    """
    # USTファイルを読み取る
    path_ust = input('USTファイルを指定してください: ').strip('"')
    ust = utaupy.ust.load(path_ust)

    # f0ファイルを読み取る
    path_f0 = input('f0ファイルを指定してください: ').strip('"')
    f0_list = load_f0(path_f0)
    # 底を10とする対数のリストに変換する。
    # f0が負や0だと対数変換できないのを回避しつつ、log(f0)>0 となるようにする。
    log_f0_list = [log2(max(f0, F0_FLOOR)) for f0 in f0_list]

    # 全ノートのf0を取得する
    base_f0_list = []
    for note in ust.notes:
        base_f0_list += get_base_f0_list(note, FRAME_PERIOD, CONCERT_PITCH)
    # 対数変換
    base_log_f0_list = [log2(f0) for f0 in base_f0_list]

    # f0のサンプル数
    print('f0 ファイルのf0サンプル数:', len(log_f0_list))
    print('USTファイルのf0サンプル数:', len(base_log_f0_list))
    assert len(log_f0_list) == len(
        base_log_f0_list), 'f0ファイルとUSTファイルのf0の点数が一致しません。処理できません。'

    # f0の差分
    log_f0_difference_list = [
        f0 - base_f0 for (f0, base_f0) in zip(log_f0_list, base_log_f0_list)
    ]

    # PBY (cent) に変換
    # log_f0_step_per_notenum = 1/12
    # pby_list = [10.0 * log_f0_diff / log2_f0_step_per_notenum]
    pby_list = [120.0 * log_f0_diff for log_f0_diff in log_f0_difference_list]

    # PBWのリストを生成 (全てのピッチ点で5ms間隔)
    pbw_list = [5] * (len(pby_list) - 1)

    # PBYを各ノートに区切って2次元リストにする
    pby_list = devide_pby_for_each_note(pby_list, ust, FRAME_PERIOD)
    print([len(v) for v in pby_list])
    # PBWを各ノートに区切って2次元リストにする
    pbw_list = devide_pbw_for_each_note(pbw_list, ust, FRAME_PERIOD)
    print([len(v) for v in pbw_list])

    # ustのpbyとpbwを上書きしつつ、pbsとpbmを初期化
    # 最初のノート
    ust.notes[0].pbs = [0, 0.0]
    ust.notes[0].pby = pby_list[0]
    ust.notes[0].pby.append(0)
    ust.notes[0].pbw = pbw_list[0]
    ust.notes[0].pbw.append(0)
    ust.notes[0].pbm = []
    ust.notes[0].pbw[0] = 0
    # 2ノート目以降
    for i, note in enumerate(ust.notes[1:], 1):
        offset = - (ust.notes[i-1].length_ms % FRAME_PERIOD)
        note.pbs = [offset, 0]
        note.pbw = [0] + pbw_list[i] + [0]
        note.pby = [ust.notes[i-1].pby[-2]] + pby_list[i] + [0]
        note.pbm = []
        note.pbw[1] = offset

    path_ust_out = path_ust.replace('.ust', '_out.ust')
    ust.write(path_ust_out)


if __name__ == "__main__":
    test()
