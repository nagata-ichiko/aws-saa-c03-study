#!/usr/bin/env python3.11
"""
問題DBの日本語訳自動補完スクリプト
- 問題DBの question_ja / choices_ja / explanation_ja が空の問題を検出
- OpenAI API (gpt-4.1-mini) で日本語訳して DB に書き戻す
- 不正解問題ファイルに含まれる問題IDのみを対象にするオプションあり

usage:
  # 不正解問題のみ翻訳
  python3.11 auto_translate.py --repo /path/to/repo --wrong-only

  # DB全体を翻訳（時間がかかる）
  python3.11 auto_translate.py --repo /path/to/repo
"""
import argparse
import glob
import json
import os
import re
import time

from openai import OpenAI

client = OpenAI()
BATCH_SIZE = 8


def load_questions_db(repo):
    """問題DBを読み込んでIDでインデックス化する"""
    q_db = {}
    db_paths = {}
    for path in glob.glob(os.path.join(repo, "practice-tests/questions/*.json")):
        if "index" in path:
            continue
        with open(path) as f:
            data = json.load(f)
        if isinstance(data, list):
            for q in data:
                qid = str(q["id"])
                q_db[qid] = q
                db_paths[qid] = path
    return q_db, db_paths


def load_wrong_question_ids(repo):
    """不正解問題ファイルからIDリストを取得する"""
    wrong_dir = os.path.join(repo, "practice-tests/wrong-answers")
    ids = set()
    for path in glob.glob(os.path.join(wrong_dir, "Q*.md")) + \
                glob.glob(os.path.join(wrong_dir, "mini_Q*.md")):
        if "template" in path:
            continue
        m = re.search(r"Q(\d+)", os.path.basename(path))
        if m:
            ids.add(m.group(1))
    return ids


def translate_batch(questions):
    """バッチ翻訳（最大BATCH_SIZE問）"""
    input_data = [
        {
            "id": str(q["id"]),
            "question": q.get("question", ""),
            "choices": q.get("choices", []),
            "explanation": q.get("explanation", ""),
        }
        for q in questions
    ]

    prompt = f"""以下のAWS SAA-C03試験問題（英語）を日本語に翻訳してください。

入力JSON:
{json.dumps(input_data, ensure_ascii=False, indent=2)}

翻訳ルール:
- AWS サービス名（Amazon S3, EC2, RDS, CloudFront, VPC, EBS, IAM, AMI, Auto Scaling, Multi-AZ, Lambda, DynamoDB, SQS, SNS, CloudWatch, CloudTrail, Route 53, Elastic Beanstalk, CloudFormation, Glacier など）は英語のまま残す
- 技術用語（IOPS, RAID, BGP, ASN, SSL/TLS, HTTPS, SSH, VPN, NAT, CIDR, DNS など）は英語のまま残す
- 自然な日本語にする（直訳ではなく意訳でOK）
- 選択肢の内容は正確に翻訳する
- id は元の値をそのまま使う（変更しない）

出力は以下のJSON形式のみ返してください（コードブロック不要、純粋なJSONのみ）:
[
  {{
    "id": "元のID（変更しない）",
    "question_ja": "翻訳した問題文",
    "choices_ja": ["選択肢A翻訳", "選択肢B翻訳", ...],
    "explanation_ja": "翻訳した解説（空なら空文字）"
  }},
  ...
]"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


def apply_translations(translations, q_db, db_paths):
    """翻訳結果をDBファイルに書き込む"""
    updated_files = set()
    for qid, t in translations.items():
        db_q = q_db.get(qid)
        path = db_paths.get(qid)
        if not db_q or not path:
            continue
        changed = False
        if not db_q.get("question_ja") and t.get("question_ja"):
            db_q["question_ja"] = t["question_ja"]
            changed = True
        if not db_q.get("choices_ja") and t.get("choices_ja"):
            db_q["choices_ja"] = t["choices_ja"]
            changed = True
        if not db_q.get("explanation_ja") and t.get("explanation_ja"):
            db_q["explanation_ja"] = t["explanation_ja"]
            changed = True
        if changed:
            updated_files.add(path)

    for path in updated_files:
        with open(path) as f:
            data = json.load(f)
        for q in data:
            qid = str(q["id"])
            if qid in translations:
                t = translations[qid]
                if not q.get("question_ja") and t.get("question_ja"):
                    q["question_ja"] = t["question_ja"]
                if not q.get("choices_ja") and t.get("choices_ja"):
                    q["choices_ja"] = t["choices_ja"]
                if not q.get("explanation_ja") and t.get("explanation_ja"):
                    q["explanation_ja"] = t["explanation_ja"]
        with open(path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  更新: {os.path.basename(path)}")

    return len(updated_files)


def main():
    parser = argparse.ArgumentParser(description="問題DBの日本語訳自動補完")
    parser.add_argument("--repo", default=".", help="リポジトリのパス")
    parser.add_argument(
        "--wrong-only", action="store_true",
        help="不正解問題ファイルに含まれるIDのみを対象にする（デフォルト: True）"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="DB全体を対象にする（時間がかかる）"
    )
    args = parser.parse_args()

    repo = os.path.abspath(args.repo)
    print(f"リポジトリ: {repo}")

    q_db, db_paths = load_questions_db(repo)
    print(f"問題DB: {len(q_db)}問読み込み")

    # 対象IDを決定
    if args.all:
        target_ids = set(q_db.keys())
    else:
        # デフォルト: 不正解問題のみ
        target_ids = load_wrong_question_ids(repo)
        print(f"不正解問題ID: {len(target_ids)}件")

    # 日本語訳がない問題を抽出
    no_ja = [
        q_db[qid] for qid in sorted(target_ids, key=lambda x: int(x) if x.isdigit() else 0)
        if qid in q_db and not q_db[qid].get("question_ja")
    ]
    print(f"翻訳対象: {len(no_ja)}問")

    if not no_ja:
        print("✅ すべての問題に日本語訳があります。翻訳不要です。")
        return

    # バッチ翻訳
    all_translations = {}
    total_batches = (len(no_ja) + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(0, len(no_ja), BATCH_SIZE):
        batch = no_ja[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        batch_ids = [str(q["id"]) for q in batch]
        print(f"バッチ {batch_num}/{total_batches}: IDs={batch_ids}")
        try:
            results = translate_batch(batch)
            for r in results:
                all_translations[str(r["id"])] = r
            print(f"  → {len(results)}件翻訳完了")
        except Exception as e:
            print(f"  → エラー: {e}")
        if i + BATCH_SIZE < len(no_ja):
            time.sleep(0.3)

    print(f"\n翻訳完了: {len(all_translations)}件")

    # DBに書き込む
    print("DBに書き込み中...")
    updated = apply_translations(all_translations, q_db, db_paths)
    print(f"✅ {updated}ファイルを更新しました")

    # 最終確認
    still_no_ja = [
        qid for qid in target_ids
        if qid in q_db and not q_db[qid].get("question_ja")
    ]
    if still_no_ja:
        print(f"\n⚠️  まだ日本語訳なし: {len(still_no_ja)}件")
        for qid in still_no_ja:
            print(f"  ID={qid}")
    else:
        print("\n✅ 全問題の日本語訳が完了しました")


if __name__ == "__main__":
    main()
