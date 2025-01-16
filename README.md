# ai-news-noti-bot

AI 트렌드 알림 봇

## modules
### news-scraper-agent
> 뉴스 스크래핑 + 알림 python 봇

## git convention

### branch
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

### commit
-   별도의 규칙 없음
