"""
カノンさんが配布しているモデルの
「波音リツ CRISSCROSS 6style world-diffusion HN-uSFGAN NNSVS/ENUNU hed418 BEATテスト #4320」
に含まれている flag_separator.py を改造したもの。

改造内容
スタイルシフトのフラグとかぶらないように、1文字フラグに反応しない用にした。

"""

import os
import re
import sys

import utaupy

# -----------------------------------モデルに合わせて調整が必要　ここから-------------------------------------------------------
# フラグに何も入力しなかった場合のフラグ
DEFAULT_FLAGS = 'p9:0300/p16:s3s0r0b0p0g0'
# フラグを短くする


def short(data2):
    flagdict = {'!': '0000', 'st': '0', 'sw': '0',
                'ro': '0', 'br': '0', 'po': '0', 'gr': '0'}
    # print(data2)
    data2 = data2.lower()
    divided = re.findall(r'[a-zA-Z]+|\d+', data2)
    divided = ['!'] + divided
    # spacediv = data2.split('/')
    # print (data2)
    # print (divided)
    for i, item in enumerate(divided):
        if i == len(divided) - 1:
            continue
        elif item == '!':
            flagdict['!'] = divided[i+1]
        elif item == 'standard':
            flagdict['st'] = divided[i+1]
        elif item == 'sweet':
            flagdict['sw'] = divided[i+1]
        elif item == 'rock':
            flagdict['ro'] = divided[i+1]
        elif item == 'breathy':
            flagdict['br'] = divided[i+1]
        elif item == 'pop':
            flagdict['po'] = divided[i+1]
        elif item == 'growl':
            flagdict['gr'] = divided[i+1]
        # print (flagdict)

    # print (flagdict)
    data3 = f"p9:{flagdict['!']}/p16:s{flagdict['st']}s{flagdict['sw']
                                                        }r{flagdict['ro']}b{flagdict['br']}p{flagdict['po']}g{flagdict['gr']}"
    # print (f"flag covert: {data3}")
    return data3
# --------------------------------モデルに合わせて調整が必要　ここまで----------------------------------------------------------


