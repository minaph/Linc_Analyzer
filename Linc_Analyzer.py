# 前回の方法がめんどくさかったので、アルゴリズム的に解く。

'''

解法

全ファイルデータを取得
「ループ開始」
検索位置直近の英字位置を取得
かぎかっこ開始がすぐ近くにあるか検証（あったら英単語として認定、なければ直近の非英字位置に検索位置を更新しループに戻る）
検索位置直近の非英字位置を取得
英字開始～終了までを英単語として記録
直後のかぎかっこ終了位置を取得
かぎかっこ開始から終了までをそのp英単語の定義として取得
「ループ終了」
英単語と定義を並べて表示

結局、「かぎかっこ開始がすぐ近く」であることの定義が非情に面倒だった…

多かったミス
ループでの初期化し忘れ


'''

# appendに問題があるようだが…

import codecs

# 全ファイルデータ取得

FILE_IN = "資料.txt"  # 検索対象のファイル（固定）
result = []  # 結果の格納先
result2 = []
f = codecs.open(FILE_IN, 'r', 'utf-8')  # utf-8でファイルデータ取得
index = 0  # 検索位置
word_end = 0  # 英単語終了位置
k = 200  # 直近の定義
def_s = 0  # 定義開始位置
def_e = 0  # 定義終了位置
p = 0  # 仮の変数


# def is_japanese(string):
#     for ch in string:
#         name = unicodedata.name(ch)
#         if "CJK UNIFIED" in name \
#         or "HIRAGANA" in name \
#         or "KATAKANA" in name:
#             return True
#     return False

# 半角判別関数

def halfletters(strings):
    ch = ""
    for ch in strings:
        if ch.encode("utf-8").isalnum() or ch == " " or ch == "-" or ch == "'" or ch == "~" or ch == ",":
            continue
        else:
            return False
    return True

# 別のさらにふさわしい英単語が混在していないか簡単にチェック
# (かぎかっこ開始と検索カーソルとの間に全角に挟まれた半角文字があれば、取得位置の英単語は不適とした)


def h_l(strings):
    bank = " "
    for ch in strings:
        if halfletters(bank) == False and halfletters(ch) == True:
            return False
        else:
            bank = ch
    return True


# ループ開始
# 条件分岐にいろいろつっこみすぎて可読性最悪

for line in f:
    index = 0
    while index <= len(line):
        if halfletters(line[index:index+1]) and line[index:index+1] != " " and line[index:index+1].encode("utf-8").isdigit() != True:
            if (line[index+1:].find("「") <= k and line[index+1:].find("「") != -1) and h_l(line[index+1:index+1+line[index+1:].find("「")]):
                p = index
                word_end = index
                while p <= len(line):
                    word_end += 1
                    p += 1
                    if halfletters(line[index:word_end]):
                        continue
                    else:
                        p += len(line)
                else:
                    if word_end-1-index >= 2:
                        result.append(line[index:word_end-1])
                    else:
                        index += 1
                        continue
                def_s = line[index+1:].find("「")
                def_e = line[index+1:].find("」")
                if def_e == -1:
                    index += 1
                else:
                    result2.append(line[index+1+def_s+1:index+1+def_e])
                    index = def_e+index+1
                continue
            else:
                index += 1
                continue
        else:
            index += 1
            continue

for i in range(int(len(result)/2)):
    print(result[i], end='/')
    print(result2[i])
