---
name: validate-questions
description: 問題データの品質を検証し、不備のある問題を修正・除外する。引数でドメインやID範囲を指定可能（例: /validate-questions domain2, /validate-questions 100-200）
user-invocable: true
---

# 問題データ検証スキル

`practice-tests/questions/` 内の問題データの品質を検証し、不備を報告・修正します。

## 引数

- `domain1`〜`domain4`: 特定ドメインのみ検証
- `ID-ID`（例: `100-200`）: 特定ID範囲のみ検証
- `fix`: 自動修正モード（検証 + 修正を実行）
- 引数なし: 全問題のサマリーレポートを出力

## 検証項目

以下の観点で問題データを検証します：

### 1. 構造的な不備（自動検出）

Bash ツールで以下の Python スクリプトを実行して一括検出：

```python
python3 -c "
import json, sys

target = sys.argv[1] if len(sys.argv) > 1 else 'all'

# ファイル選択
files = {
    'domain1': 'domain1-secure-architecture.json',
    'domain2': 'domain2-resilient-architecture.json',
    'domain3': 'domain3-high-performance.json',
    'domain4': 'domain4-cost-optimized.json',
    'all': 'all.json',
}
fname = files.get(target, 'all.json')

with open(f'practice-tests/questions/{fname}') as f:
    data = json.load(f)

# ID範囲フィルタ
if '-' in target and target[0].isdigit():
    lo, hi = map(int, target.split('-'))
    data = [q for q in data if lo <= q['id'] <= hi]

issues = {
    'single_choice': [],      # 選択肢が1つ以下
    'no_japanese': [],         # 日本語訳なし
    'no_explanation': [],      # 解説なし
    'bad_correct_index': [],   # 正解インデックスが範囲外
    'duplicate_choices': [],   # 選択肢に重複あり
    'empty_question': [],      # 問題文が空
    'correct_mismatch': [],    # 複数選択フラグと正解数の不整合
}

for q in data:
    qid = q['id']
    choices = q.get('choices', [])
    choices_ja = q.get('choices_ja', [])
    correct = q.get('correct', [])

    if len(choices) < 2:
        issues['single_choice'].append(qid)
    if not q.get('question_ja'):
        issues['no_japanese'].append(qid)
    if not q.get('explanation'):
        issues['no_explanation'].append(qid)
    if any(c >= len(choices) or c < 0 for c in correct):
        issues['bad_correct_index'].append(qid)
    if len(set(choices)) != len(choices):
        issues['duplicate_choices'].append(qid)
    if not q.get('question', '').strip():
        issues['empty_question'].append(qid)
    if q.get('multi', False) and len(correct) <= 1:
        issues['correct_mismatch'].append(qid)
    if not q.get('multi', False) and len(correct) > 1:
        issues['correct_mismatch'].append(qid)

print(f'Total questions: {len(data)}')
print()
for category, ids in issues.items():
    print(f'{category}: {len(ids)} issues')
    if ids and len(ids) <= 20:
        print(f'  IDs: {ids}')
    elif ids:
        print(f'  First 20 IDs: {ids[:20]}')
" TARGET
```

### 2. 内容の正確性検証（AI による確認）

構造的に問題ない質問について、以下を AI で検証する：

- **正解の妥当性**: AWS 公式ドキュメントの知識に基づき、設定されている正解が本当に正しいか確認
- **選択肢の妥当性**: 選択肢が適切か、明らかに間違った記述がないか
- **問題文の明確さ**: 問題文が曖昧でなく、回答可能か

**検証は10問単位で行い、問題がある場合はユーザーに報告して修正の承認を得る。**

### 3. レポート出力

検証結果を以下の形式で報告：

```
## 検証レポート

### サマリー
- 検証対象: N 問
- 構造的不備: N 問
- 内容の疑義: N 問
- 正常: N 問

### 構造的不備の内訳
- 選択肢不足: N 問（ID: ...）
- 日本語訳なし: N 問
- ...

### 内容の疑義
- Q{ID}: {問題の概要} → {疑義の内容}
```

### 4. 自動修正（`fix` モード）

`/validate-questions fix` で実行した場合、以下を自動修正する：

- **選択肢1つ以下の問題**: 問題データから除外（別ファイルに退避）
- **日本語訳なし**: AI で翻訳を生成して `question_ja`, `choices_ja` を追加
- **正解インデックス範囲外**: 問題データから除外

修正後は JSON ファイルを上書き保存し、git コミット＆プッシュする。

**重要: 正解の変更など内容に関わる修正は自動では行わず、ユーザーに確認を取ること。**
