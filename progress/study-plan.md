# AWS SAA-C03 学習計画と進捗管理

このファイルは、AWS Certified Solutions Architect - Associate (SAA-C03) の学習進捗をトラッキングするためのものです。
AI エージェント（Claude Code / Manus）に指示して、日々の学習記録や計画の更新を行ってください。

## 📅 学習スケジュール

- **目標試験日**: [未定]
- **現在の進捗**: 学習継続中（模擬試験4回実施）

## 📊 分野別進捗状況

| 分野 | 正答率（最新） | 理解度 (1-5) | 最終学習日 |
| :--- | :--- | :--- | :--- |
| 第1分野: セキュアなアーキテクチャの設計 (30%) | 33.3% (5/15) ↑ | 1 | 2026-03-27 |
| 第2分野: 弾力性に優れたアーキテクチャの設計 (26%) | 40.0% (6/15) ↑ | 1 | 2026-03-27 |
| 第3分野: 高性能アーキテクチャの設計 (24%) | 63.6% (7/11) ↓ | 2 | 2026-03-27 |
| 第4分野: コストを最適化したアーキテクチャの設計 (20%) | 42.9% (3/7) ↑ | 1 | 2026-03-27 |

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

### 2026-03-23（通常モード 10問）
- 正答率: 43%（3/7）
- 学んだ概念: S3 Glacier Flexible vs Deep Archive の取得時間差、ELB vs Route 53 の役割分担、VPC エンドポイント（ゲートウェイ型）、Lambda によるEC2スケジュール起動停止
- 弱点: コスト最適化（使用率に応じた最適戦略）、ネットワーク（VPC エンドポイント vs Direct Connect）

### 2026-03-24

- **学習内容**: フル模擬試験（65問・完走）
- **スコア**: 25/65 正解（38.5%）— 合格ライン 72% には未達だが前回（21.9%）から改善
- **分野別結果**:
  - Domain 1（セキュアなアーキテクチャ）: 5/20（25.0%）↑ 前回10.0%から改善
  - Domain 2（弾力性）: 5/17（29.4%）↑ 前回22.2%から改善
  - Domain 3（高性能）: 10/15（66.7%）↑↑ 前回33.3%から大幅改善
  - Domain 4（コスト最適化）: 5/13（38.5%）↑ 前回28.6%から改善
- **特記事項**:
  - 全分野で前回から改善。特に Domain 3 が 66.7% と大幅に伸びた
  - Domain 1（セキュリティ）が 25.0% で最も弱く、IAM ロール、Presigned URL、OAI、Secrets Manager、AWS Config 等の基礎が不十分
  - Domain 2 も 29.4% と低く、Route 53、Auto Scaling、Aurora Global Database の理解が必要
  - 65問フル完走は初めて（前回は32問で途中終了）
- **次回やること**:
  1. Domain 1 集中強化: IAMロール、Presigned URL、CloudFront OAI、Secrets Manager、AWS Config、Web Identity Federation、責任共有モデル
  2. Domain 2 強化: Route 53 ルーティングポリシー、Auto Scaling（通知・クールダウン）、Aurora Global Database、S3 ライフサイクル
  3. Domain 4 強化: S3 ストレージクラス選択、ECS Fargate、スポットインスタンス
  4. 間違えた40問を弱点復習モードで解き直す

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

----

### 2026-03-27

- **学習内容**: フル模擬試験 48問（65問中途中終了）
- **スコア**: 21/48 正解（43.8%）— 合格ライン 72% まであと 28.2pt
- **ドメイン別成績**:
  - Domain 1（セキュリティ）: 5/15 = 33.3%（引き続き最弱分野）
  - Domain 2（弾力性）: 6/15 = 40.0%
  - Domain 3（高パフォーマンス）: 7/11 = 63.6%（最も高い）
  - Domain 4（コスト最適化）: 3/7 = 42.9%
- **継続する弱点**:
  - SNS vs SQS の混同（プッシュ型 = SNS）
  - EC2 購入オプションの使い分け（期間限定 → スポット、安定稼働 → Reserved）
  - Auto Scaling 通知設定（Launch Config でなく Auto Scaling グループで設定）
  - RDS リードレプリカ vs Multi-AZ スタンバイの役割分担
  - Global Accelerator vs Route 53 の使い分け
  - VPN CloudHub の BGP ASN 設定
  - Parameter Store vs Secrets Manager の選択基準
  - AZ 名のアカウント間マッピングの概念
- **次回やること**:
  1. SNS / SQS / Kinesis の役割分担を整理する
  2. EC2 購入オプション（オンデマンド/Reserved/Spot/Savings Plans）を整理する
  3. Auto Scaling のスケーリングポリシー・通知・クールダウンを復習する
  4. RDS リードレプリカ vs Multi-AZ の用途を整理する
  5. 弱点問題を復習モードで解き直す

---
## 🤖 AI エージェントへの指示例

- 「今日の学習記録を `progress/study-plan.md` に追加して。内容は...」
- 「第1分野の理解度を 3 に更新して」
- 「現在の進捗状況から、試験日までの最適な学習スケジュールを提案して」
- 「弱点問題を復習したい」（→ `practice-tests/wrong-answers/` から出題）
- 「今日の試験結果を記録して」（→ AI が自動で study-plan.md と weakness-analysis.md を更新）
