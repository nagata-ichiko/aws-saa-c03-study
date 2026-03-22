#!/usr/bin/env python3
"""
AWS SAA-C03 模擬試験問題セット生成スクリプト

使い方:
  python3 scripts/generate_exam.py --mode full    # フル模擬試験（65問）
  python3 scripts/generate_exam.py --mode half    # ハーフ模擬試験（33問）
  python3 scripts/generate_exam.py --mode full --seed 42  # シード固定（再現性あり）

出力:
  exam_set_YYYYMMDD_HHMMSS.json  -- 出題セット（問題・選択肢・正解）
"""

import json
import random
import argparse
import os
from datetime import datetime

# 本番試験の配点比率
EXAM_MODES = {
    "full": {
        "name": "フル模擬試験",
        "total": 65,
        "distribution": {
            1: 20,  # Domain 1: 30% = 20問
            2: 17,  # Domain 2: 26% = 17問
            3: 15,  # Domain 3: 24% = 15問
            4: 13,  # Domain 4: 20% = 13問
        }
    },
    "half": {
        "name": "ハーフ模擬試験",
        "total": 33,
        "distribution": {
            1: 10,  # Domain 1: 30% ≈ 10問
            2: 9,   # Domain 2: 26% ≈ 9問
            3: 8,   # Domain 3: 24% ≈ 8問
            4: 6,   # Domain 4: 20% ≈ 6問
        }
    }
}

def load_questions(json_path: str) -> list:
    """問題データを読み込む"""
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)

def classify_by_domain(questions: list) -> dict:
    """問題を分野別に分類する"""
    domain_map = {1: [], 2: [], 3: [], 4: [], 0: []}
    for q in questions:
        # 日本語翻訳済み or 生成問題のみ対象
        if not (q.get("question_ja") and q.get("choices_ja")):
            continue
        # skip フラグがある問題は除外
        if q.get("skip"):
            continue
        domain = q.get("domain", 0)
        if domain in domain_map:
            domain_map[domain].append(q)
        else:
            domain_map[0].append(q)
    return domain_map

def sample_questions(domain_map: dict, distribution: dict, seed: int = None) -> list:
    """配点比率に従って問題をサンプリングする"""
    if seed is not None:
        random.seed(seed)

    sampled = []
    for domain, count in distribution.items():
        pool = domain_map.get(domain, []) + domain_map.get(0, [])
        if len(pool) < count:
            print(f"  ⚠️  Domain {domain}: 必要数 {count}問 に対して利用可能 {len(pool)}問")
            count = len(pool)
        selected = random.sample(pool, count)
        sampled.extend(selected)

    random.shuffle(sampled)
    return sampled

def build_exam_set(questions: list, mode_config: dict) -> dict:
    """試験セットのデータ構造を作成する"""
    exam_questions = []
    for i, q in enumerate(questions, 1):
        exam_questions.append({
            "number": i,
            "id": q.get("id"),
            "domain": q.get("domain", 0),
            "question": q.get("question_ja", q.get("question", "")),
            "choices": q.get("choices_ja", q.get("choices", [])),
            "correct": q.get("correct", []),
            "explanation": q.get("explanation_ja", q.get("explanation", "")),
            "tags": q.get("tags", []),
        })

    return {
        "mode": mode_config["name"],
        "total": mode_config["total"],
        "distribution": mode_config["distribution"],
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "questions": exam_questions
    }

def print_exam_preview(exam_set: dict):
    """試験セットのプレビューを表示する"""
    print(f"\n{'='*60}")
    print(f"  {exam_set['mode']} - {exam_set['total']}問")
    print(f"  生成日時: {exam_set['generated_at']}")
    print(f"{'='*60}")
    print(f"\n分野別問題数:")
    domain_counts = {}
    for q in exam_set["questions"]:
        d = q["domain"]
        domain_counts[d] = domain_counts.get(d, 0) + 1
    for d in sorted(domain_counts.keys()):
        label = f"Domain {d}" if d > 0 else "汎用"
        print(f"  {label}: {domain_counts[d]}問")
    print(f"\n最初の3問:")
    for q in exam_set["questions"][:3]:
        print(f"\n  Q{q['number']} [Domain {q['domain']}]")
        print(f"  {q['question'][:80]}...")
        for i, c in enumerate(q["choices"]):
            print(f"    {chr(65+i)}. {c[:60]}")

def main():
    parser = argparse.ArgumentParser(description="AWS SAA-C03 模擬試験問題セット生成")
    parser.add_argument("--mode", choices=["full", "half"], default="half",
                        help="試験モード: full=65問, half=33問 (デフォルト: half)")
    parser.add_argument("--seed", type=int, default=None,
                        help="乱数シード（再現性が必要な場合に指定）")
    parser.add_argument("--output", type=str, default=None,
                        help="出力ファイルパス（デフォルト: scripts/exam_sets/）")
    args = parser.parse_args()

    # パス設定
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    questions_path = os.path.join(repo_root, "practice-tests", "questions", "all.json")
    output_dir = os.path.join(script_dir, "exam_sets")
    os.makedirs(output_dir, exist_ok=True)

    # 問題読み込み
    print(f"問題データを読み込み中: {questions_path}")
    questions = load_questions(questions_path)
    print(f"  総問題数: {len(questions)}問")

    # 分野別分類
    domain_map = classify_by_domain(questions)
    for d, qs in domain_map.items():
        if d > 0:
            print(f"  Domain {d}: {len(qs)}問")

    # 問題抽出
    mode_config = EXAM_MODES[args.mode]
    print(f"\n{mode_config['name']}（{mode_config['total']}問）を生成中...")
    sampled = sample_questions(domain_map, mode_config["distribution"], seed=args.seed)

    # 試験セット作成
    exam_set = build_exam_set(sampled, mode_config)

    # 出力
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if args.output:
        output_path = args.output
    else:
        output_path = os.path.join(output_dir, f"exam_{args.mode}_{timestamp}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(exam_set, f, ensure_ascii=False, indent=2)

    print_exam_preview(exam_set)
    print(f"\n✅ 試験セットを保存しました: {output_path}")
    print(f"\n使い方:")
    print(f"  Claude Code / Manus に「このファイルを使って模擬試験を開始して」と伝えてください。")
    print(f"  ファイル: {output_path}")

if __name__ == "__main__":
    main()
