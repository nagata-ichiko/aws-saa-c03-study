# AWS SAA-C03 学習計画と進捗管理

このファイルは、AWS Certified Solutions Architect - Associate (SAA-C03) の学習進捗をトラッキングするためのものです。
AI エージェント（Claude Code / Manus）に指示して、日々の学習記録や計画の更新を行ってください。

## 📅 学習スケジュール

- **目標試験日**: [未定]
- **現在の進捗**: 学習開始（初回模擬試験完了）

## 📊 分野別進捗状況

| 分野 | 正答率（最新） | 理解度 (1-5) | 最終学習日 |
| :--- | :--- | :--- | :--- |
| 第1分野: セキュアなアーキテクチャの設計 (30%) | 22% (2/9) | 1 | 2026-03-22 |
| 第2分野: 弾力性に優れたアーキテクチャの設計 (26%) | 20% (1/5) | 1 | 2026-03-22 |
| 第3分野: 高性能アーキテクチャの設計 (24%) | 0% (0/3) | 1 | 2026-03-22 |
| 第4分野: コストを最適化したアーキテクチャの設計 (20%) | 0% (0/2) | 1 | 2026-03-22 |

> 詳細な弱点分析は [`progress/weakness-analysis.md`](./weakness-analysis.md) を参照。

---

## 📝 日々の学習記録

### 2026-03-22

- **学習内容**: 初回模擬試験 33問（全ドメイン混合）
- **スコア**: 8/33 正解（24.2%）— 合格ライン 72% まで大きく届かず
- **理解できていること**:
  - GuardDuty + EventBridge + Lambda による脅威自動対応フロー
  - Amazon MSK と Kinesis の使い分け（高可用性ストリーム処理 = MSK）
  - EBS スナップショットによるボリューム再作成
  - EBS の RAID 5/6 非推奨（パリティ書き込みオーバーヘッドが原因）
  - AMI の入手方法（自作・Marketplace 購入）
  - SNS トピック作成時の ARN 発行
- **弱点・課題**:
  - Route 53 の全ルーティングポリシーの使い分けが曖昧
  - Direct Connect / Transit Gateway / VPN の使い分けが不明確
  - Aurora リードレプリカ vs DAX の違いを混同（DAX は DynamoDB 専用）
  - AWS Config / CloudTrail / Inspector / GuardDuty の役割分担が不明確
  - 暗号化 EBS ボリュームのスナップショット・コピー時の動作
  - NAT インスタンスの Source/Destination Check 設定
  - EC2 購入オプション（オンデマンド/Reserved/Spot/Savings Plans）の詳細
  - S3 Storage Gateway の種類（File/Volume/Tape）と使い分け
- **次回やること**:
  1. Domain 3（高性能アーキテクチャ）の学習ノートを読む
  2. Route 53 ルーティングポリシーを整理する
  3. Direct Connect + Transit Gateway の構成パターンを学ぶ
  4. 弱点問題を復習モードで解き直す

---

## 🤖 AI エージェントへの指示例

- 「今日の学習記録を `progress/study-plan.md` に追加して。内容は...」
- 「第1分野の理解度を 3 に更新して」
- 「現在の進捗状況から、試験日までの最適な学習スケジュールを提案して」
- 「弱点問題を復習したい」（→ `practice-tests/wrong-answers/` から出題）
- 「今日の試験結果を記録して」（→ AI が自動で study-plan.md と weakness-analysis.md を更新）
