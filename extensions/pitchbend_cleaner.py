#!/usr/bin/env python3
# Copyright (c) 2024 oatsu
"""
USTの不要なピッチ点を削減する。
"""
from argparse import ArgumentParser

import utaupy


def round_pby(plugin, ndigits):
    """音高の小数を丸める。
    """
    for note in plugin.notes:
        if note.pbs is None or note.pby is None:
            continue
        note.pbs = [note.pbs[0], round(note.pbs[1], ndigits)]
        note.pby = [round(x, ndigits) for x in note.pby]


def reduce_pitch_points(plugin):
    """不要なピッチ点を削除する。具体的には、同じPBYが連続しているときに削除する。
    """
    for note in plugin.notes:
        # PBYがない場合はSkip
        if 'PBY' not in note:
            continue
        # 削減しようがない場合はSkip
        if len(note.pby) <= 2:
            continue
        assert len('PBY') == len('PBW') == len('PBM')

        # ピッチ点を削減する
        temp_pby = [note.pby[0]]
        temp_pbw = [note.pbw[0]]
        temp_pbm = [note.pbm[0]]

        # PBWの繰り越し量
        pbw_carry_over = 0
        for i, _ in enumerate(note.pby[1:-1], 1):
            if not note.pby[i-1] == note.pby[i] == note.pby[i+1]:
                temp_pby.append(note.pby[i])
                temp_pbw.append(note.pbw[i] + pbw_carry_over)
                temp_pbm.append(note.pbm[i])
                pbw_carry_over = 0
            else:
                print('ピッチ点を削除しました。')
                pbw_carry_over += note.pbw[i]

        # ノート内の最後のピッチ点を復元
        temp_pby.append(note.pby[-1])
        temp_pbw.append(note.pbw[-1] + pbw_carry_over)
        temp_pbm.append(note.pbm[-1])
        # 削減後のピッチ点でノート情報を上書き
        note.pby = temp_pby
        note.pbw = temp_pbw
        note.pbm = temp_pbm


def main(path_plugin):
    """
    全体の処理を実行する
    """
    plugin = utaupy.utauplugin.load(path_plugin)
    round_pby(plugin, ndigits=3)
    reduce_pitch_points(plugin)
    plugin.write(path_plugin)


if __name__ == '__main__':
    print('pitchbend_cleaner.py (2024-10-09) ---------------------')
    parser = ArgumentParser()
    parser.add_argument('--feedback', help='UTAUにフィードバックするために上書きするtmpファイル')
    # 使わない引数は無視
    args, _ = parser.parse_known_args()
    # 実行引数を渡して処理
    main(args.feedback)
    print('-------------------------------------------------------')
