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

LABELS = ["A", "B", "C", "D", "E", "F"]
DOMAIN_NAMES = {1: "D1: セキュリティ", 2: "D2: 弾力性", 3: "D3: 高性能", 4: "D4: コスト最適化"}


def load_questions_db(repo):
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

    result = []
    for qid in sorted(files_by_id.keys(), key=lambda x: int(x)):
        path = files_by_id[qid]
        with open(path) as f:
            content = f.read()

        domain_m = re.search(r"\*\*ドメイン:\*\* D(\d)", content)
        domain = int(domain_m.group(1)) if domain_m else 0

        q_m = re.search(r"## 問題\n\n(.*?)\n## 選択肢", content, re.DOTALL)
        question = q_m.group(1).strip() if q_m else ""

        choices_m = re.search(r"## 選択肢\n\n(.*?)\n## あなたの回答", content, re.DOTALL)
        choices_raw = choices_m.group(1).strip() if choices_m else ""
        choices = re.findall(r"- \*\*[A-F]\.\*\* (.+)", choices_raw)

        correct_m = re.search(r"## 正解: (.+)", content)
        correct = correct_m.group(1).strip() if correct_m else ""

        expl_m = re.search(r"## 解説\n\n?(.*?)$", content, re.DOTALL)
        explanation = expl_m.group(1).strip() if expl_m else ""

        user_ans_m = re.search(r"## あなたの回答: (.+)", content)
        user_answer = user_ans_m.group(1).strip() if user_ans_m else ""

        result.append({
            "id": qid,
            "domain": domain,
            "question": question,
            "choices": choices,
            "correct": correct,
            "explanation": explanation,
            "user_answer": user_answer,
            "path": path,
        })
    return result


def enrich_from_db(questions, q_db):
    for q in questions:
        db_q = q_db.get(q["id"])
        if not db_q:
            continue
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
        if not q["correct"] and db_q.get("correct"):
            q["correct"] = ",".join([LABELS[i] for i in db_q["correct"] if i < len(LABELS)])
    return questions


