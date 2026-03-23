# 弱点分析・理解度トラッキング

このファイルは模擬試験の結果から自動生成される弱点・理解済みポイントの記録です。
AI エージェントが試験終了後に自動更新します。

---

## 📊 累計スコア推移

| 日付 | 問題数 | 正解数 | 正答率 | 合否ライン(72%) |
| :--- | ---: | ---: | ---: | :--- |
| 2026-03-22 | 33 | 8 | 24.2% | ❌ 未達 |
| 2026-03-22 (2回目) | 9（採点分） | 5 | 55.6% | ❌ 未達（改善傾向） |
| 2026-03-23 | 11 | 5 | 45.5% | ❌ 未達 |
| 2026-03-23 (2回目) | 32（途中終了） | 7 | 21.9% | ❌ 未達 |
| 2026-03-23 (3回目) | 7（記録分） | 3 | 43% | ❌ 未達 |

---

## 🔴 弱点ポイント（要強化）

### Domain 1: セキュアなアーキテクチャの設計（累計: 3/19 = 16%）

**理解が不十分なトピック:**

| トピック | 間違えた問題 | 具体的な誤解・ギャップ |
| :--- | :--- | :--- |
| AWS Config vs CloudTrail vs Inspector | Q17 | S3 設定変更の監視は Config が担当。CloudTrail はAPI呼び出しログ、Inspector は脆弱性スキャン |
| EBS スナップショットのアクセス制御 | Q18 | スナップショットはデフォルトでプライベート。共有するには明示的な許可が必要 |
| Auto Scaling 終了ポリシー | Q11 | 「最初に請求時間に最も近いインスタンスを削除」= OldestInstance ではなく ClosestToNextInstanceHour |
| セキュリティグループ vs NACL の使い分け | Q25, Q32 | インスタンス間通信の制御はセキュリティグループ（ステートフル）が適切。NACL はステートレスで管理が複雑。**再度間違えた**: セキュリティグループ＝インスタンスレベル（ステートフル）、ネットワーク ACL＝サブネットレベル（ステートレス）の多層防御構造を問う問題で VPC Security Groups を選んでしまった |
| EC2 移行後のパッチ管理 | Q9 | 大量 EC2 のパッチ管理は AWS Systems Manager Patch Manager が最適 |
| HTTPS と TLS の関係 | Q28 | SSL/TLS を使った HTTP 通信 = HTTPS。TLS は SSL の後継プロトコル名であり、AWS では HTTPS を使う |
| AWS Shield vs WAF の違い | ミニQ6 | Shield = DDoS 防御、WAF = アプリケーション層保護（SQL インジェクション等）。地理的制限は CloudFront の機能 |
| S3 暗号化方式の使い分け | ミニQ7, Q146 | SSE-S3 は AWS 完全管理でキー制御不可。自社管理+自動ローテーション+監査 = SSE-KMS CMK が正解。**再度間違えた（3回目）**: 保存データ暗号化 = SSE-KMS / SSE-C / クライアントサイド暗号化の3種。EC2キーペアはSSH用で暗号化に無関係。SSL は転送中の暗号化であり保存データ暗号化ではない |
| VPC での IDS/IPS 設計 | Q5 | 各インスタンスにホストベースのエージェントをインストール + リバースプロキシ層で検査。VPC Flow Logs だけでは不十分 |
| EC2 テナンシー属性 | Q96 | Dedicated テナンシー = 専用ハードウェアで実行。Shared（デフォルト）、Dedicated Host との違いを整理する必要あり |
| デフォルトセキュリティグループの初期設定 | Q590 | デフォルトSG: インバウンド = 同SG内からのみ許可、アウトバウンド = 全許可。ユーザー作成SGとは異なる |
| ユーザー作成SGの初期設定 | Q217 | ユーザー作成SG: インバウンド = 全拒否、アウトバウンド = 全許可。デフォルトSGとの違いに注意 |
| 他サービス所有インターフェースのSG変更 | Q21 | ELB等の他サービスが管理するENIのSG変更は、そのサービス固有のコンソール/APIから行う |
| Bastion Host SG設定 | Q224 | Bastion Host のインバウンドSG = TCP/22（SSH）、ソースは管理者IPの /32 CIDR で限定する |
| Auto Scaling + SNS通知 + 鍵管理 | Q145 | Auto Scaling でスケールイン/アウト時の SNS 通知設定、鍵管理サービスによる証明書署名の組み合わせ |
| S3 バケット/オブジェクト作成者の権限 | Q328 | S3 はバケットやオブジェクトの作成者に対して自動的に他の権限を付与しない。明示的なポリシー設定が必要 |
| 大量EC2への緊急パッチ適用 | Q701 | Systems Manager Run Command で複数EC2に一括コマンド実行。Patch Manager とは異なる即時実行ツール |

