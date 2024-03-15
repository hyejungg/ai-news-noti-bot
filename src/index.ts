import dotenv from "dotenv";
import config from "./config";
import connectDB from "./loader";
import { TrendService } from "./service";
import {EventBridgeHandler} from "aws-lambda";
import {EventBridgeDetail, EventBridgeDetailType, LambdaResult} from "./types/aws/lambda";

dotenv.config();

// error handler
interface ErrorType {
    message: string;
    status: number;
}

export const handler: EventBridgeHandler<EventBridgeDetailType, EventBridgeDetail, LambdaResult> = async (event, context) => {
    try {
        // 데이터베이스 연결
        await connectDB();

        // 데이터베이스 로드가 완료된 후 TrendService.getInfoFromSite 호출
        await TrendService.getInfoFromSite();

        return 0;
    } catch (e) {
        console.error(e);
        return 1;
    }
};
