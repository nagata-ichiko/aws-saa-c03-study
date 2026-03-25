#!/usr/bin/env python3.11
"""
不正解問題レビューHTML生成スクリプト
usage: python3.11 generate_review_html.py --repo /path/to/repo --output /path/to/output.html
"""
import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime

LABELS = ["A", "B", "C", "D", "E", "F"]
DOMAIN_NAMES = {1: "D1: セキュリティ", 2: "D2: 弾力性", 3: "D3: 高性能", 4: "D4: コスト最適化"}


def load_questions_db(repo):
    """問題データベースを読み込む"""
    q_db = {}
    for path in glob.glob(os.path.join(repo, "practice-tests/questions/*.json")):
        if "index" in path:
            continue
        with open(path) as f:
            data = json.load(f)
        if isinstance(data, list):
            for q in data:
                q_db[str(q["id"])] = q
    return q_db


def load_wrong_questions(repo):
    """不正解問題ファイルを読み込む（IDごとに最新ファイルを使用）"""
    wrong_dir = os.path.join(repo, "practice-tests/wrong-answers")
    files_by_id = {}
    for path in sorted(
        glob.glob(os.path.join(wrong_dir, "Q*.md"))
        + glob.glob(os.path.join(wrong_dir, "mini_Q*.md"))
    ):
        if "template" in path:
            continue
        m = re.search(r"Q(\d+)", os.path.basename(path))
        if not m:
            continue
        qid = m.group(1)
        files_by_id[qid] = path

    sorted_ids = sorted(files_by_id.keys(), key=lambda x: int(x))
    result = []
    for qid in sorted_ids:
        path = files_by_id[qid]
        with open(path) as f:
            content = f.read()

        # ドメインを抽出
        domain_m = re.search(r"\*\*ドメイン:\*\* D(\d)", content)
        domain = int(domain_m.group(1)) if domain_m else 0

        # 問題文を抽出
        q_m = re.search(r"## 問題\n\n(.*?)\n## 選択肢", content, re.DOTALL)
        question = q_m.group(1).strip() if q_m else ""

        # 選択肢を抽出
        choices_m = re.search(r"## 選択肢\n\n(.*?)\n## あなたの回答", content, re.DOTALL)
        choices_raw = choices_m.group(1).strip() if choices_m else ""
        choices = re.findall(r"- \*\*[A-F]\.\*\* (.+)", choices_raw)

        # 正解を抽出
        correct_m = re.search(r"## 正解: (.+)", content)
        correct = correct_m.group(1).strip() if correct_m else ""

        # 解説を抽出
        expl_m = re.search(r"## 解説\n\n?(.*?)$", content, re.DOTALL)
        explanation = expl_m.group(1).strip() if expl_m else ""

        # 自分の回答を抽出
        user_ans_m = re.search(r"## あなたの回答: (.+)", content)
        user_answer = user_ans_m.group(1).strip() if user_ans_m else ""

        # ファイルから取れない場合はDBから補完
        result.append(
            {
                "id": qid,
                "domain": domain,
                "question": question,
                "choices": choices,
                "correct": correct,
                "explanation": explanation,
                "user_answer": user_answer,
                "path": path,
            }
        )

    return result


def enrich_from_db(questions, q_db):
    """問題DBから日本語データで補完する"""
    for q in questions:
        db_q = q_db.get(q["id"])
        if not db_q:
            continue
        # 問題文・選択肢・解説がファイルにない場合はDBから補完
        if not q["question"] and db_q.get("question_ja"):
            q["question"] = db_q["question_ja"]
        if not q["choices"] and db_q.get("choices_ja"):
            q["choices"] = db_q["choices_ja"]
        if not q["explanation"] and db_q.get("explanation_ja"):
            q["explanation"] = db_q["explanation_ja"]
        if not q["explanation"] and db_q.get("explanation"):
            q["explanation"] = db_q["explanation"]
        if not q["domain"] and db_q.get("domain"):
            q["domain"] = db_q["domain"]
        # 正解ラベルがない場合はDBから生成
        if not q["correct"] and db_q.get("correct"):
            q["correct"] = ",".join(
                [LABELS[i] for i in db_q["correct"] if i < len(LABELS)]
            )
    return questions


