import Extractor from "../Extractor";
import PuppeteerManager from "../../types/class/PuppeteerManager";
import { SiteInfo } from "@ai-news-noti-bot/common/types/model";
import { SiteData } from "../../types/interface/SiteData";
import { SendMessageDto } from "../../types/interface/SendMessageDto";
import { ClueitArchiveResponseItem } from "../../types/news/ClueitArchiveResponseItem";

export default class ClueitExtractor implements Extractor {
  private puppeteerManager: PuppeteerManager;
  private site: SiteInfo;

  constructor(site: SiteInfo) {
    this.puppeteerManager = new PuppeteerManager();
    this.site = site;
  }

  private async extract(): Promise<SiteData[]> {
    const page = this.puppeteerManager.getPage();

    await page.goto(this.site.url, {
      waitUntil: "networkidle2",
    });

    const today = new Date();
    const dayOfWeek = today.getDay(); // 일요일이 0, 월요일이 1, ..., 토요일이 6

    // 클루잇은 수요일에만 업로드 되어서 수요일에만 가져오도록 수정
    if (dayOfWeek !== 3) {
      return [];
    }

    const apiPath = "https://clueit.substack.com/api/v1/archive";
    const paramsData = {
      sort: "new",
      search: "",
      offset: "0",
      limit: "1",
    };
    const params = new URLSearchParams(paramsData);

    const url = `${apiPath}?${params.toString()}`;

    let posts;
    try {
      const response = await fetch(url, { method: "GET" });
      posts = (await response.json()) as ClueitArchiveResponseItem[];
    } catch (e) {
      console.error(
        `${this.site.name} : api 데이터를 가져오는데 실패했습니다. error = ${e}`,
      );
      throw e;
    }

    return posts.map((post) => {
      return {
        title: post.title,
        url: post.canonical_url,
      };
    });
  }

  async extractToMessage(): Promise<SendMessageDto> {
    await this.puppeteerManager.initialize();

    const filteredSiteDataArray = await this.extract();

    await this.puppeteerManager.close();

    console.log(`${this.site.name} : 데이터 추출 성공`);
    console.log(filteredSiteDataArray);
    return {
      siteName: this.site.name,
      siteDataArray: filteredSiteDataArray,
    };
  }
}
