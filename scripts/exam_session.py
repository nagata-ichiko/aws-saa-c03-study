#!/usr/bin/env python3
"""
exam_session.py — 模擬試験セッション管理スクリプト

【使い方】
1. 問題を抽出してセッションを開始する:
   python exam_session.py start --mode mini --repo /path/to/repo
   → /tmp/exam_session.json を生成する

   過去出題済み問題のみで試験を行う場合:
   python exam_session.py start --mode mini --repo /path/to/repo --past
   → progress/exam-history/ の履歴から過去出題済みIDを抽出して出題する

2. 1問出題するたびに回答を記録する:
   python exam_session.py record --q_num 1 --answer A
   python exam_session.py record --q_num 2 --answer B,C  # 複数選択の場合

3. 全問終了後に採点・レポートを生成する:
   python exam_session.py grade --repo /path/to/repo

【セッションファイルの形式】
/tmp/exam_session.json に以下の形式で保存する:
{
  "mode": "mini",
  "date": "2026-03-25",
  "repo": "/path/to/repo",
  "past_mode": false,
  "questions": [
    {"num": 1, "id": 371, "answer": null},
    {"num": 2, "id": 1760, "answer": null},
    ...
  ]
}

回答記録後:
    {"num": 1, "id": 371, "answer": "B"}

【重要】
- セッションファイルが出題順と採点順のズレを防ぐ唯一の信頼できる情報源
- 出題時に必ず record コマンドで記録すること
- grade コマンドはセッションファイルの questions 順で採点するため順番ズレが起きない
"""

import json
import re
import argparse
import random
import sys
from datetime import date
from pathlib import Path

SESSION_FILE = "/tmp/exam_session.json"

EXAM_MODES = {
    "mini":  {"total": 11, "d1": 3, "d2": 3, "d3": 3, "d4": 2},
    "half":  {"total": 33, "d1": 10, "d2": 9, "d3": 8, "d4": 6},
    "full":  {"total": 65, "d1": 20, "d2": 17, "d3": 15, "d4": 13},
}

LABELS = ["A", "B", "C", "D", "E"]


def load_questions(repo: str):
    path = Path(repo) / "practice-tests" / "questions" / "all.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_past_ids(repo: str) -> set:
    """
    progress/exam-history/ 内の Markdown ファイルから
    過去に出題されたすべての問題 ID を抽出する。

    対応フォーマット:
    - 「| Q{id} |」形式（試験履歴の間違えた問題・正解した問題テーブル）
    - 「ID:{id}」形式（_questions.md ファイル）
    """
    history_dir = Path(repo) / "progress" / "exam-history"
    if not history_dir.exists():
        return set()

    past_ids = set()

    # テーブル行: | Q{id} | または | Q{id}_{日付} |
    pattern_table = re.compile(r"\|\s*Q(\d+)\s*\|")

    # ID: 形式: ID:371 または (ID:371,
    pattern_id = re.compile(r"ID:(\d+)")

    for md_file in history_dir.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            for m in pattern_table.finditer(content):
                past_ids.add(int(m.group(1)))
            for m in pattern_id.finditer(content):
                past_ids.add(int(m.group(1)))
        except Exception:
            pass

    return past_ids


