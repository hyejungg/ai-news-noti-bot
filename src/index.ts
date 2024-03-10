import dotenv from "dotenv";
import express, { NextFunction, Request, Response } from "express";
import config from "./config";
import connectDB from "./loader";
import { TrendService } from "./service";
const app = express();
dotenv.config();

(async () => {
    // 데이터베이스 연결
    await connectDB();

    // 데이터베이스 로드가 완료된 후 TrendService.getInfoFromSite 호출
    await TrendService.getInfoFromSite();
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
