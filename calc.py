import PySimpleGUI as sg
from decimal import Decimal, ROUND_HALF_UP


# s1→s2で増えた部分だけ返す
def str_diff(s1, s2):
    for c in s1:
        s2 = s2.replace(c, "", 1)
    return s2


def calc(flag, num1, symbol):
    global value
    # キーボード入力かGUI入力かで処理を分ける
    if flag == "values":
        num2 = float(value[:-1])
    else:
        num2 = float(value)

    if num2.is_integer():
        num2 = int(num2)

    # 計算処理
    if symbol == "+" or symbol == "":
        num1 += num2
    elif symbol == "-":
        num1 -= num2
    elif symbol in ("*", "×"):
        num1 *= num2
    elif symbol in ("/", "÷"):
        num1 /= num2

    if isinstance(num1, int):
        pass
    elif num1.is_integer():
        num1 = int(num1)
    else:
        # num1 = round(num1, 8)
        num1 = float(Decimal(str(num1)).quantize(
            Decimal("0.0000000001"), rounding=ROUND_HALF_UP))
    return num1, num2


# 算術演算子(+-*/)によって式がまだ続く場合の計算
def symbol_calc(flag):
    global value
    global window
    global symbol_flag
    global symbol
    global num1
    global num2
    global event

    # 直前の入力が算術演算子の時(計算式の算術演算子だけ書き換える処理)
    if symbol_flag:
        # キーボード入力かGUI入力かで処理を分ける
        if flag == "values":
            symbol = value[-1]
        else:
            symbol = event
        # 計算式を書き替え
        window["formula"].update(
            layout[0][0].DisplayText[:-1] + symbol)
        # 算術演算子を表示させないように数値のみに置き換える
        window["input"].update(str(num1))

    # 直前の入力が算術演算子ではないとき(数値の時)
    else:
        # 何も押されずに算術演算子だけ押された場合は0を入れる
        if (flag == "values" and value[:-1] == "") or value == "":
            value = "0" + value[-1]
        # 値がリセットされているor最初の算術演算子入力の場合
        if num1 == 0:
            # キーボード入力かGUI入力かで処理を分ける
            if flag == "values":
                # キーボード入力の場合はテキストボックスの中に算術演算子が入っているため、
                # それを算術演算子と数値に分ける
                symbol = value[-1]
                num1 = float(value[:-1])
            else:
                # GUI入力の場合はテキストボックスの中が数値のみで
                # 算術演算子はeventに入っている
                symbol = event
                num1 = float(value)
            # floatにしているのは入っている数値が小数の可能性があるため

            if num1.is_integer():
                # 整数の場合はintに変換する
                num1 = int(num1)
            else:
                # 小数の場合は10桁で丸める
                num1 = float(Decimal(str(num1)).quantize(
                    Decimal("0.0000000001"), rounding=ROUND_HALF_UP))

            # 入力数値を表示(算術演算子を表示させない)
            window["input"].update(str(num1))
            symbol_flag = True  # 直前の入力が算術演算子のときTrue
            # 計算式を表示
            window["formula"].update(str(num1) + symbol)
        # リセット後2回目以降の算術演算子入力の場合(計算をする)
        else:
            # 計算処理
            num1, num2 = calc(flag, num1, symbol)

            # num1に計算結果が入っているため、それを表示
            window["input"].update(str(num1))

            # キーボード入力かGUI入力かで処理を分ける
            # ここでは次の計算用にsymbolに入力された算術演算子を入れている
            if flag == "values":
                symbol = value[-1]
            else:
                symbol = event

            symbol_flag = True
            # 計算式を表示
            window["formula"].update(str(num1) + symbol)


def equal_calc(flag):
    global value
    global window
    global symbol_flag
    global symbol
    global num1
    global num2
    global event

    # 計算処理
    num1, num2 = calc(flag, num1, symbol)

    # 計算式を表示
    # layout[0][0].DisplayTextは1行目に表示されている内容が入っている
    window["formula"].update(
        layout[0][0].DisplayText + str(num2) + "=")

    # num1に計算結果が入っているため、それを表示
    window["input"].update(str(num1))
    symbol = "="
    # =は算術演算子ではないのでFalseにする
    symbol_flag = False


