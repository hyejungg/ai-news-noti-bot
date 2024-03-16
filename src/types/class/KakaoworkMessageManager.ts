import * as https from "https";
import config from "../../config";
import { BlockType } from "../interface/BlockType";

const HTTP_METHOD_POST = "POST";
const HTTP_CONTENT_TYPE = "application/json";

const getFormattedNowDate = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
};

export default class KakaoworkMessageManager {
    private blocks: BlockType[] = [];
    private webhookUrl: string = config.kakaoWorkWebHookUrl;
    private nowDate: string = "";

    constructor() {
        this.nowDate = getFormattedNowDate();
    }

    getBlocks() {
        return {
            text: `📢 ${this.nowDate} AI 소식`,
            blocks: this.blocks,
        };
    }

    sendMessageBlocks() {
        return new Promise((resolve, reject) => {
            const data = JSON.stringify(this.getBlocks());
            const url = new URL(this.webhookUrl);
            const options = {
                hostname: url.hostname,
                path: url.pathname,
                port: 443,
                method: HTTP_METHOD_POST,
                headers: {
                    "Content-Type": HTTP_CONTENT_TYPE,
                    "Content-Length": Buffer.byteLength(data),
                },
            };

            const req = https.request(options, (res) => {
                if (
                    res.statusCode &&
                    res.statusCode >= 200 &&
                    res.statusCode < 300
                ) {
                    resolve(res.statusCode);
                } else {
                    reject(
                        new Error(
                            `Request failed with status code: ${res.statusCode}`
                        )
                    );
                }
            });
            req.on("error", (e) => {
                reject(e);
            });
            req.write(data);
            req.end();
        });
    }

    addHeader(text: string, style: string) {
        this.blocks.push({
            type: "header",
            text: text,
            style: style,
        });
    }

    addHeaderTitleWithNowDate(style: string) {
        this.blocks.push({
            type: "header",
            text: `📢 ${this.nowDate} AI 소식`,
            style: style,
        });
    }

    addDivider() {
        this.blocks.push({
            type: "divider",
        });
    }

    addTextLinks(text: string, url: string) {
        return {
            type: "link",
            text: text,
            url: `${url}`,
        };
    }

    addText(text: string, isBold: boolean) {
        return {
            type: "styled",
            text: text,
            bold: isBold,
        };
    }

    addTextButton(
        buttonText: string,
        openWebUrl: string,
        style: string = "default"
    ) {
        this.blocks.push({
            type: "button",
            text: buttonText,
            style: style,
            action: {
                type: "open_system_browser",
                name: "button1",
                value: openWebUrl,
            },
        });
    }

    addTextWithInlines(inlines: BlockType[]) {
        this.blocks.push({
            type: "text",
            text: "test sample",
            inlines: [...inlines],
        });
    }
}
