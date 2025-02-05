# news-scraper-agent
- python, lanchain 을 이용하여 뉴스 사이트를 크롤링 하고, 키워드에 맞는 기사제목과 링크를 추출하는 agent 구성

## required
- python 3.12.2
- poetry 2.0.1

## 실행 방법
```shell
poetry env activate
poetry install
python {파일명}.py
```

## 배포 방법
```shell
# 로컬에서 실행 방법 
sam local invoke --config-env {phase} {이미지 이름}


# 빌드 후 배포
sam build --config-env {phase}
sam deploy --config-env {phase}
```

## memo
- 의존성 내보내기
  - -f, --format: 내보낼 파일의 형식을 지정합니다. 현재는 requirements.txt 형식만 지원합니다.
  - --output, -o: 내보낸 의존성 목록을 저장할 파일의 경로를 지정합니다. 지정하지 않으면 표준 출력으로 결과가 나타납니다.
  - --without-hashes: 이 옵션을 사용하면, 의존성 목록에서 해시값을 제외할 수 있습니다. 일부 환경이나 도구에서는 해시값이 문제를 일으킬 수 있기 때문에 유용할 수 있습니다.
  - --dev: 이 옵션을 사용하면, 개발용 의존성도 포함하여 내보냅니다.
  - --with, --without: 특정 의존성 그룹을 포함하거나 제외할 때 사용합니다.
```shell
poetry export -f requirements.txt --output requirements.txt
```
