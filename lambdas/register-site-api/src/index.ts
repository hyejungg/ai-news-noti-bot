import { APIGatewayProxyHandler } from "aws-lambda";
import Site from "@ai-news-noti-bot/common/model/Site";
import { SiteInfo } from "@ai-news-noti-bot/common/types/model/SiteInfo";
import connectDB from "@ai-news-noti-bot/common/loader";

const errorResponse = {
  statusCode: 302,
  headers: {
    Location: "https://d1qbk7p5aewspc.cloudfront.net/error.html",
  },
  body: "",
};
const successResponse = {
  statusCode: 302,
  headers: {
    Location: "https://d1qbk7p5aewspc.cloudfront.net/success.html",
  },
  body: "",
};

export const handler: APIGatewayProxyHandler = async (event, context) => {
  try {
    const contentType = event.headers?.["content-type"];

    if (contentType !== "application/x-www-form-urlencoded") {
      return errorResponse;
    }
    if (!event.body) {
      return errorResponse;
    }

    await connectDB();

    const formData = new URLSearchParams(event.body);
    const siteInfo: SiteInfo = {
      name: formData.get("name") ?? "",
      url: formData.get("url") ?? "",
      keywords:
        formData.get("keywords") === ""
          ? []
          : formData
              .get("keywords")
              ?.split(",")
              ?.map((keyword) => keyword.trim()) ?? [],
      requestedBy: formData.get("requestedBy") ?? "",
    };

    await Site.create(siteInfo);

    return successResponse;
  } catch (e) {
    return errorResponse;
  }
};