def main():
    """全体の処理をする"""

    # コマンドライン引数を取得できる魔法の言葉
    args = sys.argv

    # カレントディレクトリ
    # cpath = os.getcwd()
    # print(cpath)

    # 辞書とやらにとりあえず使うパラメータを全部盛り
    lab_items = {'section': '', 'lyric': '', 'lyric2': '', 'lyric3': '', 'lyric4': '', 'p1': '', 'p2': '', 'p3': '', 'p4': '', 'p5': '', 'p6': '', 'p7': '', 'p8': '', 'p9': '', 'p10': '', 'p11': '', 'p12': '', 'p13': '', 'p14': '', 'p15': '', 'p16': '', 'a1': '', 'a2': '', 'a3': '', 'a4': '', 'a5': '', 'b1': '', 'b2': '', 'b3': '', 'b4': '', 'b5': '', 'c1': '', 'c2': '', 'c3': '', 'c4': '', 'c5': '', 'd1': '', 'd2': '', 'd3': '', 'd4': '', 'd5': '', 'd6': '', 'd7': '', 'd8': '', 'd9': '', 'e1': '', 'e2': '', 'e3': '', 'e4': '', 'e5': '', 'e6': '', 'e7': '', 'e8': '', 'e9': '', 'e10': '', 'e11': '', 'e12': '', 'e13': '', 'e14': '', 'e15': '', 'e16': '',
                 'e17': '', 'e18': '', 'e19': '', 'e20': '', 'e21': '', 'e22': '', 'e23': '', 'e24': '', 'e25': '', 'e26': '', 'e27': '', 'e28': '', 'e29': '', 'e30': '', 'e31': '', 'e32': '', 'e33': '', 'e34': '', 'e35': '', 'e36': '', 'e37': '', 'e38': '', 'e39': '', 'e40': '', 'e41': '', 'e42': '', 'e43': '', 'e44': '', 'e45': '', 'e46': '', 'e47': '', 'e48': '', 'e49': '', 'e50': '', 'e51': '', 'e52': '', 'e53': '', 'e54': '', 'e55': '', 'e56': '', 'e57': '', 'e58': '', 'e59': '', 'e60': '', 'f1': '', 'f2': '', 'f3': '', 'f4': '', 'f5': '', 'f6': '', 'f7': '', 'f8': '', 'f9': '', 'g1': '', 'g2': '', 'h1': '', 'h2': '', 'i1': '', 'i2': '', 'j1': '', 'j2': '', 'j3': ''}

    # 引数の数だけ回して--ustの次のやつがustのパス
    ustpath = None
    for i, _ in enumerate(args):
        # print (args[i])
        if args[i] == '--ust' and i + 1 < len(args):
            ustpath = args[i + 1]
    if ustpath is None:
        raise ValueError('EnuPitchから渡されたUSTのパスが分かりません')

    # print(ustpath)

    # USTをロードしてフラグを取得して/で割って:で割った。次いでに歌詞とセクション番号も取った
    ust = utaupy.ust.load(ustpath)
    # splited_by_slash = []
    splited_by_colon = []
    for i, note in enumerate(ust.notes):
        if note.flag.startswith('!'):  # 追記
            note.flag = short(note.flag)  # 追記
        if note.flag == "" and note.lyric != 'R':
            note.flag = DEFAULT_FLAGS
        flag_array = note.flags.split('/')
        flag_array.append(f"lyric:{note.lyric}")
        flag_array.append(f"section:{note.tag}")
        # print(flag_array)
        for i2 in flag_array:
            splited_part = i2.split(':')
            splited_by_colon.append(splited_part)

    # final flag check
    # for i in ust.notes:
    #    print (i.flag)

    # 辞書を配列に入れる　辞書に値を入れる　多分ここ後で見ても意味わからない
    cnt2 = 0
    new_array = []
    for i in splited_by_colon:
        # print(i)
        if i[0] in lab_items:
            lab_items[i[0]] = i[1]
        if i[0] == 'section':
            new_array.append(lab_items.copy())
            # print(lab_items)
            cnt2 += 1
    # print(cnt2)
    # print (new_array)

    ###############  phoneme.txtを読み込む  ############################
    file_path = 'phoneme.txt'
    # 結果を格納するリスト
    lines_without_newline = []
    lines_db_space = []
    # ファイルを開いて1行ずつ読み込む
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 末尾の改行を除去して配列に追加
            lines_without_newline.append(line.rstrip('\n'))
    for line in lines_without_newline:
        split_line = line.split(' ')
        lines_db_space.append(split_line)

    # print(lines_db_space)

    ###############   phonemeをループしてひらがな歌詞を音素名にする   ################
    cnt3 = 0
    for i in range(cnt2):
        for j in lines_db_space:
            # 促音統合専用
            if new_array[i]['lyric'].startswith('っ') == False and new_array[i]['lyric'].endswith('っ') == True:
                # print (f"----------{new_array[i]['lyric']}")
                new_array[i]['lyric'] = new_array[i]['lyric'].rstrip(
                    'っ')  # っを消す
                if new_array[i]['lyric'] in ("あ", "い", "う", "え", "お", "ん"):
                    new_array[i]['lyric3'] = 'cl'  # lyric4は統合促音専用
                else:
                    new_array[i]['lyric4'] = 'cl'  # lyric4は統合促音専用

            if new_array[i]['lyric'] == j[0]:  # phonemeをループしてlyricとかなが一致したら
                new_array[i]['lyric2'] = j[1]  # lyric2に1個目（子音）をいれる
                cnt3 += 1
                if len(j) == 3:  # 要素数が３なら子音があるってことだから
                    new_array[i]['lyric3'] = j[2]  # 母音もいれる
                    cnt3 += 1

    # print(new_array)

    #####################      ustparamのフォーマットにする     #############
    body = []
    for i in new_array:
        body.append(
            f"{i['section']}/{i['lyric2']}//{i['p1']}/{i['p2']
                                                       }/{i['p3']}/{i['p4']}/{i['p5']}/{i['p6']}/"
            f"{i['p7']}/{i['p8']}/{i['p9']}/{i['p10']}/{i['p11']
                                                        }/{i['p12']}/{i['p13']}/{i['p14']}/{i['p15']}/"
            f"{i['p16']}/{i['a1']}/{i['a2']}/{i['a3']}/{i['a4']
                                                        }/{i['a5']}/{i['b1']}/{i['b2']}/{i['b3']}/"
            f"{i['b4']}/{i['b5']}/{i['c1']}/{i['c2']}/{i['c3']
                                                       }/{i['c4']}/{i['c5']}/{i['d1']}/{i['d2']}/"
            f"{i['d3']}/{i['d4']}/{i['d5']}/{i['d6']}/{i['d7']
                                                       }/{i['d8']}/{i['d9']}/{i['e1']}/{i['e2']}/"
            f"{i['e3']}/{i['e4']}/{i['e5']}/{i['e6']}/{i['e7']
                                                       }/{i['e8']}/{i['e9']}/{i['e10']}/{i['e11']}/"
            f"{i['e12']}/{i['e13']}/{i['e14']}/{i['e15']
                                                }/{i['e16']}/{i['e17']}/{i['e18']}/{i['e19']}/"
            f"{i['e20']}/{i['e21']}/{i['e22']}/{i['e23']
                                                }/{i['e24']}/{i['e25']}/{i['e26']}/{i['e27']}/"
            f"{i['e28']}/{i['e29']}/{i['e30']}/{i['e31']
                                                }/{i['e32']}/{i['e33']}/{i['e34']}/{i['e35']}/"
            f"{i['e36']}/{i['e37']}/{i['e38']}/{i['e39']
                                                }/{i['e40']}/{i['e41']}/{i['e42']}/{i['e43']}/"
            f"{i['e44']}/{i['e45']}/{i['e46']}/{i['e47']
                                                }/{i['e48']}/{i['e49']}/{i['e50']}/{i['e51']}/"
            f"{i['e52']}/{i['e53']}/{i['e54']}/{i['e55']
                                                }/{i['e56']}/{i['e57']}/{i['e58']}/{i['e59']}/"
            f"{i['e60']}/{i['f1']}/{i['f2']}/{i['f3']}/{i['f4']
                                                        }/{i['f5']}/{i['f6']}/{i['f7']}/{i['f8']}/"
            f"{i['f9']}/{i['g1']}/{i['g2']}/{i['h1']}/{i['h2']
                                                       }/{i['i1']}/{i['i2']}/{i['j1']}/{i['j2']}/"
            f"{i['j3']}\n"
        )
        if i['lyric3'] != '':
            body.append(
                f"{i['section']}/{i['lyric3']}//{i['p1']}/{i['p2']
                                                           }/{i['p3']}/{i['p4']}/{i['p5']}/{i['p6']}/"
                f"{i['p7']}/{i['p8']}/{i['p9']}/{i['p10']
                                                 }/{i['p11']}/{i['p12']}/{i['p13']}/{i['p14']}/"
                f"{i['p15']}/{i['p16']}/{i['a1']}/{i['a2']
                                                   }/{i['a3']}/{i['a4']}/{i['a5']}/{i['b1']}/"
                f"{i['b2']}/{i['b3']}/{i['b4']}/{i['b5']}/{i['c1']
                                                           }/{i['c2']}/{i['c3']}/{i['c4']}/{i['c5']}/"
                f"{i['d1']}/{i['d2']}/{i['d3']}/{i['d4']}/{i['d5']
                                                           }/{i['d6']}/{i['d7']}/{i['d8']}/{i['d9']}/"
                f"{i['e1']}/{i['e2']}/{i['e3']}/{i['e4']}/{i['e5']
                                                           }/{i['e6']}/{i['e7']}/{i['e8']}/{i['e9']}/"
                f"{i['e10']}/{i['e11']}/{i['e12']}/{i['e13']
                                                    }/{i['e14']}/{i['e15']}/{i['e16']}/{i['e17']}/"
                f"{i['e18']}/{i['e19']}/{i['e20']}/{i['e21']
                                                    }/{i['e22']}/{i['e23']}/{i['e24']}/{i['e25']}/"
                f"{i['e26']}/{i['e27']}/{i['e28']}/{i['e29']
                                                    }/{i['e30']}/{i['e31']}/{i['e32']}/{i['e33']}/"
                f"{i['e34']}/{i['e35']}/{i['e36']}/{i['e37']
                                                    }/{i['e38']}/{i['e39']}/{i['e40']}/{i['e41']}/"
                f"{i['e42']}/{i['e43']}/{i['e44']}/{i['e45']
                                                    }/{i['e46']}/{i['e47']}/{i['e48']}/{i['e49']}/"
                f"{i['e50']}/{i['e51']}/{i['e52']}/{i['e53']
                                                    }/{i['e54']}/{i['e55']}/{i['e56']}/{i['e57']}/"
                f"{i['e58']}/{i['e59']}/{i['e60']}/{i['f1']}/{i['f2']
                                                              }/{i['f3']}/{i['f4']}/{i['f5']}/{i['f6']}/"
                f"{i['f7']}/{i['f8']}/{i['f9']}/{i['g1']}/{i['g2']
                                                           }/{i['h1']}/{i['h2']}/{i['i1']}/{i['i2']}/"
                f"{i['j1']}/{i['j2']}/{i['j3']}\n"
            )

        if i['lyric4'] != '':
            body.append(
                f"{i['section']}/{i['lyric4']}//{i['p1']}/{i['p2']
                                                           }/{i['p3']}/{i['p4']}/{i['p5']}/{i['p6']}/"
                f"{i['p7']}/{i['p8']}/{i['p9']}/{i['p10']
                                                 }/{i['p11']}/{i['p12']}/{i['p13']}/{i['p14']}/"
                f"{i['p15']}/{i['p16']}/{i['a1']}/{i['a2']
                                                   }/{i['a3']}/{i['a4']}/{i['a5']}/{i['b1']}/"
                f"{i['b2']}/{i['b3']}/{i['b4']}/{i['b5']}/{i['c1']
                                                           }/{i['c2']}/{i['c3']}/{i['c4']}/{i['c5']}/"
                f"{i['d1']}/{i['d2']}/{i['d3']}/{i['d4']}/{i['d5']
                                                           }/{i['d6']}/{i['d7']}/{i['d8']}/{i['d9']}/"
                f"{i['e1']}/{i['e2']}/{i['e3']}/{i['e4']}/{i['e5']
                                                           }/{i['e6']}/{i['e7']}/{i['e8']}/{i['e9']}/"
                f"{i['e10']}/{i['e11']}/{i['e12']}/{i['e13']
                                                    }/{i['e14']}/{i['e15']}/{i['e16']}/{i['e17']}/"
                f"{i['e18']}/{i['e19']}/{i['e20']}/{i['e21']
                                                    }/{i['e22']}/{i['e23']}/{i['e24']}/{i['e25']}/"
                f"{i['e26']}/{i['e27']}/{i['e28']}/{i['e29']
                                                    }/{i['e30']}/{i['e31']}/{i['e32']}/{i['e33']}/"
                f"{i['e34']}/{i['e35']}/{i['e36']}/{i['e37']
                                                    }/{i['e38']}/{i['e39']}/{i['e40']}/{i['e41']}/"
                f"{i['e42']}/{i['e43']}/{i['e44']}/{i['e45']
                                                    }/{i['e46']}/{i['e47']}/{i['e48']}/{i['e49']}/"
                f"{i['e50']}/{i['e51']}/{i['e52']}/{i['e53']
                                                    }/{i['e54']}/{i['e55']}/{i['e56']}/{i['e57']}/"
                f"{i['e58']}/{i['e59']}/{i['e60']}/{i['f1']}/{i['f2']
                                                              }/{i['f3']}/{i['f4']}/{i['f5']}/{i['f6']}/"
                f"{i['f7']}/{i['f8']}/{i['f9']}/{i['g1']}/{i['g2']
                                                           }/{i['h1']}/{i['h2']}/{i['i1']}/{i['i2']}/"
                f"{i['j1']}/{i['j2']}/{i['j3']}\n"
            )

    # 配列を無くす
    body2 = ''
    for bod in body:
        body2 = f"{body2}{bod}"
        # print (bod)

    # print (body2)

    # ファイル名から拡張子と_tempを抜いて拡張子ustparamを足す
    ustparam_path = os.path.splitext(ustpath)[0]
    # print (ustparam_path)
    # _tempを消す
    if ustparam_path.endswith('_temp'):
        ustparam_path = ustparam_path[:-len('_temp')]
    # ustparam_path = ustparam_path.rstrip('_temp')
    # print (ustparam_path)
    ustparam_path = ustparam_path + '.ustparam'

    # ustparam保存
    with open(ustparam_path, 'w') as f:
        f.write(body2)

    # フラグにp9の値を入れる
    for i, note in enumerate(ust.notes):
        note.flags = new_array[i]['p9']
        # print(note.flag)

    # USTを保存
    ust.write(ustpath)
    return cnt3, ustparam_path


if __name__ == "__main__":
    print('flag separator.py--------------------------------------')
    _cnt3, _ustparam_path = main()
    print(f"{_cnt3}行分のなんかよくわからん物を下記のパスに保存したゼ！")
    print(_ustparam_path)
    print('-------------------------------------------------------')
