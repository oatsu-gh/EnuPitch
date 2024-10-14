#!/usr/bin/env python3
# Copyright (c) 2024 oatsu
"""
GUI 表示するライブラリである flet の練習。
EnuPitchのリツモデル用にフラグをなんかいろいろやる

# 強弱
Loudest : 0-3
Loud    : 0-3
Normal  : 0-3
Soft    : 0-3
どれかを3にして他を0にするのがいいらしい。ラジオボックスにすると良さそう。
何もしなかったら Loud 3 らしい。

# スタイル
Standard: 0-3
Sweet   : 0-3
Rock    : 0-3
Breathy : 0-6
Pop     : 0-3
Growl   : 0-3
強弱と相性があるらしいけどEnuPitch的には気にしないでいいと思ってるので、ラジオボックスで実装する。
何もしなかったら Standard 3 らしい。


## リツのREADMEの抜粋
> ◆◆強弱、スタイルの使用方法
>
>     まず、フラグの先頭には!を付けてください、簡易入力モードになります
>
>     ◆強弱の設定方法
>
>         強弱は!のあとに続けて4桁の数字を入力します
>         各桁はそれぞれLoudest, Loud, normal, softに対応しており、それぞれ0～3の数字を入れることができます
>         数字が大きいほど声が強くなるというわけではなく、特徴が強く出るようになります
>         例えばsoftは弱い声が特徴なので、1より3のほうが弱くなります
>         0030, 0200, 0003のように１つの数字だけを上げて、他の３つを0にしておく方が安定しますが、0220のように混ぜて使うこともできます
>         必要に応じて調整してください
>
>     ◆スタイルの設定方法
>
>         スタイルは現在Standard, Sweet, Rock, Breathy, Pop, Growlの6種類を利用できます
>         Breathyを除く各フラグを0～3まで設定することができます
>         breathyのみ0～6まで設定可能です
>         書式は、強弱の数値に続けてスタイル名の頭2文字＋フラグの強さの数字を入れます（大文字小文字の区別をしません）
>         例: !0030po3ro1　（強さNormal 3, スタイル Pop 3, rock 1）
>
>     ※フラグは未入力だとStandardスタイルの強さ0300になります
>
>     ◆おまけ
>
>         フラグは大文字小文字の区別をしません 　（例: !0030Po1RO3bR1）
>         スタイル指定の順番は自由です
>         スタイル指定は頭文字1文字でも可能ですが、sはstandardになるため、Sweetの指定はswが最短です　（例: !0220P3s1Sw1）
>         スペースや記号は無視されるため入れても問題ありません　（例: !3100 P3/R1）
>         スタイルはそれぞれ得意な強弱があり、
>         Pop は Normal
>         rock は Loud, Loud
>         sweet は Soft, Normal
>         Breathy は Soft, Normal
>         Growl は Loud
>         Standard は全て得意です

"""
import re
from argparse import ArgumentParser

import flet as ft
import utaupy

LOUDNESS_DICT = {
    'Loudest': '3000',
    'Loud': '0300',
    'Normal': '0030',
    'Soft': '0003'
}

STYLE_DICT = {
    'Standard': 'standard3',
    'Sweet': 'sweet3',
    'Rock': 'rock3',
    'Breathy': 'breathy6',
    'Pop': 'pop3',
    'Growl': 'growl3'
}


def edit_ust_flags(loudness: str, style: str, style_shift_amount: str):
    """USTファイルのフラグに追記する
    """
    parser = ArgumentParser()
    parser.add_argument('--ust', help='選択部分のノートのUSTファイルのパス')
    parser.add_argument('--f0', help='f0の情報を持ったCSVファイルのパス')
    parser.add_argument('--full_timing', help='タイミング推定済みのフルラベルファイルのパス')

    # 使わない引数は無視して、必要な情報だけ取り出す。
    args, _ = parser.parse_known_args()
    path_ust = args.ust

    # 追記するフラグを決める
    flags = \
        f'S{style_shift_amount}!{LOUDNESS_DICT[loudness]}{STYLE_DICT[style]}'
    print('Style shift amount :', style_shift_amount)
    print('Selected loudness  :', loudness)
    print('Seledted style     :', style)
    print('Generated flag     :', flags)

    # USTを読み込み
    ust = utaupy.ust.load(path_ust)
    # USTのフラグを編集
    for note in ust.notes:
        note.flags = f'{note.flags}{flags}'
        # USTファイルを上書き
    ust.write(path_ust)


