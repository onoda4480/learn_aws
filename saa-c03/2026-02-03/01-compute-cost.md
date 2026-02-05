# コンピューティング・コスト最適化

## Compute Savings Plans vs Reserved Instances

### Compute Savings Plans
- 1年 or 3年の「金額コミット」で最大66%割引
- EC2, Fargate, Lambda に適用
- リージョン変更、インスタンスタイプ変更しても割引継続
- 柔軟性が高い（サブスク型）

### Reserved Instances
- サービスごとに個別契約（EC2用、RDS用など）
- 最大72%割引
- インスタンスタイプ・リージョンが固定
- 変更すると割引が効かなくなる

### 違い
```
Reserved Instances = 個別契約（単品購入）
  → 特定のインスタンスを予約（席を確保）
  → 変更できない代わりに割引率が高い

Savings Plans = まとめて契約（サブスク）
  → 使用金額をコミット（金額を約束）
  → 何に使っても割引

迷ったら Savings Plans の方が安全
```

---

## IaaS / PaaS / SaaS

```
IaaS = インフラを借りる（サーバー、ネットワーク）
PaaS = 開発環境を借りる（インフラ+ミドルウェア）
SaaS = ソフトウェアを借りる（完成品をそのまま使う）
```

### 自分で管理する範囲
```
            │ 自分で管理 │ AWSが管理 │
────────────┼───────────┼──────────┤
IaaS        │ OS〜アプリ │ ハードウェア│
PaaS        │ アプリのみ │ OS〜ミドル │
SaaS        │ 設定のみ  │ 全部      │
```

### 具体例

| 分類 | AWSサービス | 他社サービス |
|-----|-----------|------------|
| IaaS | EC2, VPC, EBS, S3 | Azure VM, GCE |
| PaaS | Elastic Beanstalk, Lambda, RDS, App Runner | Heroku, Vercel |
| SaaS | WorkSpaces, Chime, QuickSight | Gmail, Slack, Zoom |

---

## AMI（Amazon Machine Image）

EC2インスタンスを作るための「テンプレート」

- OS + 設定 + ソフトウェア をまるごとパッケージ化
- 同じ環境を何台でも複製できる
- AWS提供のもの or 自分で作ったカスタムAMI を使う

```
カスタムAMIの活用：
1. 1台セットアップ（nginx, Node.js等をインストール）
2. そこからAMI作成
3. 次からはそのAMIで起動するだけ（全部入りで起動）
```
