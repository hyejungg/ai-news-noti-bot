# news-scraper-agent
- python, lanchain 을 이용하여 뉴스 사이트를 크롤링 하고, 키워드에 맞는 기사제목과 링크를 추출하는 agent 구성

## required
- python 3.12.2

## 실행 방법
```shell
poetry shell
poetry install
python {파일명}.py
```

## memo
- 현재는 langsmith 로 연결해두었는데 .. 만약에 이게 사내망에서 서비스 하는 걸로 변경된다면 langfuse 써보기!
- 의존성 내보내기
  - -f, --format: 내보낼 파일의 형식을 지정합니다. 현재는 requirements.txt 형식만 지원합니다.
  - --output, -o: 내보낸 의존성 목록을 저장할 파일의 경로를 지정합니다. 지정하지 않으면 표준 출력으로 결과가 나타납니다.
  - --without-hashes: 이 옵션을 사용하면, 의존성 목록에서 해시값을 제외할 수 있습니다. 일부 환경이나 도구에서는 해시값이 문제를 일으킬 수 있기 때문에 유용할 수 있습니다.
  - --dev: 이 옵션을 사용하면, 개발용 의존성도 포함하여 내보냅니다.
  - --with, --without: 특정 의존성 그룹을 포함하거나 제외할 때 사용합니다.
```shell
poetry export -f requirements.txt --output requirements.txt
```
- 프로젝트 빌드 및 배포
  - 이 명령어는 wheel과 source archive를 생성
  - PyPI에 배포하려면 먼저 PyPI 계정이 있어야 하며, 다음과 같이 배포 가능
```shell
poetry build
poetry publish
```
