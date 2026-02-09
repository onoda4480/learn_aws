# マネジメント

## AWS Systems Manager Automation

AWSリソースの運用タスクを**自動化**する機能

### Runbook（ランブック）

自動化の手順書（ドキュメント）

```
Runbook の中身：
  Step 1: EC2を停止
  Step 2: スナップショット作成
  Step 3: EC2を起動
  Step 4: 結果を通知
```

### 主なユースケース

| タスク | 説明 |
|--------|------|
| AMI作成 | EC2を停止→AMI作成→起動を自動化 |
| パッチ適用 | 複数EC2に一斉パッチ |
| インスタンス再起動 | 障害時の自動復旧 |

### 他サービスとの違い

| サービス | 用途 |
|---------|------|
| **Automation** | AWSリソースの運用自動化 |
| Run Command | EC2内でコマンド実行 |
| Step Functions | アプリケーションのワークフロー |

### 試験ポイント

```
「運用タスクの自動化」「Runbook」→ Systems Manager Automation
「EC2内でコマンド実行」→ Run Command
```
