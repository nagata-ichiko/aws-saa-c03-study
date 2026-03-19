---
name: practice
description: AWS SAA-C03 の練習問題を出題する。引数で問題数を指定（例: /practice 5）。デフォルト10問。
user-invocable: true
---

# 練習問題出題スキル

ユーザーが指定した問題数の練習問題を出題します。

## 引数

- 問題数（数値）: 出題する問題数。省略時は10問。
  - 例: `/practice 5` → 5問出題
  - 例: `/practice 20` → 20問出題
  - 例: `/practice domain2 5` → Domain 2 から5問出題

## 実行フロー

### 1. 問題の一括取得（10問単位）

最初に問題データを一括取得してレスポンスを高速化します。
**10問単位でバッチ取得**し、必要に応じて追加バッチを取得します。

以下の Python スクリプトを Bash ツールで実行して問題を取得してください：

```python
python3 -c "
import json, random, sys

n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
batch_size = min(n, 10)
domain = sys.argv[2] if len(sys.argv) > 2 else None

# ファイル選択
if domain:
    files = {
        '1': 'domain1-secure-architecture.json',
        '2': 'domain2-resilient-architecture.json',
        '3': 'domain3-high-performance.json',
        '4': 'domain4-cost-optimized.json',
    }
    fname = files.get(domain, 'all.json')
else:
    fname = 'all.json'

with open(f'practice-tests/questions/{fname}') as f:
    data = json.load(f)

# 選択肢が2つ以上ある問題のみ（データ不備を除外）
valid = [q for q in data if len(q.get('choices_ja', q.get('choices', []))) >= 2]
selected = random.sample(valid, min(batch_size, len(valid)))

# 出力: 問題番号、問題文、選択肢、正解を一括表示
for i, q in enumerate(selected, 1):
    question = q.get('question_ja', q['question'])
    choices = q.get('choices_ja', q['choices'])
    correct = q['correct']
    multi = q.get('multi', False)
    print(f'=== Q{i} (ID:{q[\"id\"]}, Domain:{q[\"domain\"]}) ===')
    print(f'QUESTION: {question}')
    for j, c in enumerate(choices):
        print(f'  {chr(65+j)}. {c}')
    correct_letters = ','.join(chr(65+c) for c in correct)
    print(f'ANSWER: {correct_letters}')
    print(f'MULTI: {multi}')
    print()
" BATCH_SIZE DOMAIN
```

- `BATCH_SIZE` は取得する問題数（最大10）
- `DOMAIN` はドメイン番号（省略時は全問題から）
- 10問を超える場合は、最初の10問を出し終わった後に次の10問を取得する

### 2. 出題ルール

- 取得した問題データはすべてコンテキストに保持する
- **1問ずつ**出題する（まとめて出さない）
- 問題文と選択肢を日本語で提示する（`question_ja`, `choices_ja` を優先。なければ英語から翻訳）
- 複数選択問題（MULTI: True）の場合は「※ 複数選択問題です（N つ選んでください）」と表示する
- 固有名詞（AWS サービス名・略語）は英語のまま残す

### 3. 回答判定

- コンテキストに保持した正解データと照合する → **ツール呼び出し不要で即レスポンス**
- 正解・不正解を判定し、解説を提供する：
  - なぜその選択肢が正解なのか
  - なぜ他の選択肢が間違っているのか
  - 関連する AWS サービスのベストプラクティス

### 4. 間違い記録

- 間違えた問題は `practice-tests/wrong-answers/Q{問題ID}_{日付}.md` に記録する
- **ファイル作成はバッチでまとめず、間違えた直後に作成する**（ただしコミット・プッシュは全問終了後にまとめて行う）

### 5. 結果報告と記録（全問終了後）

全問終了後に以下を行う：

1. **成績表を表示**: 正答率、各問題の正誤一覧
2. **弱点分析**: 間違えた問題の傾向を分析
3. **git コミット＆プッシュ**: 間違い記録ファイルをまとめて1回でコミット・プッシュする

```bash
git add practice-tests/wrong-answers/*.md && git commit -m "練習問題の間違い記録を追加" && git push -u origin <current-branch>
```

### 6. 次バッチの取得（10問超の場合）

問題数が10問を超える場合：
- 最初の10問が終わったら、次の10問を同じ方法で取得する
- 取得済みの問題IDを除外して重複を防ぐ
- 全問完了するまで繰り返す