**学習優先度: 最高（正答率 10.0%）**
- [ ] AWS Config のルールと自動修復の仕組みを学ぶ
- [ ] IAM ポリシー・リソースポリシーの違いを整理する
- [ ] Systems Manager の主要機能（Patch Manager, Session Manager, Parameter Store, Run Command）を学ぶ
- [ ] セキュリティグループの種類別初期設定（デフォルトSG vs ユーザー作成SG）を整理する
- [ ] EC2 テナンシーオプション（Shared / Dedicated Instance / Dedicated Host）を整理する
- [ ] VPC セキュリティ設計（IDS/IPS、Bastion Host）のベストプラクティスを学ぶ

---

### Domain 2: 弾力性に優れたアーキテクチャの設計（累計: 3/14 = 21%）

**理解が不十分なトピック:**

| トピック | 間違えた問題 | 具体的な誤解・ギャップ |
| :--- | :--- | :--- |
| マルチリージョン API の高可用性設計 | Q1 | Route 53 フェイルオーバー + API Gateway マルチリージョン + CloudFront が正解パターン |
| Route 53 ルーティングポリシーの組み合わせ | Q31 | レイテンシー最適化 + フェイルオーバー = レイテンシールーティング + ヘルスチェックの組み合わせ |
| Route 53 リソースレコードの仕様 | Q6 | 複数選択問題。Alias レコードと CNAME の違い、TTL の扱いを整理する必要あり |
| 静的ウェブサイトホスティング | Q5 | S3 静的ウェブサイトホスティングが最もシンプル・低コスト |
| Lambda スケーラビリティ改善 | Q689 | Lambda のスケーラビリティ問題は SQS キューで分離して解決。非同期処理パターンの理解が必要 |
| トランスポート層の高可用性 | Q672 | トランスポート層（L4）= NLB が最適。Multi-AZ Auto Scaling と組み合わせて高可用性を実現 |
| RDS Multi-AZ 強制フェイルオーバー | Q185 | RDS Multi-AZ では手動で強制フェイルオーバーが可能。テストや計画的切り替えに使用 |
| リアルタイムストリーミング処理 | Q548 | リアルタイムストリーミング = Kinesis Data Streams。SQS は複数コンシューマーへの同時配信ができない |
| Route 53 NS レコード | Q503 | NS = Name Server レコード。ドメインの権威DNSサーバーを指定するレコードタイプ |
| グローバルリソースの理解 | Q513 | Route 53、IAM はグローバルサービスでリージョン再作成が不要。リージョナルサービスとの区別が重要 |
| VPN CloudHub 構成 | Q88 | VPN CloudHub = 仮想プライベートGW + 複数カスタマーGW + 固有BGP ASN。複数拠点間VPN接続のハブ&スポーク型構成 |
| ELB vs Route 53 の使い分け | 通常Q5 | ELB = インスタンスレベルの負荷分散・高可用性（AZ 間）、Route 53 = DNS レベルのルーティング（リージョン間フェイルオーバー等）。用途を混同しない |

**学習優先度: 最高（正答率 22.2%）**
- [ ] Route 53 の全ルーティングポリシー（シンプル/加重/レイテンシー/フェイルオーバー/地理的/地理近接/複数値）を整理する
- [ ] マルチリージョン高可用性アーキテクチャのパターンを学ぶ
- [ ] ELB の種類と使い分け（ALB=L7, NLB=L4, CLB=旧世代）を整理する
- [ ] Kinesis vs SQS vs SNS のストリーミング/メッセージング使い分けを学ぶ
- [ ] VPN CloudHub のアーキテクチャパターンを理解する
- [ ] AWS グローバルサービス vs リージョナルサービスの一覧を整理する

---

### Domain 3: 高性能アーキテクチャの設計（累計: 2/9 = 22%）

**理解が不十分なトピック:**

