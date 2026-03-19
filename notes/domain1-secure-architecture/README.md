# 第1分野: セキュアなアーキテクチャの設計 (30%)

SAA-C03 で最も配点が高い分野（30%）です。IAM・ネットワークセキュリティ・データ保護の3つの柱を中心に学習を進めてください。

## 📋 タスクステートメント

| タスク | 内容 |
| :--- | :--- |
| 1.1 | AWS リソースへのセキュアなアクセスの設計 |
| 1.2 | セキュアなワークロードとアプリケーションの設計 |
| 1.3 | 適切なデータセキュリティ管理の決定 |

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

---

*このファイルは AI エージェントによって随時更新されます。*
*「Domain 1 のノートを更新して」と指示することで、学習内容を追記できます。*
