# LangGraph 기반의 AI 뉴스 트렌드 알림 봇 (v2)
 
AI 뉴스 트렌드 알림 봇은 회사 내 GAI(Generative AI) 스터디원들에게 최신 AI 뉴스들을 매일 오전 10시에 전달 하기 위해 제작 됐어요!
특정 사이트에 대한 뉴스 기사 중 GAI, AI와 관련된 뉴스들만 필터링 합니다. 
현재 크롤링 중인 사이트는 '긱뉴스', '데보션', 'AI 타임즈'이고, 사이트 추가는 누구든 [링크](https://d1qbk7p5aewspc.cloudfront.net/index.html)에서 자유롭게 가능합니다.

> 📍 v1은 [여기](https://github.com/hyejungg/ai-news-noti-bot/releases/tag/1.0.0-archive)에서 볼 수 있습니다.

###  v1 에서 v2로 개선한 이유
- 기존 방식은 DB에 저장되어 있는 각 사이트별 keyword를 기준으로 기사 제목에서 동일한 값이 있는 뉴스들만 필터링
- 이로 인해 **원하지 않은 뉴스도 알림 메시지에 포함**되는 문제가 존재 
  - (ex. '왜 통신사 직원이 중학교 교실 찾아 AI를 가르칠까')
- **LLM을 이용하여 크롤링, 필터링, 정렬을 개선**하기 위해 **전체적인 구조**를 변경
  - 동적으로 변경되는 html에 대한 파싱 대응을 위해 크롤링 과정도 LLM을 통해 진행 

## 📂 modules
### news-scraper-agent
> LLM 관련 뉴스 정보 필터링/정렬 + 알림 python 봇

### scraper-lambda
> 뉴스 스크래핑을 위한 람다

## 📈 flow chart
- news-scraper-agent는 뉴스봇 실행부터 각 에이전트를 돌며 파싱, 크롤링, 필터링, 정렬 하는 과정을 거친 후 카카오워크 메시지로 매주 10시에 알람을 보내줍니다.
<img width="453" alt="Image" src="https://github.com/user-attachments/assets/1f1a1d17-865f-4972-9be4-dc104d9923d2" />

## 🛠️architecture
- news-scraper-agent와 scraper-lambda는 AWS 리소스로 이루어져 있습니다.
- aws sam (serverless application model)을 이용하여 로컬 환경에서 람다 디버깅 편의성을 높이고, cloudFormation 기반으로 뉴스봇에 사용하는 모든 리소스를 stack 형태로 관리하고 있습니다.
![Image](https://github.com/user-attachments/assets/af96cb0a-fcbc-4a61-8108-d328497f900a)

## 🔥result
![Image](https://github.com/user-attachments/assets/a6a4a2c7-3520-4331-8160-44ed5ce3832d)
![Image](https://github.com/user-attachments/assets/d1fb5f52-f06a-41ff-ab71-702d7998212b)

## 🔖 convention

## 🔥schedule management
> [여기](https://github.com/hyejungg/ai-news-noti-bot/issues/10)에서 전체 일정(v1, v2) 관리 내용을 볼 수 있습니다.

- v1 개발 기간: 2024.03.12 ~ 2024.03.25 (13d)
- v2 개발 기간: 2024.11.04 ~ 2024.12.05 (32d)

### ⚡ git
**1.  branch**
```
-------- main --------
    \
      -------- develop --------
      \
        --------feat/#3------
      \
        --------feat/#4------
```

-   PR이 Merge되면 해당 브랜치는 삭제한다.
-   branch 이름 : **tag/#issue_number** (ex. feat/#3)
-   tag
    -   feat : 새로운 기능 추가
    -   fix : 자잘한 수정
    -   refactor : 코드 리팩토링 시에만 사용
    -   chore : config 및 라이브러리, 빌드 관련 파일 수정
    -   rename : 파일명, 변수명 수정
    -   docs : 문서 수정
    -   comment :주석 추가 및 수정

**2. commit message**
-   별도의 규칙 없음
