# AWS SAA-C03 学習メモ（2026-02-02）

## Compute Savings Plans / Reserved Instances

### Compute Savings Plans
- 1年 or 3年の「金額コミット」で最大66%割引
- EC2, Fargate, Lambda に適用
- リージョン変更、インスタンスタイプ変更しても割引継続
- 柔軟性が高い

### Reserved Instances
- サービスごとに個別契約（EC2用、RDS用など）
- 最大72%割引
- インスタンスタイプ・リージョンが固定
- 変更すると割引が効かなくなる

### 違い
```
Reserved Instances = 個別契約（単品購入）
Savings Plans     = まとめて契約（サブスク）

迷ったら Savings Plans の方が安全
```

---

## AWS KMS（Key Management Service）

- 暗号化キーを安全に作成・保管・管理するサービス
- S3, EBS, RDS など多くのサービスと連携
- 鍵のローテーション、アクセス制御、監査ログに対応

### S3マネージドキー / KMS / Secrets Manager の違い

| サービス | 役割 | 保管するもの |
|---------|------|------------|
| S3マネージドキー（SSE-S3） | S3専用の暗号化方式 | - |
| KMS | 暗号化キーの管理 | 暗号化キー |
| Secrets Manager | 秘密情報の保管庫 | パスワード、APIキー等 |

#### 使い分け
- **SSE-S3**：とりあえず暗号化、コスト不要、監査不要な時
- **KMS**：監査・権限制御・コンプライアンス対応
- **Secrets Manager**：パスワード・APIキーの安全な保管・自動ローテーション

※ Secrets Manager は内部で KMS を使っている

---

## IaaS / PaaS / SaaS

```
IaaS = インフラを借りる（サーバー、ネットワーク）
PaaS = 開発環境を借りる（インフラ+ミドルウェア）
SaaS = ソフトウェアを借りる（完成品をそのまま使う）
```

### 具体例

| 分類 | AWSサービス | 他社サービス |
|-----|-----------|------------|
| IaaS | EC2, VPC, EBS, S3 | Azure VM, GCE |
| PaaS | Elastic Beanstalk, Lambda, RDS, App Runner | Heroku, Vercel |
| SaaS | WorkSpaces, Chime, QuickSight | Gmail, Slack, Zoom |

---

## ネットワーク構成（ALB / NATゲートウェイ）

### 一般的な通信構成

```
入ってくる通信（ユーザー → アプリ）
  インターネット → IGW → ALB → プライベートサブネット

出ていく通信（アプリ → 外部）
  プライベートサブネット → NAT GW → IGW → インターネット
```

### ALB（Application Load Balancer）
- Webリクエストを複数サーバーに振り分ける
- HTTP/HTTPS 向け（L7）
- ヘルスチェック、SSL終端、パスベースルーティング

### NATゲートウェイ
- プライベートサブネットからインターネットへの「出る専用の門」
- 外からの通信は不可

### ロードバランサーの種類

| 種類 | 用途 | レイヤー |
|-----|------|---------|
| ALB | Webアプリ（HTTP/HTTPS） | L7 |
| NLB | 高速・大量接続（TCP/UDP） | L4 |

---

## ストレージサービス

### EFS（Elastic File System）
- 複数のサーバーから同時にアクセスできる共有ストレージ
- NFS プロトコルで通信
- フォルダのように使える

### EBS vs EFS vs S3

| 項目 | EBS | EFS | S3 |
|-----|-----|-----|-----|
| 共有 | 1台のみ | 複数台OK | 複数台OK |
| 使い方 | HDDとして | フォルダとして | API経由 |
| 直接編集 | できる | できる | できない |
| 料金 | 安い | やや高い | 最安 |
| 用途 | DBなど | 共有ファイル | 画像、バックアップ |

### NFS（Network File System）
- ネットワーク経由でファイルを共有するプロトコル（規格）
- EFS は NFS を使って通信している

---

## AWS Storage Gateway

オンプレミスとAWSストレージを繋ぐサービス

### 3つのゲートウェイタイプ

| タイプ | 見え方 | 保存先 | 主な用途 |
|-------|-------|-------|---------|
| File Gateway | ファイル共有 | S3 | ファイルサーバー |
| Volume Gateway | HDD | S3/EBS | ディスクバックアップ |
| Tape Gateway | テープ | Glacier | テープ置き換え |

### Tape Gateway
- 物理テープを仮想テープ（クラウドのデータ）に置き換える
- バックアップソフトからは物理テープに見える
- 実際は S3 / Glacier に保存
- 物理テープの購入・保管・輸送が不要に
- CD/DVD は対象外（磁気テープ専用）

---

## Amazon FSx for Lustre

- 超高速ファイルシステム（EFSの高速版）
- スループット：数百GB/s
- 用途：機械学習、動画レンダリング、シミュレーション
- S3と連携（普段はS3に保存、処理時だけFSxにロード）

### FSx シリーズ
- FSx for Lustre → 超高速処理向け
- FSx for Windows → Windows ファイル共有
- FSx for NetApp → NetApp 機能が必要な時
- FSx for OpenZFS → ZFS が必要な時

---

## 階層型ストレージ

アクセス頻度でデータを仕分けし、適切な場所に保存する仕組み

```
よく使う     → 高速・高い（S3 Standard）
たまに使う   → 中間（S3 Standard-IA）
ほぼ使わない → 低速・安い（S3 Glacier）
年1回以下   → 最安（S3 Glacier Deep Archive）
```

### S3 Intelligent-Tiering
- アクセスパターンを監視して自動で階層を移動
- 手動管理不要

---

## RDS マルチAZ配置 vs マルチAZ DBクラスター配置

| 項目 | マルチAZ配置 | マルチAZ DBクラスター |
|-----|------------|-------------------|
| 構成 | プライマリ + スタンバイ1台 | ライター1台 + リーダー2台 |
| スタンバイの利用 | 使えない（待機のみ） | 読み取りに使える |
| フェイルオーバー | 60〜120秒 | 約35秒 |
| AZ数 | 2つ | 3つ |
| 読み取り負荷分散 | できない | できる |

### 選び方
- **マルチAZ配置**：シンプルに冗長化、コスト抑えたい
- **マルチAZ DBクラスター**：高速フェイルオーバー、読み取り分散が必要
