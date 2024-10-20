# build stage
FROM node:20 AS builder


# 전체 파일 복사
COPY . ./build

# 디렉터리 위치 이동
WORKDIR ./build

# pnpm 설치
RUN npm install -g typescript pnpm \
    && pnpm install

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

# production stage
# AWS Lambda의 Node.js 20 베이스 이미지 사용
FROM public.ecr.aws/lambda/nodejs:20

# phase
ENV PHASE=prod

# amazonlinux2023 에서 chrome 실행에 필요한 라이브러리 설치
RUN dnf install -y libXcomposite libXdamage libXrandr libxkbcommon pango alsa-lib atk at-spi2-atk cups-libs libdrm mesa-libgbm dbus-libs.x86_64 nss

WORKDIR ${LAMBDA_TASK_ROOT}
COPY --from=builder /build/lambdas/news-scraper/dist ./

# production stage 이미지에 chrome 설치
RUN lambdas/news-scraper/node_modules/.bin/puppeteer browsers install chrome

CMD ["index.handler"]