| トピック | 間違えた問題 | 具体的な誤解・ギャップ |
| :--- | :--- | :--- |
| CloudFront + Lambda@Edge の認証フロー | Q3 | 認証トークン検証は Lambda@Edge で実装し、キャッシュ制御と組み合わせる |
| Direct Connect + Transit Gateway の構成 | Q26 | 複数 VPC + オンプレミスの一元管理 = Direct Connect + Transit Gateway が正解 |
| Aurora リードレプリカ vs DAX | Q32 | Aurora の読み取りスケールは Aurora リードレプリカが正解。DAX は DynamoDB 専用 |
| Auto Scaling クールダウン期間の計算 | ミニQ3 | クールダウンは最後のスケーリングアクティビティ完了後から起算。複数インスタンス起動時は最後の起動基準 |
| DAX vs ElastiCache の使い分け | ミニQ10 | DynamoDB のキャッシュ = DAX（専用・コード変更最小）。ElastiCache は汎用だがアプリ側実装が必要 |
| マルチリージョン低レイテンシー設計（DynamoDB vs ElastiCache） | Q158 | **再度間違えた**: ユーザー好みデータの永続保存+マルチリージョン = 各リージョンのローカル DynamoDB テーブルが正解。ElastiCache はインメモリで高速だが永続性・マルチリージョン対応で DynamoDB に劣る。Route 53 レイテンシーベースルーティングの有無も要確認 |
| EBS Provisioned IOPS の CloudWatch メトリクス | Q105 | Provisioned IOPS ボリュームの CloudWatch メトリクス送信間隔は1分。汎用SSD等は5分間隔 |
| AWS Storage Gateway の機能理解 | Q56 | Storage Gateway の各タイプ（File/Volume/Tape）の用途と機能を整理する必要あり |
| DB書き込みスループット向上 | Q604 | EBSアレイ（RAID 0等）+ EC2インスタンスサイズ拡大で書き込み性能を向上。RDS では対応できないケースの設計 |
| Oracle SQL Developer の理解 | Q197 | Oracle提供の無料Javaグラフィカルツール。AWS固有サービスではなく一般的なDB管理ツール |
| VPC エンドポイント vs Direct Connect の使い分け | 通常Q9 | VPC エンドポイント = VPC 内から AWS サービスへのプライベート接続（ゲートウェイ型: S3/DynamoDB）。Direct Connect = オンプレミスと AWS 間の専用線接続。用途が異なる |

**学習優先度: 最高（正答率 33.3%）**
- [ ] CloudFront のキャッシュ動作とオリジン設定を学ぶ
- [ ] Direct Connect / VPN / Transit Gateway の使い分けを整理する
- [ ] Aurora のアーキテクチャ（クラスターエンドポイント、リーダーエンドポイント）を学ぶ
- [ ] EBS ボリュームタイプ別の CloudWatch メトリクス間隔を整理する
- [ ] Storage Gateway の全タイプと使い分けを学ぶ
- [ ] EC2 + EBS のパフォーマンスチューニング（RAID構成、インスタンスサイズ）を学ぶ

---

### Domain 4: コストを最適化したアーキテクチャの設計（累計: 2/9 = 22%）

**理解が不十分なトピック:**

| トピック | 間違えた問題 | 具体的な誤解・ギャップ |
| :--- | :--- | :--- |
| Spot インスタンスの活用 | Q24, Q331 | 分散処理・バッチ処理・障害耐性のある分散処理には Spot インスタンスが最もコスト効率が高い。**再度出題**: 障害耐性ありの分散処理コスト最適化 = Spot Instances |
| S3 File Gateway + ライフサイクルポリシー | Q27 | SMB ファイルサーバー拡張 = S3 File Gateway。7日後のアーカイブ = S3 Glacier Deep Archive へのライフサイクル |
| DynamoDB コスト最適化・SQS バッファリング | Q489 | SQS による書き込みバッファリングでスパイクを平準化→WCU 削減。不要テーブル削除でストレージコスト削減。S3 は DynamoDB より大量データ保存に安価 |
| EMR + Redshift コスト最適化 | Q9 | PDF/CSV 保存は S3 RRS（Reduced Redundancy Storage）、EMR は Spot Instances、Redshift は Reserved Instances でコスト最適化 |
| S3 Intelligent-Tiering | Q686 | 予測不可能なアクセスパターンのデータには S3 Intelligent-Tiering が最適。アクセス頻度に応じて自動的にストレージ層を移動 |
| Reserved Instances の上限 | Q409 | Reserved Instances は月20台/AZ（アベイラビリティゾーン）の上限がある。上限緩和申請が可能 |
| S3 Glacier Flexible vs Deep Archive の取得時間 | 通常Q4 | Glacier Flexible Retrieval = 数分〜12時間、Deep Archive = 12〜48時間。取得時間要件に応じたクラス選択が重要 |
| EC2 コスト最適化（低使用率ワークロード） | 通常Q8 | 低使用率の EC2 は Lambda でスケジュール起動停止が最もコスト効率が高い。常時稼働前提の RI ではなく使用時間を減らす発想 |

