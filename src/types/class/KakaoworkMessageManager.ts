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

    async sendMessageBlocks() {
        const data = JSON.stringify(this.getBlocks());
        const response = await fetch(this.webhookUrl, {
            method: HTTP_METHOD_POST,
            headers: {
                "Content-Type": HTTP_CONTENT_TYPE,
            },
            body: data,
        });
        return response.status;
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
