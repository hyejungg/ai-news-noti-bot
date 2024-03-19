import Message from "@ai-news-noti-bot/common/model/Message";
import KakaoworkMessageManager from "../types/class/KakaoworkMessageManager";
import { Messages } from "@ai-news-noti-bot/common/types/model";
import { BlockType } from "../types/interface/BlockType";
import { SendMessageDto } from "../types/interface/SendMessageDto";

const buildKakaoworkMessagesAndMessageDtos = (
  existsNewsData: boolean,
  messageData: SendMessageDto[],
  blockManager: KakaoworkMessageManager,
) => {
  const messageDto: Messages[] = [];
  blockManager.appendDateHeaderBlock("blue");

  if (!existsNewsData) {
    const inlinesTextData: BlockType[] = [];
    inlinesTextData.push(
      blockManager.createTextBlock("오늘은 소식이 없어요! 😅", false),
    );
    blockManager.appendTextBlockWithInlines(inlinesTextData);
    return messageDto;
  }

  // 카카오워크 메시지 생성 및 db 저장 dto 생성
  messageData
    .filter((data) => data.siteDataArray.length !== 0)
    .forEach((data) => {
      const name = data.siteName;
      const inlineTextData: BlockType[] = [
        blockManager.createTextBlock(`${data.siteName}\n\n`, true),
        ...data.siteDataArray
          .filter((item) => item.title !== null && item.url !== null)
          .map((item, index, array) => {
            const isLastItem = index === array.length - 1;
            // 가독성을 위해 뉴스 타이틀 간 \n 추가
            const title = isLastItem ? `${item.title}\n` : `${item.title}\n\n`;
            const url = item.url!;
            messageDto.push({ name, title: item.title!, url });
            return blockManager.createLinkBlock(title, url);
          }),
      ];
      blockManager.appendSectionBlockWithInlines(inlineTextData);
      blockManager.appendDividerBlock();
    });

  // TODO 사이트는 정적 웹사이트로 변경하기!
  blockManager.appendTextButtonBlock(
    "사이트 추가하기",
    "https://github.com/hyejungg/ai-news-noti-bot",
  );

  return messageDto;
};

const getUniqueMessageData = async (messageData: SendMessageDto[]) => {
  const targetTitles: string[] = messageData.flatMap((data) => {
    const validSiteDataArray = data.siteDataArray ?? [];
    const filteredSiteDataArray = validSiteDataArray.filter(
      (item): item is { title: string; url: string } => item.title != null,
    );
    const titles = filteredSiteDataArray.map((item) => item.title);
    return titles;
  });

  // db 에서 status 가 SEND_MESSAGE_SUCCESS 면서 현재 뉴스 타이틀과 일치하는 값들 조회
  const duplicateMessages = await Message.find({
    status: "SEND_MESSAGE_SUCCESS",
    "messages.title": { $in: targetTitles },
  });

  // 중복된 메시지 db 값 중의 제목을 추출
  const duplicateTitles = duplicateMessages.flatMap((doc) =>
    doc.messages.map((message) => message.title),
  );

  // targetTitles 중에서 duplicateTitles에 없는 제목만 필터링
  const uniqueTitles = targetTitles.filter(
    (title) => !duplicateTitles.includes(title),
  );

  for (const data of messageData) {
    data.siteDataArray = data.siteDataArray.filter((item) => {
      return item.title != null && uniqueTitles.includes(item.title);
    });
  }
  return messageData;
};

const sendMessageAndSave = async (
  messageDto: Messages[],
  blockManager: KakaoworkMessageManager,
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

  const newsCount = uniqueMessageData.filter(
    (data) => data.siteDataArray.length !== 0,
  ).length;
  const existsNewsData = newsCount > 0;

  const blockManager = new KakaoworkMessageManager();
  const messageDto = buildKakaoworkMessagesAndMessageDtos(
    existsNewsData,
    uniqueMessageData,
    blockManager,
  );

  await sendMessageAndSave(messageDto, blockManager);
};
export default { processMessages };
