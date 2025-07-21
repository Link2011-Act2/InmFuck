# -*- coding: utf-8 -*-
import sys
import os

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
BF_TO_INMU = {v: k for k, v in INMU_TO_BF.items()}

def inmu_to_brainfuck(code):
    bf = ''
    index = 0
    unknown_count = 0
    while index < len(code):
        matched = False
        for phrase in sorted(INMU_TO_BF.keys(), key=len, reverse=True):
            if code.startswith(phrase, index):
                bf += INMU_TO_BF[phrase]
                index += len(phrase)
                matched = True
                break
        if not matched:
            print(f"⚠ 未定義語録: {code[index:index+10]}")
            unknown_count += 1
            index += 1
    if unknown_count:
        print(f"⚠ 合計 {unknown_count} 件の未定義語録が検出されました")
    return bf

def brainfuck_to_inmu(code):
    result = ''
    for c in code:
        if c in BF_TO_INMU:
            result += BF_TO_INMU[c]
        else:
            print(f"⚠ 無効なBrainfuck命令: {c}")
    return result

def build_bracket_map(code):
    bracket_map = {}
    stack = []
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

def brainfuck_interpreter(code, input_func=input):
    tape = [0] * 30000
    ptr = 0
    pc = 0
    code_len = len(code)

    bracket_map = build_bracket_map(code)

    while pc < code_len:
        cmd = code[pc]
        if cmd == '>':
            ptr = (ptr + 1) % len(tape)
        elif cmd == '<':
            ptr = (ptr - 1) % len(tape)
        elif cmd == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '.':
            print(chr(tape[ptr]), end='')
        elif cmd == ',':
            try:
                inp = input("Input (1文字): ")
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

def main():
    print("モードを選んでください:")
    print("1: InmFuckを実行する")
    print("2: InmFuck → Brainfuck変換")
    print("3: Brainfuck → InmFuck変換")
    mode = input("番号を入力してください (1-3): ").strip()

    if mode not in ('1', '2', '3'):
        print("⚠ 無効な入力です。終了します。")
        sys.exit(1)

    if len(sys.argv) >= 2:
        input_path = sys.argv[1]
        print(f"入力ファイル: {input_path}")
    else:
        input_path = input("入力ファイルのパスを入力してください: ").strip()

    if not os.path.isfile(input_path):
        print("⚠ ファイルが存在しません。終了します。")
        sys.exit(1)

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            code = f.read().strip()
        if not code:
            print("⚠ ファイル内容が空です。終了します。")
            sys.exit(1)
    except Exception as e:
        print(f"⚠ ファイル読み込み中にエラーが発生しました: {e}")
        sys.exit(1)

    try:
        if mode == '1':
            bf_code = inmu_to_brainfuck(code)
            brainfuck_interpreter(bf_code)
        elif mode == '2':
            bf_code = inmu_to_brainfuck(code)
            build_bracket_map(bf_code)  # 構文チェック
            print("=== 変換結果（Brainfuck） ===")
            print(bf_code)
            save_path = input("変換結果の保存先ファイル名を入力してください (.bf推奨): ").strip()
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(bf_code)
                print(f"変換結果を保存しました: {save_path}")
            else:
                print("⚠ 保存先が指定されませんでした。")
        else:
            # Brainfuck → HomoFuck
            for c in code:
                if c not in BF_TO_INMU:
                    print(f"⚠ 無効なBrainfuck命令: {c}")
            inmu_code = brainfuck_to_inmu(code)
            print("=== 変換結果（InmFuck） ===")
            print(inmu_code)
            save_path = input("変換結果の保存先ファイル名を入力してください (.inm推奨): ").strip()
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(inmu_code)
                print(f"変換結果を保存しました: {save_path}")
            else:
                print("⚠ 保存先が指定されませんでした。")

    except SyntaxError as e:
        print(f"⚠ 構文エラー: {e}")
    except Exception as e:
        print(f"⚠ 実行時にエラーが発生しました: {e}")

if __name__ == "__main__":
    main()
