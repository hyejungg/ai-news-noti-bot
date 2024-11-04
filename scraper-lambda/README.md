# scraper-lambda

## 동작
url, content_type, selector를 받아 해당 url의 데이터에서
html인 경우 전체 내용 또는 selector에 해당하는 데이터를 추출하여 반환
json인 경우에는 해당 데이터 자체를 반환

**body**


| 필드           | 설명            | 필수여부 | 타입  | 값          |
|--------------|---------------|------|-----|------------|
| url          | 요청 URL        | 필수   | str |            |
| content_type | 컨텐츠 유형        | 선택   | str | html, json |
| selector     | html selector | 선택   | str |            |

Example
```json
{
    "url": "https://www.naver.com",
    "content_type": "html",
    "selector": "div"
}
```

## 배포
1. sam build 실행 (이미지 빌드 및 배포용 template.yaml 파일 생성)
    ```bash
    sam build
    ```

2. 변경된 stack 배포
    ```bash
    sam deploy
    ```
   - 자세한 로그가 필요한 경우 --debug 추가
        ```bash
        sam deploy --debug
        ```
   - 아래와 같이 ROLLBACK 관련해서 state 변경할 수 없다고 표시되는 경우 cloudfront 콘솔에서 stack 삭제 후 재배포
     
     [참고](https://repost.aws/questions/QUjl_fJ_-bQEW-_a-i6qCVog/rollback-complete-state-and-can-not-be-updated)
     ```aiignore
      An error occurred (ValidationError) when calling the CreateChangeSet operation: Stack:arn:aws:cloudformation:ap-northeast-2:339712918956:stack/scraper-lambda/3277bad0-9a85-11ef-81d5-069f4e3fe3e7 is in ROLLBACK_COMPLETE state and can not be updated.
     ```