if __name__ == "__main__":
    sg.theme("Black")

    # ボタンのサイズを変数で定義
    key_size = (4, 2)
    # レイアウト設定
    layout = [
        # 計算式を表示する場所
        [sg.Text("", size=(19, 1), font=("メイリオ", 8), key="formula")],
        # 入力欄(enable=Trueで1文字入力するたびにeventが発生するようにしている)
        [sg.InputText("", size=(19, 1), font=("メイリオ", 12),
                      key="input", enable_events=True)],
        # 以下入力ボタン
        [sg.Button("CE", size=key_size), sg.Button("C", size=key_size),
         sg.Button("BS", size=key_size), sg.Button("÷", size=key_size)],
        [sg.Button("7", size=key_size), sg.Button("8", size=key_size),
         sg.Button("9", size=key_size), sg.Button("×", size=key_size)],
        [sg.Button("4", size=key_size), sg.Button("5", size=key_size),
         sg.Button("6", size=key_size), sg.Button("-", size=key_size)],
        [sg.Button("1", size=key_size), sg.Button("2", size=key_size),
         sg.Button("3", size=key_size), sg.Button("+", size=key_size)],
        [sg.Button("0", size=key_size), sg.Button(".", size=key_size),
         sg.Button("+/-", size=key_size), sg.Button("=", size=key_size)]
    ]
    # ウィンドウ名とレイアウトを指定
    window = sg.Window("電卓", layout, finalize=True)
    # Enterを入力として処理するための設定
    # これをしないとEnter入力しても何も起こらない
    window['input'].bind("<Return>", "_Enter")

    # 使う変数の初期化
    num1 = 0
    num2 = 0
    symbol = ""
    symbol_flag = False
    call_flag = ""

    while True:
        # eventが発生するまで待つ
        # ボタンを押したりキーボードで入力したりするとeventが発生する
        # eventには、ボタンが押された場合はボタン名が(CE,C等)、
        # キーボード入力されたらinput、Enterが押されたらinput_Enterが入る
        event, values = window.read()

        # ×が押された時の処理
        if event is None:
            break

        # 入力内容をvalueに格納
        value = values["input"]

        # Enterが押された場合
        if event == "input_Enter":
            # 計算終了直後に押された場合
            if symbol == "=":
                symbol = ""
                window["input"].update(value)
                window["formula"].update("")

            call_flag = "enter"
            equal_calc(call_flag)

        # キーボードで入力された場合(BackSpaceキーやDeleteキーも含む)
        if event == "input":
            # 値がなく空になった場合はスルー
            if not value:
                continue

            # qを押すとClearと同じ動作
            if value[-1] == "q":
                num1 = 0
                symbol = ""
                window["input"].update("")
                window["formula"].update("")
                symbol_flag = False
                continue
            # 数値・算術演算子・小数点・q以外の文字が入力された場合は無視する
            elif (not value[-1].isdecimal()) and (not value[-1] in (".", "+", "-", "*", "/")):
                print("認識できない文字入力")
                window["input"].update(value[:-1])
                continue

            # 計算終了後("="入力後)に数値か小数点が入力された時
            # 入力欄の数値を今入力したものだけにして、計算式表示はリセット
            if symbol == "=" and (not value[-1] in ("+", "-", "*", "/") and value != str(num1)):
                symbol = ""
                # 入力値だけを格納
                diff = str_diff(str(num1), value)
                if diff == ".":
                    window["input"].update("0" + diff)
                else:
                    window["input"].update(diff)
                symbol_flag = False
                # num1をリセット
                num1 = 0
                continue

            # 算術演算子が入力されたら
            elif value[-1] in ("+", "-", "*", "/"):

                call_flag = "values"
                symbol_calc(call_flag)
                continue

            # 算術演算子の後最初の入力の場合
            elif symbol_flag and value != str(num1):
                # 入力値だけを格納
                diff = str_diff(str(num1), value)
                if diff == ".":
                    window["input"].update("0" + diff)
                else:
                    window["input"].update(diff)
                symbol_flag = False
                continue

            elif value[-1] == "=":
                call_flag = "values"
                equal_calc(call_flag)
                continue

            # 何も数値を入れていないときに小数点が入力されたら小数点前に0を追加する
            if value == ".":
                window["input"].update("0.")
            # 小数点が2個目の場合
            elif value.count(".") == 2:
                print("二つ以上の小数点")
                window["input"].update(value[:-1])

        # ---ここからボタンの処理---

        # BackSpace 一文字消す
        if event == "BS":
            if value != "":
                window["input"].update(value[:-1])

        # Clear クリア
        if event == "C":
            num1 = 0
            symbol = ""
            window["input"].update("")
            window["formula"].update("")
            symbol_flag = False

        # Clear Entry 入力文字だけクリア
        if event == "CE":
            window["input"].update("")

        # 算術演算子ボタン 計算
        if event in ("+", "-", "×", "÷"):
            call_flag = "event"
            symbol_calc(call_flag)

        # =ボタン 計算
        if event == "=":
            # 連続で押された場合
            if symbol == "=":
                symbol = ""
                window["input"].update(value)
                window["formula"].update("")
            call_flag = "event"
            equal_calc(call_flag)

        # 数値ボタン
        if event in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            # 計算終了後("="入力後)に数値か小数点が入力された時
            # 入力欄の数値を押されたボタンの数値だけにして、計算式表示はリセット
            if symbol == "=":
                symbol = ""
                window["input"].update(event)
                window["formula"].update("")
            # 算術演算子の後最初の入力の場合
            elif symbol_flag:
                window["input"].update(event)
                symbol_flag = False
            # その他の場合はそのまま入力欄の後ろに数値を入れる
            else:
                window["input"].update(value + event)

        # 小数点ボタン すでに小数点がある場合は何もしない
        if event == ".":
            if "." in value:
                pass
            else:
                window["input"].update(value + ".")

        # ±ボタン -を付けたり外したりする
        if event == "+/-":
            if "-" in value:
                window["input"].update(value.replace("-", ""))
            else:
                window["input"].update("-" + value)
