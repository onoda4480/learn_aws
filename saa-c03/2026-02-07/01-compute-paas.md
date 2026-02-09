# コンピュート・PaaS

## AWS Elastic Beanstalk

アプリケーションをアップロードするだけで、インフラを**自動構築・管理**してくれるPaaSサービス

### 仕組み

```
コードをアップロード
      │
      ▼
Elastic Beanstalk が自動で構築
      │
      ├─→ EC2（アプリサーバー）
      ├─→ ALB（ロードバランサー）
      ├─→ Auto Scaling（自動スケール）
      ├─→ セキュリティグループ
      └─→ CloudWatch（監視）
```

### 特徴

| 項目 | 内容 |
|------|------|
| 対応言語 | Java, Python, Node.js, Ruby, Go, .NET, PHP, Docker |
| 料金 | Beanstalk自体は無料（EC2等のリソース代のみ） |

### 比較

```
EC2        = 全部自分で構築・管理（IaaS）
Beanstalk  = コードだけ渡せばOK（PaaS）
Lambda     = 関数単位で実行（FaaS/サーバーレス）
```

### 試験ポイント

```
「コードをアップロードするだけ」「インフラ自動構築」→ Elastic Beanstalk
```