def start_session(mode: str, repo: str, past: bool = False):
    """問題を抽出してセッションファイルを生成する"""
    if mode not in EXAM_MODES:
        print(f"ERROR: mode は {list(EXAM_MODES.keys())} のいずれかを指定してください")
        sys.exit(1)

    config = EXAM_MODES[mode]
    all_qs = load_questions(repo)

    # skip フラグが True の問題を除外
    all_qs = [q for q in all_qs if not q.get("skip", False)]

    if past:
        # 過去出題済み問題のみに絞り込む
        past_ids = extract_past_ids(repo)
        if not past_ids:
            print("WARNING: 過去の試験履歴が見つかりません。通常モードで実行します。")
            past = False
        else:
            all_qs = [q for q in all_qs if q["id"] in past_ids]
            if len(all_qs) == 0:
                print("ERROR: 過去出題済み問題が問題データに見つかりません。")
                sys.exit(1)
            print(f"📚 過去出題済みモード: {len(past_ids)} 問のIDを履歴から抽出、"
                  f"問題データと照合して {len(all_qs)} 問が利用可能")

    # ドメイン別に分類
    by_domain = {1: [], 2: [], 3: [], 4: []}
    for q in all_qs:
        d = q.get("domain")
        if d in by_domain:
            by_domain[d].append(q)

    # 各ドメインからランダムに抽出
    selected = []
    for d, count_key in [(1, "d1"), (2, "d2"), (3, "d3"), (4, "d4")]:
        count = config[count_key]
        pool = by_domain[d]
        if len(pool) < count:
            print(f"WARNING: Domain {d} の問題数が不足しています（{len(pool)} < {count}）")
            count = len(pool)
        if count > 0:
            selected.extend(random.sample(pool, count))

    if len(selected) == 0:
        print("ERROR: 出題できる問題がありません。")
        sys.exit(1)

    # シャッフル
    random.shuffle(selected)

    # セッションファイルを生成
    session = {
        "mode": mode,
        "date": str(date.today()),
        "repo": repo,
        "past_mode": past,
        "questions": [
            {"num": i + 1, "id": q["id"], "answer": None}
            for i, q in enumerate(selected)
        ],
        # 問題の全データも保存（採点時に再ロード不要）
        # キーは文字列に統一（JSONのキーは文字列になるため）
        "_question_data": {str(q["id"]): q for q in selected}
    }

    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(session, f, ensure_ascii=False, indent=2)

    mode_label = f"{mode}（過去出題済み問題）" if past else mode
    print(f"✅ セッション開始: {mode_label} モード ({len(selected)}問)")
    print(f"📄 セッションファイル: {SESSION_FILE}")
    print()
    print("\n出題する問題一覧（この順番で出題すること）:")
    for entry in session["questions"]:
        q = session["_question_data"][str(entry["id"])]
        print(f"  Q{entry['num']:2d} (ID:{entry['id']:4d}, Domain:{q['domain']}): {q.get('question_ja', q.get('question', ''))[:60]}...")

    return session


def record_answer(q_num: int, answer: str):
    """1問の回答をセッションファイルに記録する"""
    with open(SESSION_FILE, "r", encoding="utf-8") as f:
        session = json.load(f)

    found = False
    for entry in session["questions"]:
        if entry["num"] == q_num:
            entry["answer"] = answer.upper().replace(" ", "")
            found = True
            break

    if not found:
        print(f"ERROR: Q{q_num} はセッションに存在しません")
        sys.exit(1)

    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(session, f, ensure_ascii=False, indent=2)

    print(f"✅ Q{q_num} の回答を記録しました: {answer.upper()}")


def grade_session(repo: str = None):
    """セッションファイルを使って採点し、結果を出力する"""
    with open(SESSION_FILE, "r", encoding="utf-8") as f:
        session = json.load(f)

    q_data = session.get("_question_data", {})

    # repo が指定された場合は問題データを再ロード（_question_data がない古いセッション対応）
    if not q_data and repo:
        all_qs = load_questions(repo)
        q_data = {str(q["id"]): q for q in all_qs}

    results = []
    correct_count = 0

    for entry in session["questions"]:
        qid = entry["id"]
        user_answer_str = entry.get("answer")
        q = q_data.get(str(qid))

        if not q:
            print(f"WARNING: ID:{qid} の問題データが見つかりません")
            continue

        if user_answer_str is None:
            print(f"WARNING: Q{entry['num']} (ID:{qid}) の回答が記録されていません")
            continue

        # 回答を数値インデックスに変換（A→0, B→1, ...）
        user_indices = sorted([LABELS.index(c) for c in user_answer_str.split(",") if c in LABELS])
        correct_indices = sorted(q["correct"])
        is_correct = user_indices == correct_indices

        if is_correct:
            correct_count += 1

        correct_label = ",".join([LABELS[i] for i in correct_indices])
        results.append({
            "num": entry["num"],
            "id": qid,
            "domain": q["domain"],
            "user_answer": user_answer_str,
            "correct_answer": correct_label,
            "is_correct": is_correct,
            "question": q.get("question_ja", q.get("question", ""))[:80],
            "user_choice": q.get("choices_ja", q.get("choices", []))[user_indices[0]] if user_indices else "",
            "correct_choice": q.get("choices_ja", q.get("choices", []))[correct_indices[0]] if correct_indices else "",
            "explanation": q.get("explanation_ja", q.get("explanation", "")),
        })

    total = len(results)
    score_pct = correct_count / total * 100 if total > 0 else 0

    past_label = "（過去出題済み問題）" if session.get("past_mode") else ""
    print(f"\n{'='*60}")
    print(f"  採点結果{past_label}: {correct_count}/{total} ({score_pct:.1f}%)")
    print(f"  合格ライン: 72%  {'✅ 合格' if score_pct >= 72 else '❌ 未達'}")
    print(f"{'='*60}\n")

    # ドメイン別集計
    domain_results = {1: {"correct": 0, "total": 0}, 2: {"correct": 0, "total": 0},
                      3: {"correct": 0, "total": 0}, 4: {"correct": 0, "total": 0}}
    for r in results:
        d = r["domain"]
        domain_results[d]["total"] += 1
        if r["is_correct"]:
            domain_results[d]["correct"] += 1

    domain_names = {1: "D1: セキュリティ", 2: "D2: 弾力性", 3: "D3: 高性能", 4: "D4: コスト最適化"}
    for d, dr in domain_results.items():
        if dr["total"] > 0:
            pct = dr["correct"] / dr["total"] * 100
            print(f"  {domain_names[d]}: {dr['correct']}/{dr['total']} ({pct:.0f}%)")

    print()
    print("問題別結果:")
    for r in results:
        mark = "✅" if r["is_correct"] else "❌"
        print(f"  {mark} Q{r['num']:2d} (ID:{r['id']:4d}): あなた={r['user_answer']} / 正解={r['correct_answer']}")
        if not r["is_correct"]:
            print(f"       あなた: {r['user_choice'][:50]}")
            print(f"       正解:   {r['correct_choice'][:50]}")

    # 結果をセッションファイルに保存
    session["results"] = results
    session["score"] = {"correct": correct_count, "total": total, "pct": score_pct}
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(session, f, ensure_ascii=False, indent=2)

    print(f"\n📄 採点結果をセッションファイルに保存しました: {SESSION_FILE}")
    return results, correct_count, total, score_pct


