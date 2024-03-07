import dotenv from "dotenv";
import express, { NextFunction, Request, Response } from "express";
import connectDB from "./loader";
const app = express();
dotenv.config();

connectDB();
// TrendService.getInfoFromSite();

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
    res.locals.error = req.app.get("env") === "production" ? err : {};

    res.status(err.status || 500);
    res.render("error");
});

app.listen(process.env.PORT, () => {
    console.log(`
    -- ${process.env.NODE_ENV}
    ################################################
          🛡️  Server listening on port ${process.env.PORT} 🛡️
    ################################################
  `);
}).on("error", (err) => {
    console.error(err);
    process.exit(1);
});