def flet_ui(page: ft.Page):
    """全体の処理をする
    """

    def launch_button_clicked(_):
        launch_button.disabled = True
        launch_button.text = 'Running...'
        launch_button.update()
        edit_ust_flags(loudness=loudness.value,
                       style=style.value,
                       style_shift_amount=style_shift_amount.value)
        page.window.close()

    page.window.center()
    page.title = 'EnuPitch Style Selector'
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 640
    page.window.height = 540
    page.window.minimizable = True  # 最小化ボタン
    page.window.maximizable = False  # 最大化ボタン
    page.window.resizable = True  # ウィンドウサイズ変更可否

    # 歌唱スタイルの選択用 ラジオボックス
    loudness = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="Loudest", label="Loudest",
                         active_color=ft.colors.PINK),
                ft.Radio(value="Loud", label="Loud",
                         active_color=ft.colors.PINK),
                ft.Radio(value="Normal", label="Normal",
                         active_color=ft.colors.PINK),
                ft.Radio(value="Soft", label="Soft",
                         active_color=ft.colors.PINK),
            ],
            alignment=ft.MainAxisAlignment.START
        ),
        value='Loud'
    )

    # 歌唱スタイルの選択用 ラジオボックス
    style = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="Standard", label="Standard",
                         active_color=ft.colors.BLUE),
                ft.Radio(value="Sweet", label="Sweet",
                         active_color=ft.colors.RED),
                ft.Radio(value="Rock", label="Rock",
                         active_color=ft.colors.PURPLE),
                ft.Radio(value="Breathy", label="Breathy",
                         active_color=ft.colors.ORANGE),
                ft.Radio(value="Pop", label="Pop",
                         active_color=ft.colors.PINK),
                ft.Radio(value="Growl", label="Growl",
                         active_color=ft.colors.TEAL),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        value='Standard',
    )

    style_shift_amount = ft.TextField(
        value="0", text_align="center", width=100)

    # スタイルシフトの量を指定するUi
    style_shift_selector = ft.CupertinoSlidingSegmentedButton(
        selected_index=6,
        thumb_color=ft.colors.GREY_50,
        # on_change=lambda e: print(f"selected_index: {e.data}"),
        padding=ft.padding.symmetric(0, 10),
        controls=[
            ft.Text("-6"),
            ft.Text("-5"),
            ft.Text("-4"),
            ft.Text("-3"),
            ft.Text("-2"),
            ft.Text("-1"),
            ft.Text("0"),
            ft.Text("+1"),
            ft.Text("+2"),
            ft.Text("+3"),
            ft.Text("+4"),
            ft.Text("+5"),
            ft.Text("+6"),
        ],
    )

    # 閉じてEnuPitchをの処理を再開するボタン
    launch_button = ft.ElevatedButton(
        text='Run EnuPitch',
        on_click=launch_button_clicked,
        width=240
    )

    # ここからUI配置 -----------------------------------------
    page.add(
        ft.Container(
            ft.Column([
                ft.Text('1. Select loudness (強弱)'),
                ft.Card(
                    ft.Container(
                        loudness,
                        width=600,
                        height=60,
                        padding=10
                    )
                ),
                ft.Text('\n2. Select style (スタイル)'),
                ft.Card(
                    ft.Container(
                        style,
                        width=600,
                        height=60,
                        padding=10
                    )
                ),
                ft.Text('\n3. Style shift amount (スタイルシフト)'),
                ft.Card(
                    ft.Container(
                        style_shift_selector,
                        width=600,
                        height=60,
                        padding=10
                    )
                ),
                ft.Text('\n4. Run EnuPitch (実行)'),
                launch_button
            ]),
            width=640,
            padding=10
        ),
    )
    # ここまでUI配置 -----------------------------------------


if __name__ == "__main__":
    print('style_selector_with_flet.py (2024-10-06) --------------')
    ft.app(target=flet_ui)
    print('-------------------------------------------------------')