def escape_html(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("\n", "<br>")
    )


def generate_html(questions, output_path):
    """ページング形式のHTMLを生成する"""
    total = len(questions)
    questions_json = json.dumps(questions, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AWS SAA-C03 不正解問題レビュー ({total}問)</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; }}

  .header {{
    background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
    padding: 20px 24px;
    border-bottom: 1px solid #334155;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
  }}
  .header h1 {{ font-size: 1.1rem; font-weight: 700; color: #f8fafc; }}
  .header .subtitle {{ font-size: 0.8rem; color: #94a3b8; margin-top: 2px; }}

  .progress-bar-wrap {{ flex: 1; margin: 0 24px; }}
  .progress-bar {{ background: #1e293b; border-radius: 999px; height: 8px; overflow: hidden; }}
  .progress-fill {{ background: linear-gradient(90deg, #3b82f6, #8b5cf6); height: 100%; border-radius: 999px; transition: width 0.3s ease; }}
  .progress-label {{ font-size: 0.75rem; color: #64748b; text-align: right; margin-top: 4px; }}

  .main {{ max-width: 860px; margin: 0 auto; padding: 32px 16px 80px; }}

  .card {{
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
  }}

  .card-meta {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 18px;
  }}
  .badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.03em;
  }}
  .badge-d1 {{ background: #1e3a5f; color: #93c5fd; border: 1px solid #3b82f6; }}
  .badge-d2 {{ background: #1a3a2a; color: #6ee7b7; border: 1px solid #10b981; }}
  .badge-d3 {{ background: #3a2a1a; color: #fcd34d; border: 1px solid #f59e0b; }}
  .badge-d4 {{ background: #2a1a3a; color: #c4b5fd; border: 1px solid #8b5cf6; }}
  .badge-id {{ background: #1e293b; color: #64748b; border: 1px solid #334155; }}
  .q-num {{ font-size: 0.85rem; color: #64748b; margin-left: auto; }}

  .question-text {{
    font-size: 1rem;
    line-height: 1.75;
    color: #e2e8f0;
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid #334155;
  }}

  .choices {{ list-style: none; display: flex; flex-direction: column; gap: 10px; margin-bottom: 24px; }}
  .choice-item {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 10px;
    border: 1px solid #334155;
    background: #0f172a;
    transition: border-color 0.2s;
  }}
  .choice-item.correct {{
    border-color: #10b981;
    background: #052e16;
  }}
  .choice-item.user-wrong {{
    border-color: #ef4444;
    background: #2d0a0a;
  }}
  .choice-label {{
    font-weight: 700;
    font-size: 0.9rem;
    min-width: 24px;
    color: #94a3b8;
  }}
  .choice-item.correct .choice-label {{ color: #10b981; }}
  .choice-item.user-wrong .choice-label {{ color: #ef4444; }}
  .choice-text {{ font-size: 0.9rem; line-height: 1.6; color: #cbd5e1; }}
  .choice-mark {{ margin-left: auto; font-size: 1rem; }}

  .answer-row {{
    display: flex;
    gap: 16px;
    margin-bottom: 20px;
    font-size: 0.85rem;
  }}
  .answer-box {{
    padding: 6px 14px;
    border-radius: 8px;
    font-weight: 600;
  }}
  .answer-box.user {{ background: #2d0a0a; color: #fca5a5; border: 1px solid #ef4444; }}
  .answer-box.correct {{ background: #052e16; color: #6ee7b7; border: 1px solid #10b981; }}

  .explanation {{
    background: #0f172a;
    border: 1px solid #334155;
    border-left: 3px solid #3b82f6;
    border-radius: 8px;
    padding: 16px 20px;
    font-size: 0.88rem;
    line-height: 1.75;
    color: #94a3b8;
  }}
  .explanation-title {{
    font-size: 0.78rem;
    font-weight: 700;
    color: #3b82f6;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
  }}
  .no-explanation {{ color: #475569; font-style: italic; }}

  .nav {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #0f172a;
    border-top: 1px solid #334155;
    padding: 14px 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    z-index: 100;
  }}
  .btn {{
    padding: 10px 24px;
    border-radius: 10px;
    border: none;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
  }}
  .btn-primary {{ background: #3b82f6; color: #fff; }}
  .btn-primary:hover {{ background: #2563eb; }}
  .btn-secondary {{ background: #1e293b; color: #94a3b8; border: 1px solid #334155; }}
  .btn-secondary:hover {{ background: #334155; color: #e2e8f0; }}
  .btn:disabled {{ opacity: 0.35; cursor: not-allowed; }}
  .nav-counter {{ font-size: 0.85rem; color: #64748b; min-width: 80px; text-align: center; }}

  .filter-bar {{
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
    flex-wrap: wrap;
  }}
  .filter-btn {{
    padding: 5px 14px;
    border-radius: 999px;
    border: 1px solid #334155;
    background: #1e293b;
    color: #94a3b8;
    font-size: 0.78rem;
    cursor: pointer;
    transition: all 0.15s;
  }}
  .filter-btn.active {{ background: #3b82f6; color: #fff; border-color: #3b82f6; }}
  .filter-btn:hover:not(.active) {{ background: #334155; }}

  .done-screen {{
    text-align: center;
    padding: 60px 20px;
  }}
  .done-screen h2 {{ font-size: 1.8rem; color: #f8fafc; margin-bottom: 12px; }}
  .done-screen p {{ color: #64748b; font-size: 1rem; }}
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="header h1">AWS SAA-C03 不正解問題レビュー</div>
    <div class="subtitle" id="subtitle">全 {total} 問</div>
  </div>
  <div class="progress-bar-wrap">
    <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
    <div class="progress-label" id="progressLabel">0 / {total}</div>
  </div>
</div>

<div class="main">
  <div class="filter-bar" id="filterBar">
    <button class="filter-btn active" onclick="setFilter(0)">すべて</button>
    <button class="filter-btn" onclick="setFilter(1)">D1: セキュリティ</button>
    <button class="filter-btn" onclick="setFilter(2)">D2: 弾力性</button>
    <button class="filter-btn" onclick="setFilter(3)">D3: 高性能</button>
    <button class="filter-btn" onclick="setFilter(4)">D4: コスト最適化</button>
  </div>
  <div id="cardContainer"></div>
</div>

<div class="nav">
  <button class="btn btn-secondary" id="btnPrev" onclick="navigate(-1)" disabled>← 前へ</button>
  <span class="nav-counter" id="navCounter">1 / {total}</span>
  <button class="btn btn-primary" id="btnNext" onclick="navigate(1)">次へ →</button>
</div>

<script>
const ALL_QUESTIONS = {questions_json};
let filtered = [...ALL_QUESTIONS];
let current = 0;
let activeFilter = 0;

const DOMAIN_BADGE = {{
  1: 'badge-d1', 2: 'badge-d2', 3: 'badge-d3', 4: 'badge-d4'
}};
const DOMAIN_LABEL = {{
  1: 'D1: セキュリティ', 2: 'D2: 弾力性', 3: 'D3: 高性能', 4: 'D4: コスト最適化', 0: '不明'
}};

function setFilter(domain) {{
  activeFilter = domain;
  document.querySelectorAll('.filter-btn').forEach((b, i) => {{
    b.classList.toggle('active', i === domain);
  }});
  filtered = domain === 0 ? [...ALL_QUESTIONS] : ALL_QUESTIONS.filter(q => q.domain === domain);
  current = 0;
  render();
}}

function navigate(dir) {{
  current = Math.max(0, Math.min(filtered.length - 1, current + dir));
  render();
  window.scrollTo({{top: 0, behavior: 'smooth'}});
}}

function render() {{
  const total = filtered.length;
  const q = filtered[current];

  // progress
  const pct = total > 0 ? Math.round((current + 1) / total * 100) : 0;
  document.getElementById('progressFill').style.width = pct + '%';
  document.getElementById('progressLabel').textContent = (current + 1) + ' / ' + total;
  document.getElementById('navCounter').textContent = (current + 1) + ' / ' + total;
  document.getElementById('subtitle').textContent = '全 ' + total + ' 問' + (activeFilter ? ' (D' + activeFilter + ')' : '');

  // buttons
  document.getElementById('btnPrev').disabled = current === 0;
  document.getElementById('btnNext').disabled = current === total - 1;

  if (!q) {{
    document.getElementById('cardContainer').innerHTML = '<div class="done-screen"><h2>表示する問題がありません</h2></div>';
    return;
  }}

  const domainBadge = DOMAIN_BADGE[q.domain] || 'badge-id';
  const domainLabel = DOMAIN_LABEL[q.domain] || '不明';
  const correctLabels = q.correct ? q.correct.split(',').map(s => s.trim()) : [];
  const userLabels = q.user_answer ? q.user_answer.split(',').map(s => s.trim()).filter(s => s && s !== 'SKIP') : [];

  // choices HTML
  let choicesHtml = '';
  (q.choices || []).forEach((c, i) => {{
    const label = 'ABCDEF'[i];
    const isCorrect = correctLabels.includes(label);
    const isUserWrong = userLabels.includes(label) && !isCorrect;
    let cls = 'choice-item';
    let mark = '';
    if (isCorrect) {{ cls += ' correct'; mark = '<span class="choice-mark">✅</span>'; }}
    if (isUserWrong) {{ cls += ' user-wrong'; mark = '<span class="choice-mark">❌</span>'; }}
    choicesHtml += `<li class="${{cls}}">
      <span class="choice-label">${{label}}</span>
      <span class="choice-text">${{escHtml(c)}}</span>
      ${{mark}}
    </li>`;
  }});

  // explanation
  let explHtml = '';
  if (q.explanation && q.explanation.trim()) {{
    explHtml = `<div class="explanation">
      <div class="explanation-title">解説</div>
      <div>${{escHtml(q.explanation)}}</div>
    </div>`;
  }} else {{
    explHtml = `<div class="explanation"><span class="no-explanation">解説データなし（問題データベースに解説が登録されていません）</span></div>`;
  }}

  // user answer row
  const userAnsDisplay = q.user_answer && q.user_answer !== 'SKIP' ? q.user_answer : 'スキップ';
  const answerRow = `<div class="answer-row">
    <div class="answer-box user">あなたの回答: ${{escHtml(userAnsDisplay)}}</div>
    <div class="answer-box correct">正解: ${{escHtml(q.correct || '?')}}</div>
  </div>`;

  document.getElementById('cardContainer').innerHTML = `
    <div class="card">
      <div class="card-meta">
        <span class="badge ${{domainBadge}}">${{domainLabel}}</span>
        <span class="badge badge-id">ID: ${{q.id}}</span>
        <span class="q-num">${{current + 1}} / ${{total}}</span>
      </div>
      <div class="question-text">${{escHtml(q.question || '（問題文データなし）')}}</div>
      <ul class="choices">${{choicesHtml}}</ul>
      ${{answerRow}}
      ${{explHtml}}
    </div>
  `;
}}

function escHtml(str) {{
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/\\n/g, '<br>');
}}

// init
render();
</script>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML生成完了: {output_path} ({total}問)")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="不正解問題レビューHTML生成")
    parser.add_argument("--repo", default=".", help="リポジトリのパス")
    parser.add_argument("--output", default="/tmp/wrong_review.html", help="出力HTMLファイルのパス")
    args = parser.parse_args()

    repo = os.path.abspath(args.repo)
    print(f"リポジトリ: {repo}")

    q_db = load_questions_db(repo)
    print(f"問題DB: {len(q_db)}問読み込み")

    questions = load_wrong_questions(repo)
    print(f"不正解問題: {len(questions)}問読み込み")

    questions = enrich_from_db(questions, q_db)

    generate_html(questions, args.output)


if __name__ == "__main__":
    main()
