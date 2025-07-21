# -*- coding: utf-8 -*-

INMU_TO_BF = {
    'やりますねぇ！': '+',
    '王道を征く': '-',
    'ンアッー！': '>',
    'イキスギィ！': '<',
    'で、出ますよ': '.',
    'ファッ！？': ',',
    'まずうちさぁ': '[',
    '屋上あんだけど': ']',
}

def parse_Inmfuck(code):
    tokens = []
    index = 0
    unknown_count = 0
    while index < len(code):
        matched = False
        for phrase in sorted(INMU_TO_BF.keys(), key=len, reverse=True):
            if code.startswith(phrase, index):
                tokens.append(INMU_TO_BF[phrase])
                index += len(phrase)
                matched = True
                break
        if not matched:
            print(f"⚠ 未定義語録: {code[index:index+10]}")
            unknown_count += 1
            index += 1
    if unknown_count:
        print(f"⚠ 合計 {unknown_count} 件の未定義語録が検出されました")
    return ''.join(tokens)

def build_bracket_map(code):
    stack = []
    bracket_map = {}
    for i, c in enumerate(code):
        if c == '[':
            stack.append(i)
        elif c == ']':
            if not stack:
                raise SyntaxError(f"対応していない ']' が位置 {i} にあります")
            start = stack.pop()
            bracket_map[start] = i
            bracket_map[i] = start
    if stack:
        raise SyntaxError(f"対応していない '[' が位置 {stack[-1]} にあります")
    return bracket_map

def run_homofuck(code):
    bf_code = parse_Inmfuck(code)
    tape = [0] * 30000
    ptr = 0
    pc = 0
    bracket_map = build_bracket_map(bf_code)
    length = len(bf_code)

    while pc < length:
        cmd = bf_code[pc]
        if cmd == '>':
            ptr += 1
            if ptr >= len(tape):
                ptr = 0
        elif cmd == '<':
            ptr -= 1
            if ptr < 0:
                ptr = len(tape) - 1
        elif cmd == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '.':
            print(chr(tape[ptr]), end='')
        elif cmd == ',':
            try:
                inp = input("Input: ")
                tape[ptr] = ord(inp[0]) if inp else 0
            except EOFError:
                print("\n⚠ 入力が予期せず終了しました。0を代入します。")
                tape[ptr] = 0
            except Exception as e:
                print(f"\n⚠ 入力処理中にエラーが発生しました: {e}\n0を代入します。")
                tape[ptr] = 0
        elif cmd == '[':
            if tape[ptr] == 0:
                pc = bracket_map[pc]
        elif cmd == ']':
            if tape[ptr] != 0:
                pc = bracket_map[pc]
        pc += 1

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("⚠ エラー: 入力ファイルが指定されていません。")
        print("使い方: python InmFuckInterpreter.py [input.inm]")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, "r", encoding="utf-8") as f:
            homofuck_code = f.read()
        if not homofuck_code.strip():
            print("⚠ エラー: ファイルが空です。")
            sys.exit(1)
    except FileNotFoundError:
        print(f"⚠ エラー: ファイルが見つかりません: {filename}")
        sys.exit(1)
    except PermissionError:
        print(f"⚠ エラー: ファイルを開く権限がありません: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"⚠ エラー: ファイル読み込み時に予期せぬエラーが発生しました: {e}")
        sys.exit(1)

    try:
        run_homofuck(homofuck_code)
    except SyntaxError as e:
        print(f"\n⚠ 構文エラー: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n⚠ 実行中にエラーが発生しました: {e}")
        sys.exit(1)
