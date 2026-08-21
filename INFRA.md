# 인프라 스택 관리

메인 스택(`template.yaml`, GitHub Actions 자동 배포)과 별개로 관리하는 인프라 리소스에 대한 문서입니다.

## 스택 구성

| 스택 이름 | 템플릿 | 관리 리소스 |
|---|---|---|
| `ai-news-agent-ecr-dev` | `2026-08-21-template.yaml` (`PROFILE=dev`) | ECR 리포지토리 2개, SAM 아티팩트 S3 버킷 |
| `ai-news-agent-ecr-prod` | `2026-08-21-template.yaml` (`PROFILE=prod`) | ECR 리포지토리 2개, SAM 아티팩트 S3 버킷 |

> 스택 이름의 `-ecr` 은 처음 ECR만 담고 있던 시절의 흔적입니다. 스택 이름 변경은 리소스 재편입이 필요해서 그대로 둡니다.

### 리소스 상세
- **ECR 리포지토리** (`ai-news-agent/news-scraper-agent-<phase>`, `ai-news-agent/scraper-lambda-<phase>`)
  - 라이프사이클 정책: 최신 2개 이미지만 유지(현재 사용 중 + 롤백용), 나머지는 자동 만료 (만료는 24시간 이내 비동기 처리)
  - Lambda가 함수 생성 시 자동으로 붙이는 이미지 pull 정책(`LambdaECRImageRetrievalPolicy`)을 템플릿에 명시 — 템플릿에서 빠지면 CloudFormation이 실제 정책을 삭제하려고 하므로 **지우면 안 됨**
- **SAM 아티팩트 버킷** (`ai-news-agent-sam-artifacts-<phase>-339712918956`)
  - `sam deploy` 가 템플릿을 업로드하는 버킷. 계정 공용 SAM 버킷(`aws-sam-cli-managed-default-*`) 대신 사용
  - 객체 30일 만료 + 미완료 멀티파트 업로드 7일 후 정리

## 템플릿 파일 규칙
- 파일명은 **마지막으로 변경한 날짜**를 따릅니다: `YYYY-MM-DD-template.yaml`
- 내용을 변경할 때는:
  1. `git mv` 로 파일명을 변경한 날짜로 갱신
  2. 파일 상단 독스트링에 수행 내역 한 줄 추가
  3. 이 문서의 변경 이력 표에 행 추가
  4. 파일명을 참조하는 곳 갱신: `samconfig.toml` (`template_file`), `README.md`
- 모든 리소스에 `DeletionPolicy: Retain` 을 유지합니다 (스택 삭제/교체 사고에서 실제 리소스 보호)

## 배포 방법
템플릿 수정 후 phase별로 실행합니다 (자주 바뀌지 않아 CI에 넣지 않음):

```bash
aws cloudformation deploy --region ap-northeast-2 --template-file 2026-08-21-template.yaml \
  --stack-name ai-news-agent-ecr-<phase> --parameter-overrides PROFILE=<phase> --no-fail-on-empty-changeset
```

- `<phase>`: `dev` 또는 `prod`
- `sam deploy --config-env <phase>-ecr` 도 가능하지만, S3 업로드를 거치기 때문에 계정 권한에 따라 실패할 수 있습니다. 템플릿이 작아 S3가 필요 없는 위 명령을 권장합니다.

## 변경 이력

| 날짜 | 내용 |
|---|---|
| 2026-08-21 | 기존 ECR 리포지토리 4개를 스택으로 편입(import), 라이프사이클 정책(최신 2개 유지) 적용. SAM 아티팩트 버킷(30일 만료) 추가, 메인 스택이 공용 SAM 버킷 대신 이 버킷을 쓰도록 `samconfig.toml` 변경 |

## 1회성 작업 기록 (재실행 불필요)

### 2026-08-21: 기존 ECR 리포지토리 스택 편입
콘솔에서 수동 생성했던 리포지토리를 CloudFormation IMPORT changeset으로 편입했습니다. 요지:

```bash
aws cloudformation create-change-set \
  --stack-name ai-news-agent-ecr-<phase> --change-set-name import-ecr-repositories \
  --change-set-type IMPORT \
  --template-body file://<최소 템플릿> \
  --parameters ParameterKey=PROFILE,ParameterValue=<phase> \
  --resources-to-import '[{"ResourceType":"AWS::ECR::Repository","LogicalResourceId":"...","ResourceIdentifier":{"RepositoryName":"..."}}, ...]'
aws cloudformation execute-change-set --stack-name ... --change-set-name import-ecr-repositories
```

### 2026-08-21: IAM 변경
- `AI_NEWS_NOTI_BOT_LAMBDA` 정책(v16)에 추가: CloudFormation ECR 핸들러용 권한(`ecr:TagResource`, `ecr:PutLifecyclePolicy` 등, `ai-news-agent/*` 한정) + `s3:PutObject`
