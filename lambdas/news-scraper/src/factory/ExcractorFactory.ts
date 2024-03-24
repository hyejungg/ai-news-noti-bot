import AiTimesExtractor from "../extractor/implementation/AiTimesExtractor";
import SamsungSdsExtractor from "../extractor/implementation/SamsungSdsExtractor";
import DevoceanExtractor from "../extractor/implementation/DevoceanExtractor";
import ClueitExtractor from "../extractor/implementation/ClueitExtractor";
import Extractor from "../extractor/Extractor";
import GeekNewsExtractor from "../extractor/implementation/GeekNewsExtractor";
import { SiteInfo } from "@ai-news-noti-bot/common/types/model";

export default class ExtractorFactory {
  static createExtractor(site: SiteInfo): Extractor {
    switch (site.name) {
      case "긱뉴스":
        return new GeekNewsExtractor(site);
      case "AI 타임즈":
        return new AiTimesExtractor(site);
      case "삼성 SDS":
        return new SamsungSdsExtractor(site);
      case "데보션":
        return new DevoceanExtractor(site);
      case "클루잇":
        return new ClueitExtractor(site);
      default:
        throw new Error(`지원하지 않는 사이트입니다. : ${site.name}`);
    }
  }
}
