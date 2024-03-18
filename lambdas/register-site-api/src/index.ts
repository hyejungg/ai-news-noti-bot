import { APIGatewayProxyHandler } from "aws-lambda";
import Site from "@ai-news-noti-bot/common/model/Site";
import { SiteInfo } from "@ai-news-noti-bot/common/types/model/SiteInfo";
import connectDB from "@ai-news-noti-bot/common/loader";

export const handler: APIGatewayProxyHandler = async (event, context) => {
    const contentType = event.headers?.['content-type'];
    if (contentType !== "application/x-www-form-urlencoded") {
        return {
            statusCode: 400,
            body: "Invalid content type",
        };
    }
    if (!event.body) {
        return {
            statusCode: 400,
            body: "No data",
        };
    }

    await connectDB();

    const formData = new URLSearchParams(event.body);
    const siteInfo: SiteInfo = {
        name: formData.get("name") ?? "",
        url: formData.get("url") ?? "",
        keywords: formData.get("keywords") === "" ? [] : formData.get("keywords")?.split(",")?.map(keyword => keyword.trim()) ?? [],
        requestedBy: formData.get("requestedBy") ?? "",
    }

    await Site.create(siteInfo);

    return {
        statusCode: 200,
        body: "success",
    }
};
