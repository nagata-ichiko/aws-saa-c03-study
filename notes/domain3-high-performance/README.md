# 第3分野: 高性能アーキテクチャの設計 (24%)

ストレージ・コンピューティング・データベース・ネットワーキングのパフォーマンス最適化が問われる分野です（24%）。

## 📋 タスクステートメント

### 3.1 高性能かつスケーラブルなストレージソリューションの決定
- **ストレージサービスとユースケース**: Amazon S3, Amazon EFS, Amazon EBS
- **ストレージタイプ**: オブジェクトストレージ, ファイルストレージ, ブロックストレージ
- **ハイブリッドストレージ**: AWS Storage Gateway, AWS DataSync

### 3.2 高性能かつ弾力性に優れたコンピューティングソリューションの設計
- **コンピューティングサービス**: Amazon EC2, AWS Lambda, AWS Fargate, AWS Batch, Amazon EMR
- **スケーラビリティ機能**: Amazon EC2 Auto Scaling
- **インスタンスタイプとサイズ**: 汎用, コンピューティング最適化, メモリ最適化, ストレージ最適化

### 3.3 高性能なデータベースソリューションの決定
- **データベースタイプ**: リレーショナル (RDS, Aurora), 非リレーショナル (DynamoDB), インメモリ (ElastiCache)
- **キャパシティプランニング**: プロビジョンド IOPS, DynamoDB のキャパシティユニット (RCU/WCU)
- **データベースのレプリケーション**: リードレプリカ (Read Replica)
- **キャッシュ戦略**: Amazon ElastiCache (Redis, Memcached), DynamoDB DAX

### 3.4 高性能かつスケーラブルなネットワークアーキテクチャの決定
- **エッジネットワーキング**: Amazon CloudFront, AWS Global Accelerator
- **ネットワーク接続オプション**: AWS Direct Connect, AWS VPN, AWS PrivateLink
- **ロードバランシング**: ALB (レイヤー7), NLB (レイヤー4 - 超高性能)

### 3.5 高性能なデータ取り込みおよび変換ソリューションの決定
- **ストリーミングデータ**: Amazon Kinesis (Data Streams, Data Firehose)
- **データ分析と可視化**: Amazon Athena, AWS Lake Formation, Amazon QuickSight
- **データ変換**: AWS Glue

## 🔑 重要サービス一覧

| カテゴリ | サービス | 重要度 |
| :--- | :--- | :--- |
| ストレージ | EBS (gp3/io2), S3, EFS, FSx for Lustre | ⭐⭐⭐ |
| コンピューティング | EC2 (インスタンスタイプ), Lambda, Fargate | ⭐⭐⭐ |
| データベース | ElastiCache (Redis/Memcached), DynamoDB DAX, Aurora | ⭐⭐⭐ |
| CDN・ネットワーク | CloudFront, Global Accelerator, Direct Connect | ⭐⭐⭐ |
| データ処理 | Kinesis Data Streams, Kinesis Data Firehose, EMR, Glue | ⭐⭐ |

## 📝 学習ノート

### ストレージパフォーマンスの選択

**EBS ボリュームタイプ比較**

| タイプ | 最大 IOPS | 最大スループット | ユースケース |
| :--- | :--- | :--- | :--- |
| gp3 (汎用 SSD) | 16,000 | 1,000 MB/s | 一般的なワークロード |
| io2 Block Express | 256,000 | 4,000 MB/s | 高 IOPS が必要な DB |
| st1 (スループット HDD) | 500 | 500 MB/s | ビッグデータ・ログ処理 |
| sc1 (コールド HDD) | 250 | 250 MB/s | アクセス頻度の低いデータ |

### キャッシュ戦略

**ElastiCache** は、データベースの読み取り負荷を軽減するキャッシュレイヤーです。

| 項目 | Redis | Memcached |
| :--- | :--- | :--- |
| データ構造 | 豊富（リスト、セット、ソート済みセットなど） | シンプル（文字列のみ） |
| 永続化 | あり | なし |
| レプリケーション | あり（Multi-AZ 対応） | なし |
| ユースケース | セッション管理、リアルタイムランキング | シンプルなキャッシュ |

### DAX vs ElastiCache — インメモリキャッシュの使い分け

どちらも「インメモリキャッシュ」だが、用途が全く異なる。

| | DAX | ElastiCache |
| :--- | :--- | :--- |
| 何のキャッシュ？ | **DynamoDB 専用** | **汎用**（どの DB でも使える） |
| API 互換 | DynamoDB API と互換 | 独自 API（Redis/Memcached） |
| コード変更 | ほぼ不要（エンドポイント変更だけ） | キャッシュロジックを自前実装 |
| レイテンシー | マイクロ秒 | ミリ秒 |
| 対応 DB | DynamoDB のみ | RDS, Aurora, DynamoDB, 何でも |
| 運用負荷 | 低い | 高い（キャッシュ戦略の設計が必要） |

**試験での判断フローチャート:**
- 「DynamoDB の読み取りを高速化」→ DAX（一択！）
- 「RDS / Aurora の読み取りを高速化」→ ElastiCache
- 「セッション管理 / リアルタイムランキング」→ ElastiCache (Redis)
- 「シンプルなキーバリューキャッシュ」→ ElastiCache (Memcached)

**鉄則: DynamoDB + キャッシュ = DAX。それ以外 = ElastiCache。**

### エッジネットワーキングによるパフォーマンス向上

- **Amazon CloudFront**: 静的および動的コンテンツをエッジロケーションから配信する CDN。レイテンシーを低減。
- **AWS Global Accelerator**: AWS のグローバルネットワークを使用して、ユーザーからアプリケーションへのトラフィックのパフォーマンスを最大 60% 向上させる。IP アドレスを固定（Anycast IP）できる。

---

*このファイルは AI エージェントによって随時更新されます。*
