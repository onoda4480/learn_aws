#!/usr/bin/env python3
"""間違えた問題を「間違えたやつ一覧.md」に追記するスクリプト"""

from __future__ import annotations

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_FILE = os.path.join(SCRIPT_DIR, "間違えたやつ一覧.md")


def read_multiline(prompt: str) -> list[str] | None:
    """複数行の入力を受け取る。空行で入力終了。exitで終了。"""
    print(prompt)
    print("（入力が終わったら空行でEnter / 終了するには exit）")
    lines = []
    while True:
        line = input()
        if line.strip().lower() == "exit":
            return None
        if line == "":
            break
        lines.append(line)
    return lines


def split_question_and_choices(lines: list[str]) -> tuple[str, list[str]]:
    """問題文と選択肢を分離する。

    Ping-tの形式: 問題文の後に選択肢が1行ずつ並ぶ。
    問題文の最終行は「〜か。」「〜選択）」などで終わる。
    """
    question_end = -1
    for i, line in enumerate(lines):
        stripped = line.rstrip()
        if stripped.endswith(("か。", "か？", "選択）", "選択)", "ください。")):
            question_end = i
            # 最後に見つかったものを使う（問題文中にも「〜か。」がある場合があるため）

    if question_end == -1 or question_end >= len(lines) - 1:
        # 自動検出できない場合は手動で聞く
        print("\n--- 貼り付けたテキスト ---")
        for i, line in enumerate(lines):
            print(f"  {i + 1}: {line}")
        print("---")
        try:
            n = int(input("選択肢が始まる行番号を入力してください: ").strip())
            question_end = n - 2  # 0-indexed, 1つ前が問題の最終行
        except (ValueError, IndexError):
            print("無効な入力です。終了します。")
            sys.exit(1)

    question_lines = lines[: question_end + 1]
    choice_lines = [line.strip() for line in lines[question_end + 1 :] if line.strip()]

    return "\n".join(question_lines), choice_lines


def append_entry(entry: str):
    """間違えたやつ一覧.mdにエントリを追記する。"""
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    template = "### 問題\n### 正解\n### 回答"
    if content.rstrip().endswith(template):
        content = content.rstrip()
        content = content[: content.rfind(template)]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content.rstrip("\n") + "\n" + entry)


def add_one() -> bool:
    """1問分の処理。続行ならTrue、終了ならFalseを返す。"""
    lines = read_multiline("問題文と選択肢をまとめて貼り付けてください:")
    if lines is None:
        return False
    if not lines:
        print("入力が空です。スキップします。")
        return True

    question, choices = split_question_and_choices(lines)

    # 選択肢に番号を振って表示
    print("\n--- 検出結果 ---")
    print(f"問題文: {question[:60]}...")
    print("選択肢:")
    numbered_choices = []
    for i, choice in enumerate(choices, 1):
        numbered = f"{i}.{choice}"
        numbered_choices.append(numbered)
        print(f"  {numbered}")
    print("---\n")

    correct = input("正解の番号（例: 3 または 1,3,5）: ").strip()
    if correct.lower() == "exit":
        return False
    answer = input("自分の回答（例: 4 または 2,4,6）: ").strip()
    if answer.lower() == "exit":
        return False

    if not correct or not answer:
        print("正解または回答が空です。スキップします。")
        return True

    choices_text = "\n".join(numbered_choices)
    entry = f"\n### 問題\n{question}\n{choices_text}\n\n### 正解\n{correct}\n### 自分の回答\n{answer}\n"

    append_entry(entry)
    print("\n追記しました！\n")
    return True


def main():
    print("=" * 50)
    print("  間違えた問題を追記するツール")
    print("  （Ctrl+C または exit で終了）")
    print("=" * 50)

    count = 0
    try:
        while True:
            print(f"\n--- {count + 1}問目 ---")
            if not add_one():
                break
            count += 1
    except KeyboardInterrupt:
        print()

    print(f"\n{count}問 追記しました。おつかれさまでした！")


if __name__ == "__main__":
    main()
