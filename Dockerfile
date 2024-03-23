# AWS Lambda의 Node.js 18 베이스 이미지 사용
FROM public.ecr.aws/lambda/nodejs:18

WORKDIR /home/app

RUN npm install -g pnpm

# 모노레포 구조와 관련된 파일들 복f사
COPY pnpm-workspace.yaml ./
COPY package.json ./
COPY pnpm-lock.yaml ./

# common 모듈과 news-scrapper 함수의 코드와 package.json 복사
COPY common ./common
COPY lambdas/news-scraper ./lambdas/news-scraper

# 의존성 설치를 위한 작업 디렉토리로 변경
WORKDIR /home/app/lambdas/news-scraper

RUN pnpm install

WORKDIR /home/app/lambdas/news-scraper/dist

CMD ["node", "index.js"]
