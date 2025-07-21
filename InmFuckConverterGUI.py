# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

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
    warnings = []
    while index < len(code):
        matched = False
        for phrase in sorted(INMU_TO_BF.keys(), key=len, reverse=True):
            if code.startswith(phrase, index):
                bf += INMU_TO_BF[phrase]
                index += len(phrase)
                matched = True
                break
        if not matched:
            warnings.append(f"⚠ 未定義語録: {code[index:index+10]}")
            index += 1
    if warnings:
        messagebox.showwarning("未定義語録あり", "\n".join(warnings))
    return bf

def brainfuck_to_inmu(code):
    result = ''
    for c in code:
        if c in BF_TO_INMU:
            result += BF_TO_INMU[c]
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

def brainfuck_interpreter(code, input_func=None):
    root = tk.Tk()
    root.withdraw()

    tape = [0] * 30000
    ptr = 0
    pc = 0
    output = ''
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
            output += chr(tape[ptr])
        elif cmd == ',':
            try:
                s = simpledialog.askstring("入力待ち", "1文字入力してください（キャンセルで0）:")
                if s and len(s) > 0:
                    tape[ptr] = ord(s[0])
                else:
                    tape[ptr] = 0
            except Exception:
                tape[ptr] = 0
        elif cmd == '[':
            if tape[ptr] == 0:
                pc = bracket_map[pc]
        elif cmd == ']':
            if tape[ptr] != 0:
                pc = bracket_map[pc]
        pc += 1

    root.destroy()
    return output

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    mode = simpledialog.askstring(
        "変換モード選択",
        "モードを選んでください:\n"
        "1: InmFuckを実行する\n"
        "2: InmFuck → Brainfuck変換\n"
        "3: Brainfuck → InmFuck変換"
    )

    if mode not in ('1', '2', '3'):
        messagebox.showerror("エラー", "⚠ 無効な入力です。終了します。")
        exit()

    if mode in ('1', '2'):
        filetypes = [("InmFuckコード", "*.inm"), ("すべてのファイル", "*.*")]
        title = "InmFuckコードファイルを選択してください (.inm)"
    else:
        filetypes = [("Brainfuckコード", "*.bf *.b"), ("すべてのファイル", "*.*")]
        title = "Brainfuckコードファイルを選択してください (.bf, .b)"

    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    if not file_path:
        messagebox.showwarning("ファイル未選択", "⚠ ファイルが選択されませんでした。終了します。")
        exit()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read().strip()
    except Exception as e:
        messagebox.showerror("読み込みエラー", f"ファイルを開けませんでした:\n{e}")
        exit()

    if not code:
        messagebox.showwarning("警告", "⚠ ファイルが空です。終了します。")
        exit()

    try:
        if mode == '1':
            bf_code = inmu_to_brainfuck(code)
            output = brainfuck_interpreter(bf_code)
            messagebox.showinfo("実行結果", output if output else "(出力なし)")

        elif mode == '2':
            bf_code = inmu_to_brainfuck(code)
            build_bracket_map(bf_code)  # 構文チェック
            messagebox.showinfo("変換結果（Brainfuck）", bf_code or "(空)")
            save_path = filedialog.asksaveasfilename(
                defaultextension=".bf",
                filetypes=[("Brainfuckコード", "*.bf"), ("すべてのファイル", "*.*")],
                title="変換結果の保存先を選んでください"
            )
            if save_path:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(bf_code)
                messagebox.showinfo("保存完了", f"変換結果を保存しました:\n{save_path}")
            else:
                messagebox.showwarning("保存中止", "⚠ 保存先が選択されませんでした。")

        else:  # mode == '3'
            for c in code:
                if c not in BF_TO_INMU:
                    messagebox.showwarning("警告", f"⚠ 無効な命令: {c}")
            inmu_code = brainfuck_to_inmu(code)
            messagebox.showinfo("変換結果（InmFuck）", inmu_code or "(空)")
            save_path = filedialog.asksaveasfilename(
                defaultextension=".inm",
                filetypes=[("InmFuckコード", "*.inm"), ("すべてのファイル", "*.*")],
                title="変換結果の保存先を選んでください"
            )
            if save_path:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(inmu_code)
                messagebox.showinfo("保存完了", f"変換結果を保存しました:\n{save_path}")
            else:
                messagebox.showwarning("保存中止", "⚠ 保存先が選択されませんでした。")

    except SyntaxError as e:
        messagebox.showerror("構文エラー", str(e))
    except Exception as e:
        messagebox.showerror("実行時エラー", str(e))
