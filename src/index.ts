import { EventBridgeHandler } from "aws-lambda";
import dotenv from "dotenv";
import connectDB from "./loader";
import { KakaoWorkService, TrendService } from "./service";
import {
    EventBridgeDetail,
    EventBridgeDetailType,
    LambdaResult,
} from "./types/aws/lambda";

dotenv.config();

export const handler: EventBridgeHandler<
    EventBridgeDetailType,
    EventBridgeDetail,
    LambdaResult
> = async (event, context) => {
    try {
        // 데이터베이스 연결
        await connectDB();

        // 데이터베이스 로드가 완료된 후 TrendService.getInfoFromSite 호출
        const messageData = await TrendService.getInfoFromSite();

        if (messageData === undefined) {
            console.error("크롤링을 통해 뉴스 메시지 생성 실패");
            return;
        }
        await KakaoWorkService.processMessages(messageData);
    } catch (e) {
        console.error(e);
    }
};

// handler(); // 로컬에서 실행 시 주석 해제하고 실행하기