**学習優先度: 最高（正答率 28.6%）**
- [ ] EC2 購入オプション（オンデマンド/Reserved/Spot/Savings Plans）の使い分けと制限を整理する
- [ ] S3 ストレージクラス全種類（Standard/IA/One Zone-IA/Intelligent-Tiering/Glacier/Glacier Deep Archive/RRS）を学ぶ
- [ ] AWS Storage Gateway の種類（File/Volume/Tape）を整理する
- [ ] EMR + Redshift のコスト最適化パターンを学ぶ
- [ ] Reserved Instances の仕様と制限（上限、スコープ、変更可能性）を整理する

---

### Domain 0: 総合（5/14 = 36%）

**理解が不十分なトピック:**

| トピック | 間違えた問題 | 具体的な誤解・ギャップ |
| :--- | :--- | :--- |
| EC2 購入オプション | Q7 | オンデマンドインスタンスの正確な定義・特徴 |
| 暗号化 EBS ボリュームの仕様 | Q10, Q12 | 暗号化 EBS のスナップショット・コピー時の動作（暗号化が引き継がれる） |
| NAT インスタンスの設定 | Q14 | NAT インスタンスは Source/Destination Check を無効化する必要がある |
| EBS ボリューム情報の確認方法 | Q21 | EC2 コンソールの Volumes セクションで確認する |
| EC2 の IP アドレス割り当て | Q22 | 起動時に割り当てられる2つの IP = プライベート IP + パブリック IP（または Elastic IP） |
| Organizations の SCP | Q19 | Organizations の SCP（サービスコントロールポリシー）でアカウント横断の権限制御 |

---

## 🟢 理解済みポイント（定着している知識）

### 正解した問題から確認できた理解

| トピック | 問題 | 理解の証拠 |
| :--- | :--- | :--- |
| GuardDuty + EventBridge + Lambda の自動対応フロー | Q20 | 脅威検知の自動対応パターンを正しく選択できた |
| Amazon MSK vs Kinesis の使い分け | Q15 | 高可用性・複雑なストリーム処理 = MSK を正しく選択できた |
| SNS トピック作成時の ARN 発行 | Q13 | AWS リソースの ARN 仕組みを理解している |
| EBS スナップショットによるボリューム再作成 | Q33 | EBS のバックアップ・復元フローを理解している |
| EBS の RAID 5/6 非推奨 | Q29 | EBS の RAID 推奨事項を正しく記憶している |
| AMI の作成・購入方法 | Q4 | AMI の入手方法（自作・Marketplace）を理解している |
| EFS + ライフサイクルポリシー（IA） | ミニQ4 | NFS 移行 + コスト最適化 = EFS + IA ストレージクラスへの自動移行を正しく選択 |
| Organizations 組織トレイル | ミニQ5 | マルチアカウント CloudTrail ログ集約 = 組織トレイルが最適解を正しく選択 |
| DR 戦略の選定（ウォームスタンバイ） | ミニQ8 | RTO 1-2h / RPO 15min + コスト考慮 = ウォームスタンバイを正しく選択 |
| SQS FIFO キュー | ミニQ9 | メッセージ順序保証 + Exactly-once + 重複排除 = SQS FIFO を正しく選択 |
| S3 + CloudFront + ACM 構成 | ミニQ11 | 静的サイトのグローバル配信 + HTTPS + 低コスト = S3+CloudFront+ACM を正しく選択 |
| EC2 ルートデバイス名 | Q20 | /dev/sda1 はルートデバイスとして予約されている。データボリュームには /dev/sd[b-z] を使用 |
| Placement Groups で低レイテンシー | Q628 | 低レイテンシーのインスタンス間通信には Placement Groups（クラスター配置グループ）が有効 |
| Reserved Instances 前払い金は返金不可 | Q238 | RI の前払い金は途中解約しても返金されない。Marketplace での売却は可能 |
| RDS Multi-AZ の用途 | Q627 | 複雑なクエリ処理 + 高可用性が必要な場合は RDS Multi-AZ が最適 |
| Route 53 アクティブ-アクティブフェイルオーバー | Q433 | 複数リソースへの同時トラフィック分散 + フェイルオーバー = アクティブ-アクティブ構成 |
| User data によるカスタムスクリプト | Q142 | EC2 起動時にカスタムスクリプトを実行するには User data を使用 |
| EBS は複数EC2に同時アタッチ不可 | Q607 | EBS ボリュームは基本的に1つの EC2 インスタンスにのみアタッチ可能（io1/io2 の Multi-Attach は例外） |
| RDS リードレプリカの活用 | 通常Q6 | 読み取り負荷の分散に RDS リードレプリカを正しく選択できた |
| SSE-KMS による暗号化 | 通常Q7 | SSE-KMS を使った S3 暗号化の仕組みを正しく理解している |
| マルチリージョン + Route 53 フェイルオーバー | 通常Q10 | マルチリージョン構成での耐障害性確保に Route 53 フェイルオーバーを正しく選択できた |

