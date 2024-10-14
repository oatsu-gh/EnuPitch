# EnuPitch

ピッチを自動生成するUTAUプラグイン

## 使い方

1. ノートを範囲選択してプラグインを起動してください。

## 利用規約

同梱の LICENSE ファイルをご覧ください。

## 更新履歴

### v0.0.1

- 配布開始
- 配布動画： https://www.nicovideo.jp/watch/sm40920519

### v0.1.0

- 休符前でピッチが下がるのを直す機能を追加

### v0.2.0

- 使用モデルを「波音リツ CRISSCROSS 6style world-diffusion HN-uSFGAN NNSVS/ENUNU hed418 BEATテスト #4320」に変更
  - flag_separator.py を改造し、モデルのフォルダに flag_separator_for_enupitch.py を配置しています。
- 歌唱スタイル指定用の拡張機能 enupitch_launcher_with_flet.py を追加
- ほか、複数の拡張機能を追加
- 同梱の python を 3.12.7 に更新
- pytorch のインストールに light-the-torch を使うようにした

## Python-Embed 環境構築のメモ

### python-3.12.7-embed-amd64 での環境構築手順

- pysptk をインストールするときに dll とか h ファイルとかが必要なので、インストール版の Python からコピーする。(2024/10/14)
  - python/include/  → python-embeddable/include/
  - python/libs/  → python-embeddable/libs/
- pysptk をインストールするときと uSFGAN を使うときに tcl/tk が必要なので、インストール版の Python から下記内容でコピーして対処。(2024/10/14)
  - python/tcl/  → python-embeddable/tcl/
  - python/Lib/tkinter/ → python/tkinter/
  - python/DLLs/\_tkinter.pyd → python-embeddable/\_tkinter.pyd 
  - python/DLLs/tcl86t.dll → python-embeddable/tcl86t.dll
  - python/DLLs/tk86t.dll→ python-embeddable/tk86t.dll 
  - python/DLLs/zlib1.dll → python-embeddable/zlib1.dll

- `python ./get-pip.py --no-warn-script-location`
- `python -m pip install -r requirements.txt --no-warn-script-location`
- nnsvs をダウンロード (https://github.com/nnsvs/nnsvs)
- uSFGAN は HN-UnifiedSourceFilterGAN-nnsvs を DL
- ParallelWaveGAN は ParallelWaveGAN-nnsvs をDL (https://github.com/nnsvs/ParallelWaveGAN)
- SiFiGAN は SiFiGAN-nnsvs を DL (https://github.com/nnsvs/SiFiGAN)
  - pip で python embeddable に SiFiGAN をインストールする場合は docopt が無いとエラーが出るので、インストール版の Python から docopt をコピーして対処。(2024/05/19)

## 連絡先

CrazY ( https://twitter.com/crazy_toho )
