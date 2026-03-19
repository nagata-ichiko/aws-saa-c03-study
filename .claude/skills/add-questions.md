---
name: add-questions
description: AWS SAA-C03 の練習問題を新規作成して追加する。引数でドメインや問題数を指定（例: /add-questions domain1 10）
user-invocable: true
---

# 問題追加スキル

AWS SAA-C03 試験の練習問題を AI が生成し、問題データに追加します。

## 引数

- `domainN`（N=1〜4）: 対象ドメイン（省略時はバランスよく全ドメインから）
- 問題数（数値）: 生成する問題数。デフォルト5問。
- トピック（文字列）: 特定のトピックに絞る（例: `VPC`, `S3`, `Lambda`）

例:
- `/add-questions domain1 10` → Domain 1 の問題を10問生成
- `/add-questions S3 5` → S3 関連の問題を5問生成
- `/add-questions` → 全ドメインから5問生成

## ドメイン定義

- **Domain 1**: セキュアなアーキテクチャの設計（IAM, KMS, VPC セキュリティ, etc.）
- **Domain 2**: 弾力性に優れたアーキテクチャの設計（マルチ AZ, Auto Scaling, バックアップ, etc.）
- **Domain 3**: 高パフォーマンスなアーキテクチャの設計（ElastiCache, CloudFront, EBS 最適化, etc.）
- **Domain 4**: コスト最適化アーキテクチャの設計（RI, Spot, S3 ストレージクラス, etc.）

## 実行フロー

### 1. 既存問題の確認

まず既存の問題データを読み込み、次の ID を決定する：

```python
python3 -c "
import json
with open('practice-tests/questions/all.json') as f:
    data = json.load(f)
max_id = max(q['id'] for q in data)
print(f'Current max ID: {max_id}')
print(f'Next ID starts at: {max_id + 1}')
print(f'Total questions: {len(data)}')
"
```

### 2. 問題の生成

以下の要件に従って問題を生成する：

#### 問題の品質基準
- **SAA-C03 試験の出題範囲**に準拠すること
- **シナリオベース**の問題を優先する（単純な知識問題よりも実践的な問題）
- 選択肢は **4つ**（単一選択）または **5つ以上**（複数選択）
- **正解は1つまたは明示的に複数**とする
- 不正解の選択肢も**もっともらしい**ものにする（明らかに間違いとわかるものは避ける）
- **解説を必ず含める**（正解の理由、不正解の理由、関連するベストプラクティス）

#### データ形式

```json
{
  "id": 次のID,
  "question": "英語の問題文",
  "choices": ["選択肢A（英語）", "選択肢B", "選択肢C", "選択肢D"],
  "correct": [正解のインデックス（0始まり）],
  "multi": false,
  "domain": ドメイン番号（1-4, 0は未分類）,
  "tags": ["関連タグ"],
  "explanation": "解説（英語）",
  "domain_seq": ドメイン内の連番,
  "question_ja": "日本語の問題文",
  "choices_ja": ["選択肢A（日本語）", "選択肢B", "選択肢C", "選択肢D"]
}
```

### 3. 生成した問題をユーザーに提示

生成した問題を一覧で表示し、ユーザーに確認を求める：

```
## 生成した問題

### Q{ID}: {問題の概要}
- ドメイン: {domain}
- タイプ: 単一選択 / 複数選択
- 問題文: {question_ja の冒頭50文字}...
- 正解: {correct_letters}

（全問題を表示）

これらの問題を追加してよろしいですか？修正が必要な問題があれば指摘してください。
```

### 4. 問題データへの追加

ユーザーの承認後、以下を実行：

1. `all.json` に追加
2. 該当ドメインの JSON ファイルにも追加（domain が 1-4 の場合）
3. `general.json` に追加（domain が 0 の場合）

```python
python3 -c "
import json

# all.json に追加
with open('practice-tests/questions/all.json') as f:
    data = json.load(f)
new_questions = [...]  # 生成した問題リスト
data.extend(new_questions)
with open('practice-tests/questions/all.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# ドメイン別ファイルにも追加
domain_files = {
    1: 'domain1-secure-architecture.json',
    2: 'domain2-resilient-architecture.json',
    3: 'domain3-high-performance.json',
    4: 'domain4-cost-optimized.json',
    0: 'general.json',
}
for q in new_questions:
    fname = domain_files.get(q['domain'], 'general.json')
    with open(f'practice-tests/questions/{fname}') as f:
        domain_data = json.load(f)
    domain_data.append(q)
    with open(f'practice-tests/questions/{fname}', 'w') as f:
        json.dump(domain_data, f, ensure_ascii=False, indent=2)
"
```

### 5. コミット＆プッシュ

```bash
git add practice-tests/questions/*.json
git commit -m "SAA-C03 練習問題を N 問追加（Domain X）"
git push -u origin <current-branch>
```
