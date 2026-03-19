# 第1分野: セキュアなアーキテクチャの設計 (30%)

SAA-C03 で最も配点が高い分野（30%）です。IAM・ネットワークセキュリティ・データ保護の3つの柱を中心に学習を進めてください。

## 📋 タスクステートメント

### 1.1 AWS リソースへのセキュアなアクセスの設計
- **複数アカウントのアクセス制御と管理**: AWS Organizations, Service Control Policies (SCP), AWS Control Tower
- **フェデレーションと ID サービス**: AWS IAM, AWS IAM Identity Center (旧 AWS SSO)
- **セキュリティのベストプラクティス**: 最小権限の原則 (Principle of least privilege), MFA (多要素認証)
- **ロールベースのアクセス制御**: AWS STS, ロールの切り替え, クロスアカウントアクセス

### 1.2 セキュアなワークロードとアプリケーションの設計
- **ネットワークセキュリティ**: VPC, セキュリティグループ, ネットワーク ACL, NAT ゲートウェイ
- **ネットワークのセグメンテーション**: パブリックサブネットとプライベートサブネットの使い分け
- **外部からの脅威防御**: AWS WAF, AWS Shield, Amazon GuardDuty, Amazon Macie
- **セキュアな接続**: AWS Client VPN, AWS Site-to-Site VPN, AWS Direct Connect

### 1.3 適切なデータセキュリティ管理の決定
- **保管中のデータの暗号化**: AWS KMS (Key Management Service), CloudHSM
- **転送中のデータの暗号化**: AWS Certificate Manager (ACM), TLS
- **データのバックアップとレプリケーション**: S3 クロスリージョンレプリケーション, AWS Backup
- **データのライフサイクルと保護**: S3 オブジェクトロック, S3 バージョニング

## 🔑 重要サービス一覧

| カテゴリ | サービス | 重要度 |
| :--- | :--- | :--- |
| ID・アクセス管理 | IAM, AWS Organizations, SCP, IAM Identity Center (SSO) | ⭐⭐⭐ |
| ネットワークセキュリティ | Security Groups, NACL, WAF, Shield, Firewall Manager | ⭐⭐⭐ |
| 暗号化・鍵管理 | KMS, CloudHSM, ACM, Secrets Manager, Parameter Store | ⭐⭐⭐ |
| 脅威検知・監視 | GuardDuty, Inspector, Macie, Security Hub, CloudTrail | ⭐⭐ |

## 📝 学習ノート

### IAM の基礎

IAM（Identity and Access Management）は AWS リソースへのアクセスを制御するサービスです。
試験では、**最小権限の原則**（Principle of Least Privilege）に基づいたポリシー設計が頻出です。

**ポリシー評価ロジック（重要）**

1. デフォルトはすべて **Deny**
2. 明示的な **Allow** があれば許可
3. 明示的な **Deny** があれば、Allow があっても **必ず拒否**

**IAM ロール vs IAM ユーザー**

| 項目 | IAM ユーザー | IAM ロール |
| :--- | :--- | :--- |
| 認証情報 | 長期（パスワード・アクセスキー） | 一時的（STS トークン） |
| 主な用途 | 人間のオペレーター | AWS サービス・外部 ID プロバイダー |
| ベストプラクティス | MFA を有効化、アクセスキーは極力使わない | EC2 インスタンスプロファイルなどで活用 |

### ネットワークセキュリティの階層防御

VPC 内のリソースを保護するためには、セキュリティグループとネットワーク ACL を組み合わせて使用します。

| 特徴 | セキュリティグループ | ネットワーク ACL (NACL) |
| :--- | :--- | :--- |
| 適用範囲 | インスタンスレベル (ENI) | サブネットレベル |
| ステート | ステートフル (戻りのトラフィックは自動許可) | ステートレス (戻りのトラフィックも明示的な許可が必要) |
| ルール | 許可ルールのみ | 許可ルールと拒否ルールの両方 |
| 評価順序 | すべてのルールを評価 | 番号の若い順に評価 |

---

*このファイルは AI エージェントによって随時更新されます。*
*「Domain 1 のノートを更新して」と指示することで、学習内容を追記できます。*
