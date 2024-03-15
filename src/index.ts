import dotenv from "dotenv";
import config from "./config";
import connectDB from "./loader";
import { TrendService } from "./service";

dotenv.config();


(async () => {
    // 데이터베이스 연결
    await connectDB();

    // 데이터베이스 로드가 완료된 후 TrendService.getInfoFromSite 호출
    await TrendService.getInfoFromSite();
})();


// error handler
interface ErrorType {
    message: string;
    status: number;
}
