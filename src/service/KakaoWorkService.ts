import KakaoworkMessageManager from "../types/class/KakaoworkMessageManager";
import { BlockType } from "../types/interface/BlockType";
import { MessageData } from "../types/interface/MessageData";

const getFormattedNowDate = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
};

const sendMessage = async (messageData: MessageData[]) => {
    const nowDate = getFormattedNowDate();
    const blockManager = new KakaoworkMessageManager(nowDate);

    blockManager.addHeader(`📢 ${nowDate} AI 소식`, "blue");

    for await (const data of messageData) {
        const inlineTextData: BlockType[] = [];
        inlineTextData.push(blockManager.addText(`${data.siteName}\n`, true));
        data.siteData.forEach((item, index, array) => {
            const isLastItem = index === array.length - 1;
            if (item.title && item.url) {
                const titleWithNewLine = isLastItem
                    ? item.title
                    : `${item.title}\n`;
                inlineTextData.push(
                    blockManager.addTextLinks(titleWithNewLine, item.url)
                );
            }
        });
        blockManager.addTextWithInlines(inlineTextData);
        blockManager.addDivider();
    }

    // TODO 사이트는 정적 웹사이트로 변경하기!
    blockManager.addTextButton(
        "사이트 추가하기",
        "https://github.com/hyejungg/ai-news-noti-bot"
    );

    blockManager.sendMessageBlocks();
};
export default { sendMessage };
