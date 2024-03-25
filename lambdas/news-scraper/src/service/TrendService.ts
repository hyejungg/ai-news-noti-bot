import Site from "@ai-news-noti-bot/common/model/Site";
import ExtractorFactory from "../factory/ExcractorFactory";

const getInfoFromSite = async () => {
  const sites = await Site.find({ verified: true });
  console.log(`sites: ${sites}`);

  if (!sites || sites.length === 0) {
    console.error("site 정보를 가져오는 것을 실패했습니다!");
    return;
  }

  const result = [];
  for await (const site of sites) {
    const message =
      await ExtractorFactory.createExtractor(site).extractToMessage();
    result.push(message);
  }

  return result;
};

export default { getInfoFromSite };
