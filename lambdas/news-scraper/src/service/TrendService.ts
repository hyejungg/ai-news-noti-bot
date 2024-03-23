import Site from "@ai-news-noti-bot/common/model/Site";
import ExtractorFactory from "../factory/ExcractorFactory";

const getInfoFromSite = async () => {
  const sites = await Site.find({ verified: true });
  console.log(`sites: ${sites}`);

  if (!sites) {
    console.error("site 정보를 가져오는 것을 실패했습니다!");
    return;
  }

  return await Promise.all(
    sites.map(async (site) => {
      return ExtractorFactory.createExtractor(site).extractToMessage();
    }),
  );
};

export default { getInfoFromSite };
