# AWS SAA-C03 学習計画と進捗管理

このファイルは、AWS Certified Solutions Architect - Associate (SAA-C03) の学習進捗をトラッキングするためのものです。
AI エージェント（Claude Code / Manus）に指示して、日々の学習記録や計画の更新を行ってください。

## 📅 学習スケジュール

- **目標試験日**: [未定]
- **現在の進捗**: 学習継続中（模擬試験3回 + 通常モード1回 + 弱点復習1回 実施）

## 📊 分野別進捗状況

| 分野 | 正答率（最新） | 理解度 (1-5) | 最終学習日 |
| :--- | :--- | :--- | :--- |
| 第1分野: セキュアなアーキテクチャの設計 (30%) | 10% (1/10) ↓↓ | 1 | 2026-03-23 |
| 第2分野: 弾力性に優れたアーキテクチャの設計 (26%) | 22.2% (2/9) ↓↓ | 1 | 2026-03-23 |
| 第3分野: 高性能アーキテクチャの設計 (24%) | 33.3% (2/6) ↑ | 1 | 2026-03-23 |
| 第4分野: コストを最適化したアーキテクチャの設計 (20%) | 28.6% (2/7) ↓ | 1 | 2026-03-23 |

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

### 2026-03-23

- **学習内容**: フル模擬試験（途中終了・32問/65問）
- **スコア**: 7/32 正解（21.9%）— 合格ライン 72% には大きく届かず
- **分野別結果**:
  - Domain 1（セキュアなアーキテクチャ）: 1/10（10.0%）↓↓
  - Domain 2（弾力性）: 2/9（22.2%）↓↓
  - Domain 3（高性能）: 2/6（33.3%）↑
  - Domain 4（コスト最適化）: 2/7（28.6%）↓
- **特記事項**:
  - 全分野で正答率が低い。特に Domain 1（セキュアなアーキテクチャ）が10%と最も弱い
  - セキュリティグループ、VPN、IDS/IPS、証明書管理など基礎的なセキュリティ概念の復習が急務
  - 前回のミニ模擬試験（55.6%）から大幅に下降。問題数が増えると正答率が下がる傾向あり
- **次回やること**:
  1. Domain 1（セキュアなアーキテクチャ）の基礎を集中的に復習する
  2. セキュリティグループ・NACL・VPN・IDS/IPS の違いと使い分けを整理する
  3. 証明書管理（ACM）の基本を学ぶ
  4. 間違えた25問を弱点復習モードで解き直す
  5. 全分野の基礎概念を学習ノートで確認する

### 2026-03-23（弱点復習 7問）

- **学習内容**: 弱点復習セッション 7問
- **スコア**: 2/7 正解（28.6%）— 合格ライン 72% には大きく届かず
- **問題別結果**:
  - Q340 — Route 53 ルーティングポリシー → ❌
  - Q687 — S3 ストレージクラス (Glacier Deep Archive) → ✅
  - Q342 — Storage Gateway Cached vs Stored → ❌
  - Q361 — SQS デカップリングパターン → ✅
  - Q557 — EC2 購入オプション (Spot vs RI) → ❌
  - Q463 — EBS CloudWatch メトリクス → ❌
  - Q358 — Direct Connect/VPN 移行手順 → ❌
- **克服できた弱点**:
  - S3 Glacier Deep Archive のストレージクラス選択（Q687）
  - SQS によるデカップリングパターン（Q361）
- **依然として弱い分野**:
  - Route 53 ルーティングポリシー（繰り返し間違えている）
  - Storage Gateway の Cached Volume vs Stored Volume の違い
  - EC2 購入オプション（Spot / Reserved Instance の使い分け）
  - EBS の CloudWatch メトリクス（VolumeQueueLength 等）
  - Direct Connect / VPN の移行手順・構成パターン
- **⚠️ 重点学習が必要な分野**:
  - **Domain 3（高性能アーキテクチャ）**: Route 53、Storage Gateway、EBS メトリクスなどインフラ基盤の理解が不足
  - **Domain 4（コスト最適化）**: EC2 購入オプションの使い分けが定着していない
  - **Domain 2（弾力性）**: Direct Connect/VPN の移行・冗長構成の理解が必要
- **次回やること**:
  1. Route 53 ルーティングポリシー（シンプル/加重/レイテンシー/フェイルオーバー/地理的近接性/複数値）を整理して notes に記録する
  2. Storage Gateway の3タイプ（File/Volume Cached/Volume Stored/Tape）を比較表にまとめる
  3. EC2 購入オプションのユースケース別選択基準を整理する
  4. EBS CloudWatch メトリクスの主要指標を学ぶ
  5. Direct Connect + VPN のハイブリッド構成パターンを復習する

### 2026-03-23（通常モード 10問）
- 正答率: 43%（3/7）
- 学んだ概念: S3 Glacier Flexible vs Deep Archive の取得時間差、ELB vs Route 53 の役割分担、VPC エンドポイント（ゲートウェイ型）、Lambda によるEC2スケジュール起動停止
- 弱点: コスト最適化（使用率に応じた最適戦略）、ネットワーク（VPC エンドポイント vs Direct Connect）

### 2026-03-22（2回目）

- **学習内容**: ミニ模擬試験 11問（9問採点）
- **スコア**: 5/9 正解（55.6%）— 前回 24.2% から **+31.4pt 改善**
- **改善が見られた分野**:
  - Domain 2（弾力性）: 20% → 100% — DR 戦略、EFS、CloudTrail 組織トレイル、S3+CloudFront 構成を正しく理解
  - Domain 1（セキュリティ）: 22% → 33% — 改善傾向あり
- **まだ弱い分野**:
  - Domain 3（高性能）: 0% — Auto Scaling クールダウン計算、DAX vs ElastiCache
  - Domain 1: AWS Shield vs WAF の違い、S3 暗号化方式（SSE-S3 vs SSE-KMS）
- **新たに学んだポイント**:
  - Auto Scaling クールダウンは最後のアクティビティから起算
  - Shield = DDoS、WAF = アプリ層保護、CloudFront = 地理的制限
  - SSE-KMS CMK = 自社管理+自動ローテーション+監査の3要件対応
  - DAX = DynamoDB 専用キャッシュ（コード変更最小）
- **次回やること**:
  1. Domain 3 の強化（Auto Scaling、DynamoDB DAX）
  2. S3 暗号化方式の比較を整理する
  3. AWS Shield / WAF / CloudFront の機能範囲を整理する
  4. 間違えた4問を復習モードで解き直す

---

## 🤖 AI エージェントへの指示例

- 「今日の学習記録を `progress/study-plan.md` に追加して。内容は...」
- 「第1分野の理解度を 3 に更新して」
- 「現在の進捗状況から、試験日までの最適な学習スケジュールを提案して」
- 「弱点問題を復習したい」（→ `practice-tests/wrong-answers/` から出題）
- 「今日の試験結果を記録して」（→ AI が自動で study-plan.md と weakness-analysis.md を更新）