def generate_html(questions, output_path):
    total = len(questions)
    questions_json = json.dumps(questions, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AWS SAA-C03 不正解問題レビュー ({total}問)</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  :root {{
    --bg: #0d1117;
    --surface: #161b22;
    --surface2: #1c2128;
    --border: #30363d;
    --border-light: #21262d;
    --text-primary: #e6edf3;
    --text-secondary: #8b949e;
    --text-muted: #484f58;
    --blue: #58a6ff;
    --green: #3fb950;
    --green-bg: #0d2818;
    --green-border: #238636;
    --red: #f85149;
    --red-bg: #2d0f0f;
    --red-border: #da3633;
    --purple: #bc8cff;
    --yellow: #e3b341;
    --radius: 12px;
    --radius-sm: 8px;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans JP', sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    font-size: 15px;
    line-height: 1.6;
  }}

  /* ── ヘッダー ── */
  .header {{
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 14px 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    position: sticky;
    top: 0;
    z-index: 200;
  }}
  .header-title {{
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-primary);
    white-space: nowrap;
  }}
  .header-sub {{
    font-size: 0.75rem;
    color: var(--text-secondary);
    white-space: nowrap;
  }}
  .progress-wrap {{ flex: 1; }}
  .progress-track {{
    background: var(--border);
    border-radius: 999px;
    height: 6px;
    overflow: hidden;
  }}
  .progress-fill {{
    background: linear-gradient(90deg, var(--blue), var(--purple));
    height: 100%;
    border-radius: 999px;
    transition: width 0.35s ease;
  }}
  .progress-label {{
    font-size: 0.72rem;
    color: var(--text-muted);
    text-align: right;
    margin-top: 4px;
  }}

  /* ── フィルターバー ── */
  .filter-bar {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    padding: 14px 24px 0;
    max-width: 900px;
    margin: 0 auto;
  }}
  .filter-btn {{
    padding: 5px 14px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--surface2);
    color: var(--text-secondary);
    font-size: 0.78rem;
    cursor: pointer;
    transition: all 0.15s;
    font-weight: 500;
  }}
  .filter-btn:hover:not(.active) {{ background: var(--border); color: var(--text-primary); }}
  .filter-btn.active {{ background: var(--blue); color: #fff; border-color: var(--blue); }}

  /* ── メインコンテンツ ── */
  .main {{
    max-width: 900px;
    margin: 0 auto;
    padding: 20px 24px 100px;
  }}

  /* ── カード ── */
  .card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
  }}

  /* カードヘッダー */
  .card-head {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 20px;
    border-bottom: 1px solid var(--border-light);
    background: var(--surface2);
  }}
  .badge {{
    display: inline-flex;
    align-items: center;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    border: 1px solid;
  }}
  .badge-d1 {{ background: #0d1f3c; color: #79c0ff; border-color: #1f4d8a; }}
  .badge-d2 {{ background: #0d2818; color: #56d364; border-color: #1a5c2a; }}
  .badge-d3 {{ background: #2d1f00; color: #e3b341; border-color: #5c3d00; }}
  .badge-d4 {{ background: #1d1040; color: #bc8cff; border-color: #4a2d8a; }}
  .badge-id {{ background: var(--surface2); color: var(--text-muted); border-color: var(--border); }}
  .card-qnum {{ margin-left: auto; font-size: 0.78rem; color: var(--text-muted); font-weight: 600; }}

  /* 問題文 */
  .question-block {{
    padding: 24px 24px 20px;
    border-bottom: 1px solid var(--border-light);
  }}
  .question-label {{
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--blue);
    margin-bottom: 10px;
  }}
  .question-text {{
    font-size: 1.05rem;
    line-height: 1.85;
    color: var(--text-primary);
    font-weight: 400;
  }}

  /* 選択肢 */
  .choices-block {{
    padding: 20px 24px;
    border-bottom: 1px solid var(--border-light);
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  .choice-item {{
    display: flex;
    align-items: flex-start;
    gap: 0;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    background: var(--surface2);
    overflow: hidden;
    transition: border-color 0.2s;
  }}
  .choice-item.correct {{
    border-color: var(--green-border);
    background: var(--green-bg);
  }}
  .choice-item.user-wrong {{
    border-color: var(--red-border);
    background: var(--red-bg);
  }}
  .choice-label-col {{
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 44px;
    padding: 14px 0;
    font-size: 0.95rem;
    font-weight: 800;
    color: var(--text-muted);
    border-right: 1px solid var(--border);
    background: rgba(0,0,0,0.15);
    align-self: stretch;
  }}
  .choice-item.correct .choice-label-col {{
    color: var(--green);
    border-right-color: var(--green-border);
    background: rgba(63,185,80,0.08);
  }}
  .choice-item.user-wrong .choice-label-col {{
    color: var(--red);
    border-right-color: var(--red-border);
    background: rgba(248,81,73,0.08);
  }}
  .choice-text-col {{
    flex: 1;
    padding: 14px 16px;
    font-size: 0.95rem;
    line-height: 1.7;
    color: var(--text-primary);
  }}
  .choice-item.correct .choice-text-col {{ color: #aff5b4; }}
  .choice-item.user-wrong .choice-text-col {{ color: #ffa198; }}
  .choice-mark-col {{
    display: flex;
    align-items: center;
    padding: 0 14px;
    font-size: 1.1rem;
    align-self: stretch;
  }}

  /* 回答行 */
  .answer-block {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 24px;
    border-bottom: 1px solid var(--border-light);
    background: var(--surface2);
    flex-wrap: wrap;
  }}
  .answer-label {{
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
  }}
  .answer-chip {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: var(--radius-sm);
    font-size: 0.88rem;
    font-weight: 700;
    border: 1px solid;
  }}
  .answer-chip.user-chip {{
    background: var(--red-bg);
    color: #ffa198;
    border-color: var(--red-border);
  }}
  .answer-chip.correct-chip {{
    background: var(--green-bg);
    color: #aff5b4;
    border-color: var(--green-border);
  }}
  .answer-arrow {{ color: var(--text-muted); font-size: 1rem; }}

  /* 解説 */
  .explanation-block {{
    padding: 20px 24px;
  }}
  .explanation-label {{
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--purple);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .explanation-label::before {{
    content: '';
    display: inline-block;
    width: 3px;
    height: 14px;
    background: var(--purple);
    border-radius: 2px;
  }}
  .explanation-text {{
    font-size: 0.95rem;
    line-height: 1.85;
    color: var(--text-secondary);
    background: var(--surface2);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    padding: 16px 20px;
  }}
  .no-explanation {{
    font-size: 0.88rem;
    color: var(--text-muted);
    font-style: italic;
    padding: 12px 16px;
    background: var(--surface2);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
  }}

  /* ── ナビゲーション ── */
  .nav {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(13,17,23,0.95);
    backdrop-filter: blur(12px);
    border-top: 1px solid var(--border);
    padding: 12px 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    z-index: 200;
  }}
  .btn {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 28px;
    border-radius: var(--radius-sm);
    border: 1px solid;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
    letter-spacing: 0.01em;
  }}
  .btn-primary {{
    background: var(--blue);
    color: #0d1117;
    border-color: var(--blue);
  }}
  .btn-primary:hover {{ background: #79c0ff; border-color: #79c0ff; }}
  .btn-secondary {{
    background: var(--surface2);
    color: var(--text-secondary);
    border-color: var(--border);
  }}
  .btn-secondary:hover {{ background: var(--border); color: var(--text-primary); }}
  .btn:disabled {{ opacity: 0.3; cursor: not-allowed; pointer-events: none; }}
  .nav-counter {{
    font-size: 0.85rem;
    color: var(--text-muted);
    min-width: 70px;
    text-align: center;
    font-weight: 600;
  }}

  /* ── 空状態 ── */
  .empty-state {{
    text-align: center;
    padding: 80px 20px;
    color: var(--text-muted);
    font-size: 1rem;
  }}
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="header-title">AWS SAA-C03 不正解問題レビュー</div>
    <div class="header-sub" id="headerSub">全 {total} 問</div>
  </div>
  <div class="progress-wrap">
    <div class="progress-track">
      <div class="progress-fill" id="progressFill" style="width:0%"></div>
    </div>
    <div class="progress-label" id="progressLabel">0 / {total}</div>
  </div>
</div>

<div class="filter-bar">
  <button class="filter-btn active" onclick="setFilter(0)">すべて</button>
  <button class="filter-btn" onclick="setFilter(1)">D1: セキュリティ</button>
  <button class="filter-btn" onclick="setFilter(2)">D2: 弾力性</button>
  <button class="filter-btn" onclick="setFilter(3)">D3: 高性能</button>
  <button class="filter-btn" onclick="setFilter(4)">D4: コスト最適化</button>
</div>

<div class="main">
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

const DOMAIN_BADGE = {{ 1:'badge-d1', 2:'badge-d2', 3:'badge-d3', 4:'badge-d4' }};
const DOMAIN_LABEL = {{ 1:'D1: セキュリティ', 2:'D2: 弾力性', 3:'D3: 高性能', 4:'D4: コスト最適化', 0:'不明' }};

function setFilter(domain) {{
  activeFilter = domain;
  document.querySelectorAll('.filter-btn').forEach((b, i) => b.classList.toggle('active', i === domain));
  filtered = domain === 0 ? [...ALL_QUESTIONS] : ALL_QUESTIONS.filter(q => q.domain === domain);
  current = 0;
  render();
}}

function navigate(dir) {{
  current = Math.max(0, Math.min(filtered.length - 1, current + dir));
  render();
  window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function esc(str) {{
  return String(str || '')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;').replace(/\\n/g,'<br>');
}}

function render() {{
  const total = filtered.length;
  const q = filtered[current];

  // progress
  const pct = total > 0 ? Math.round((current + 1) / total * 100) : 0;
  document.getElementById('progressFill').style.width = pct + '%';
  document.getElementById('progressLabel').textContent = (current + 1) + ' / ' + total;
  document.getElementById('navCounter').textContent = (current + 1) + ' / ' + total;
  document.getElementById('headerSub').textContent = '全 ' + total + ' 問' + (activeFilter ? ' (D' + activeFilter + ')' : '');
  document.getElementById('btnPrev').disabled = current === 0;
  document.getElementById('btnNext').disabled = current === total - 1;

  if (!q) {{
    document.getElementById('cardContainer').innerHTML = '<div class="empty-state">表示する問題がありません</div>';
    return;
  }}

  const domainBadge = DOMAIN_BADGE[q.domain] || 'badge-id';
  const domainLabel = DOMAIN_LABEL[q.domain] || '不明';
  const correctLabels = q.correct ? q.correct.split(',').map(s => s.trim()) : [];
  const userLabels = q.user_answer ? q.user_answer.split(',').map(s => s.trim()).filter(s => s && s !== 'SKIP') : [];

  // 選択肢HTML
  let choicesHtml = '';
  (q.choices || []).forEach((c, i) => {{
    const label = 'ABCDEF'[i];
    const isCorrect = correctLabels.includes(label);
    const isUserWrong = userLabels.includes(label) && !isCorrect;
    let cls = 'choice-item';
    let mark = '';
    if (isCorrect) {{ cls += ' correct'; mark = '<div class="choice-mark-col">✅</div>'; }}
    else if (isUserWrong) {{ cls += ' user-wrong'; mark = '<div class="choice-mark-col">❌</div>'; }}
    choicesHtml += `
      <div class="${{cls}}">
        <div class="choice-label-col">${{label}}</div>
        <div class="choice-text-col">${{esc(c)}}</div>
        ${{mark}}
      </div>`;
  }});

  // 回答表示
  const userAnsDisplay = q.user_answer && q.user_answer !== 'SKIP' ? q.user_answer : 'スキップ';
  const answerHtml = `
    <div class="answer-block">
      <span class="answer-label">回答</span>
      <span class="answer-chip user-chip">✗ ${{esc(userAnsDisplay)}}</span>
      <span class="answer-arrow">→</span>
      <span class="answer-chip correct-chip">✓ 正解: ${{esc(q.correct || '?')}}</span>
    </div>`;

  // 解説HTML
  let explHtml = '';
  if (q.explanation && q.explanation.trim()) {{
    explHtml = `<div class="explanation-block">
      <div class="explanation-label">解説</div>
      <div class="explanation-text">${{esc(q.explanation)}}</div>
    </div>`;
  }} else {{
    explHtml = `<div class="explanation-block">
      <div class="explanation-label">解説</div>
      <div class="no-explanation">解説データなし（問題データベースに解説が登録されていません）</div>
    </div>`;
  }}

  document.getElementById('cardContainer').innerHTML = `
    <div class="card">
      <div class="card-head">
        <span class="badge ${{domainBadge}}">${{domainLabel}}</span>
        <span class="badge badge-id">ID: ${{q.id}}</span>
        <span class="card-qnum">${{current + 1}} / ${{total}}</span>
      </div>
      <div class="question-block">
        <div class="question-label">問題</div>
        <div class="question-text">${{esc(q.question || '（問題文データなし）')}}</div>
      </div>
      <div class="choices-block">${{choicesHtml}}</div>
      ${{answerHtml}}
      ${{explHtml}}
    </div>`;
}}

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