def list_past_ids(repo: str):
    """過去出題済み問題IDの一覧を表示する（デバッグ用）"""
    past_ids = extract_past_ids(repo)
    all_qs = load_questions(repo)
    all_qs = [q for q in all_qs if not q.get("skip", False)]
    available = [q for q in all_qs if q["id"] in past_ids]

    print(f"📚 過去出題済み問題: {len(past_ids)} 問のIDを履歴から抽出")
    print(f"   問題データと照合: {len(available)} 問が利用可能")

    # ドメイン別集計
    by_domain = {1: 0, 2: 0, 3: 0, 4: 0}
    for q in available:
        d = q.get("domain")
        if d in by_domain:
            by_domain[d] += 1

    domain_names = {1: "D1: セキュリティ", 2: "D2: 弾力性", 3: "D3: 高性能", 4: "D4: コスト最適化"}
    for d, cnt in by_domain.items():
        print(f"   {domain_names[d]}: {cnt} 問")

    return past_ids, available


def main():
    parser = argparse.ArgumentParser(description="模擬試験セッション管理")
    subparsers = parser.add_subparsers(dest="command")

    # start コマンド
    start_parser = subparsers.add_parser("start", help="セッションを開始する")
    start_parser.add_argument("--mode", choices=["mini", "half", "full"], default="mini")
    start_parser.add_argument("--repo", required=True, help="リポジトリのパス")
    start_parser.add_argument("--past", action="store_true",
                              help="過去出題済み問題のみで試験を行う")

    # record コマンド
    record_parser = subparsers.add_parser("record", help="回答を記録する")
    record_parser.add_argument("--q_num", type=int, required=True, help="問題番号")
    record_parser.add_argument("--answer", required=True, help="回答 (例: A, B,C)")

    # grade コマンド
    grade_parser = subparsers.add_parser("grade", help="採点する")
    grade_parser.add_argument("--repo", help="リポジトリのパス（オプション）")

    # list-past コマンド（デバッグ用）
    list_parser = subparsers.add_parser("list-past", help="過去出題済み問題IDを一覧表示する")
    list_parser.add_argument("--repo", required=True, help="リポジトリのパス")

    args = parser.parse_args()

    if args.command == "start":
        start_session(args.mode, args.repo, past=getattr(args, "past", False))
    elif args.command == "record":
        record_answer(args.q_num, args.answer)
    elif args.command == "grade":
        grade_session(args.repo)
    elif args.command == "list-past":
        list_past_ids(args.repo)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