---

## 📌 次回試験に向けた優先学習リスト

以下を優先的に学習すること（正答率が低いドメインから順に）:

1. **Domain 1（10.0%・最低）**: セキュリティグループ（デフォルトSG vs ユーザー作成SG）、Systems Manager（Run Command, Patch Manager）、VPCセキュリティ設計（IDS/IPS, Bastion Host）、EC2テナンシー、S3権限管理
2. **Domain 2（22.2%）**: ELB種類別使い分け（ALB/NLB）、Kinesis vs SQS vs SNS、VPN CloudHub、グローバルサービス vs リージョナルサービス、RDS Multi-AZ フェイルオーバー
3. **Domain 4（28.6%）**: EC2購入オプション（Spot/RI上限）、S3ストレージクラス全種類（Intelligent-Tiering含む）、EMR+Redshiftコスト最適化
4. **Domain 3（33.3%）**: EBSボリュームタイプ別CloudWatchメトリクス、Storage Gateway全タイプ、EC2+EBSパフォーマンスチューニング

---

## 🔄 更新履歴

| 日付 | 更新内容 |
| :--- | :--- |
| 2026-03-22 | 初回試験（33問）の結果を記録。正答率 24.2% |
| 2026-03-22 | ミニ模擬試験（9問採点）の結果を記録。正答率 55.6%（+31.4pt改善） |
| 2026-03-22 | 弱点復習 5問中3問正解。Q688/Q520/miniQ3 を克服。miniQ6(Shield vs WAF)・miniQ7(S3暗号化) は再度間違い → 最優先弱点に格上げ |
| 2026-03-23 | Q146(S3保存データ暗号化) 不正解。S3暗号化方式の弱点が継続（3回目）。「保存データ vs 転送中」の区別、SSE-C の存在を再確認 |
| 2026-03-23 | Q158(マルチリージョン低レイテンシー設計) 不正解。DynamoDB vs ElastiCache の使い分け弱点が継続。永続データ+マルチリージョン = DynamoDB ローカルテーブル |
| 2026-03-23 | ミニ模擬試験（11問）の結果を記録。正答率 45.5%（前回比 +21.3%）。Domain 3 が 66.7% と最も改善。Domain 1・2 は 33.3% で引き続き要強化 |
| 2026-03-23 | フル模擬試験途中終了（32問）の結果を記録。正答率 21.9%（7/32）。全ドメインで大幅な弱点が判明。Domain 1: 10.0%、Domain 2: 22.2%、Domain 3: 33.3%、Domain 4: 28.6%。25問の新規弱点トピックを追加、7問の理解済みトピックを確認 |
| 2026-03-23 | 通常モード（10問・7問記録）の結果を記録。正答率 43%（3/7）。新規弱点4件追加（S3 Glacier取得時間、ELB vs Route 53、Lambda スケジュール停止、VPCエンドポイント vs Direct Connect）。理解済み3件追加（RDSリードレプリカ、SSE-KMS、マルチリージョン耐障害性） |
