import dotenv from "dotenv";
import express, { NextFunction, Request, Response } from "express";
import config from "./config";
import connectDB from "./loader";
import { KakaoWorkService, TrendService } from "./service";
const app = express();
dotenv.config();

(async () => {
    // 데이터베이스 연결
    await connectDB();
    // 데이터베이스 로드가 완료된 후 TrendService.getInfoFromSite 호출
    const messageData = await TrendService.getInfoFromSite();

    if (messageData === undefined) {
        console.error("크롤링을 통해 뉴스 메시지 생성 실패");
        return;
    }
    await KakaoWorkService.processMessages(messageData);
})();

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// error handler
interface ErrorType {
    message: string;
    status: number;
}

app.use(function (
    err: ErrorType,
    req: Request,
    res: Response,
    next: NextFunction
) {
    res.locals.message = err.message;
    res.locals.error = req.app.get("env") === "real" ? err : {};

    res.status(err.status || 500);
    res.render("error");
});

app.listen(config.port, () => {
    console.log(`
    -- ${config.nodeEnv}
    ################################################
          🛡️  Server listening on port ${config.port} 🛡️
    ################################################
  `);
}).on("error", (err) => {
    console.error(err);
    process.exit(1);
});
