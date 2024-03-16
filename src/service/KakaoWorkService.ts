import Message from "../model/Message";
import KakaoworkMessageManager from "../types/class/KakaoworkMessageManager";
import { BlockType } from "../types/interface/BlockType";
import { Messages } from "../types/interface/Messages";
import { SendMessageDto } from "../types/interface/SendMessageDto";

const buildKakaoworkMessagesAndMessageDtos = (
    existsNewsData: boolean,
    messageData: SendMessageDto[],
    blockManager: KakaoworkMessageManager
) => {
    let messageDto: Messages[] = [];
    blockManager.addHeaderTitleWithNowDate("blue");

    if (!existsNewsData) {
        const inlinesTextData: BlockType[] = [];
        inlinesTextData.push(
            blockManager.addText("오늘은 소식이 없어요! 😅", false)
        );
        blockManager.addTextWithInlines(inlinesTextData);
        return [];
    }

    // 카카오워크 메시지 생성 및 db 저장 dto 생성
    for (const data of messageData) {
        const inlineTextData: BlockType[] = [];
        if (data.siteData.length !== 0) {
            inlineTextData.push(
                blockManager.addText(`${data.siteName}\n`, true)
            );
            data.siteData.forEach((item, index, array) => {
                const isLastItem = index === array.length - 1;
                if (item.title && item.url) {
                    const titleWithNewLine = isLastItem
                        ? item.title
                        : `${item.title}\n`;
                    inlineTextData.push(
                        blockManager.addTextLinks(titleWithNewLine, item.url)
                    );
                    messageDto.push({
                        name: data.siteName,
                        title: item.title,
                        url: item.url,
                    });
                }
            });
            blockManager.addTextWithInlines(inlineTextData);
            blockManager.addDivider();
        }
    }

    // TODO 사이트는 정적 웹사이트로 변경하기!
    blockManager.addTextButton(
        "사이트 추가하기",
        "https://github.com/hyejungg/ai-news-noti-bot"
    );

    return messageDto;
};

const getUniqueMessageData = async (messageData: SendMessageDto[]) => {
    const targetTitles: string[] = messageData.flatMap((data) => {
        const validSiteData = data.siteData ?? [];
        const filteredSiteData = validSiteData.filter(
            (item): item is { title: string; url: string } => item.title != null
        );
        const titles = filteredSiteData.map((item) => item.title);
        return titles;
    });

    // db 에서 status 가 SEND_MESSAGE_SUCCESS 면서 현재 뉴스 타이틀과 일치하는 값들 조회
    const duplicateMessages = await Message.find({
        status: "SEND_MESSAGE_SUCCESS",
        "messages.title": { $in: targetTitles },
    });

    // 중복된 메시지 db 값 중의 제목을 추출
    const duplicateTitles = duplicateMessages.flatMap((doc) =>
        doc.messages.map((message) => message.title)
    );

    // targetTitles 중에서 duplicateTitles에 없는 제목만 필터링
    const uniqueTitles = targetTitles.filter(
        (title) => !duplicateTitles.includes(title)
    );

    for (const data of messageData) {
        data.siteData = data.siteData.filter((item) => {
            return item.title != null && uniqueTitles.includes(item.title);
        });
    }
    return messageData;
};

const sendMessageAndSave = async (
    messageDto: Messages[],
    blockManager: KakaoworkMessageManager
) => {
    try {
        const statusCode = await blockManager.sendMessageBlocks();
        console.log(`Status Code: ${statusCode}`);
        const status =
            statusCode === 200 ? "SEND_MESSAGE_SUCCESS" : "SEND_MESSAGE_FAIL";
        const message = new Message({
            type: "KAKAOWORK",
            status,
            messages: messageDto,
        });
        await message.save();
    } catch (error) {
        console.error(error);
    }
};

const processMessages = async (messageData: SendMessageDto[]) => {
    const uniqueMessageData = await getUniqueMessageData(messageData);

    const newsCount = uniqueMessageData
        .map((data) => data.siteData.length !== 0)
        .filter((isNotEmpty) => isNotEmpty).length;
    const existsNewsData = newsCount > 0;

    const blockManager = new KakaoworkMessageManager();
    const messageDto = buildKakaoworkMessagesAndMessageDtos(
        existsNewsData,
        uniqueMessageData,
        blockManager
    );

    await sendMessageAndSave(messageDto, blockManager);
};
export default { processMessages };
