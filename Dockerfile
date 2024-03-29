# AWS Lambda의 Node.js 18 베이스 이미지 사용
FROM public.ecr.aws/lambda/nodejs:18

# pnpm 설치
RUN npm install -g typescript
RUN npm install -g pnpm

# 전체 파일 복사
COPY . ${LAMBDA_TASK_ROOT}

# 디렉터리 위치 이동
WORKDIR ${LAMBDA_TASK_ROOT}

RUN pnpm install

# 의존성 설치를 위한 작업 디렉토리로 변경
WORKDIR ./lambdas/news-scraper

# 실행 환경 구성
RUN pnpm build \
    && cp ../../pnpm-workspace.yaml ./dist \
    && cp ./package.json ./dist/lambdas/news-scraper \
    && cp ../../common/package.json ./dist/common \
    && cd ./dist \
    && pnpm install \
    && cp ../../../common/.env ./common/.env \
    && echo "import { handler as test } from './lambdas/news-scraper/src/index.js'" > index.mjs \
    && echo "export const handler = test;" >> index.mjs

WORKDIR ${LAMBDA_TASK_ROOT}
#COPY /home/app/lambdas/news-scraper/dist ./

CMD ["lambdas/news-scraper/dist/index.handler"]
