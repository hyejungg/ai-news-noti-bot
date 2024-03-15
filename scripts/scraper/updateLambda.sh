# 자동배포 구성 전 테스트용 스크립트
# npm script를 통한 실행을 기준으로 작성

# zip파일 생성
npm run build

cp ./.env ./dist
cp ./package.json ./dist
cp ./package-lock.json ./dist
cd ./dist
npm install --production

zip -r ./ai-news-noti-bot.zip ./

# AWS Lambda에 배포
# 실행 전 인증관련 환경변수 설정 필요 (https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/cli-configure-envvars.html)
aws lambda update-function-code \
 --function-name aws-news-noti-bot-test \
 --zip-file fileb://ai-news-noti-bot.zip
