# 자동배포 구성 전 테스트용 스크립트
# npm script를 통한 실행을 기준으로 작성

# 람다 실행
# 실행 전 인증관련 환경변수 설정 필요 (https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/cli-configure-envvars.html)

aws lambda invoke \
 --function-name aws-news-noti-bot-test \
 --log-type Tail \
 --query 'LogResult' \
 --output json \
 --payload '{}' /dev/stdout | awk -F '"' '{print $2}' | base64 --decode
