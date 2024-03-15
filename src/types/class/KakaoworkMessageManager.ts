import * as https from "https";
import config from "../../config";
import { BlockType } from "../interface/BlockType";

const HTTP_METHOD_POST = "POST";
const HTTP_CONTENT_TYPE = "application/json";

export default class KakaoworkMessageManager {
    private blocks: BlockType[] = [];
    private webhookUrl: string = config.kakaoWorkWebHookUrl;
    private nowDate: string;

    constructor(nowDate: string) {
        this.nowDate = nowDate;
    }

    getBlocks() {
        return {
            text: `📢 ${this.nowDate} AI 소식`,
            blocks: this.blocks,
        };
    }

    sendMessageBlocks() {
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
            console.log(`Status Code: ${res.statusCode}`);
        });
        req.on("error", (e) => {
            console.error(e);
        });
        req.write(data);
        req.end();
    }

    addHeader(text: string, style: string) {
        this.blocks.push({
            type: "header",
            text: text,
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
