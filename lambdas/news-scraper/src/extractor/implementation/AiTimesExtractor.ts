import Extractor from "../Extractor";
import PuppeteerManager from "../../types/class/PuppeteerManager";
import { ElementHandle } from "puppeteer-core";
import { SiteData } from "../../types/interface/SiteData";
import { SiteInfo } from "@ai-news-noti-bot/common/types/model";
import { SendMessageDto } from "../../types/interface/SendMessageDto";

export default class AiTimesExtractor implements Extractor {
  private puppeteerManager: PuppeteerManager;
  private site: SiteInfo;

  constructor(site: SiteInfo) {
    this.puppeteerManager = new PuppeteerManager();
    this.site = site;
  }

  private async processLink(
    link: ElementHandle<HTMLDivElement>,
  ): Promise<SiteData | null> {
    let titleName;
    let detailUrl;
    try {
      titleName = await link.$eval("a > span", (el) => el.textContent);
    } catch (e) {
      console.error(
        `${this.site.name} : titleName을 가져오는데 실패했습니다. error = ${e}`,
      );
      throw e;
    }

    try {
      detailUrl = await link.$eval("a", (el) => el.getAttribute("href"));
    } catch (e) {
      console.error(
        `${this.site.name} : detailUrl을 가져오는데 실패했습니다. error = ${e}`,
      );
      throw e;
    }

    if (titleName && detailUrl) {
      return {
        title: titleName,
        url: detailUrl,
      };
    }

    return null;
  }

  private async extract(): Promise<SiteData[]> {
    const page = this.puppeteerManager.getPage();

    await page.goto(this.site.url, {
      waitUntil: "networkidle2",
    });

    const selector = `aside.side div.auto-article > div.item`;
    const links = await page.$$(selector);
    return Promise.all(
      links
        .map((link) => this.processLink(link))
        .filter((siteData): siteData is Promise<SiteData> => siteData !== null),
    );
  }

  async extractToMessage(): Promise<SendMessageDto> {
    await this.puppeteerManager.initialize();

    let extractedSiteData;
    try {
      extractedSiteData = await this.extract();
    } catch (e) {
      console.error(
        `${this.site.name} : extract에서 에러가 발생했습니다. error = ${e}`,
      );
      throw e;
    }

    const filteredSiteData = extractedSiteData.filter((siteData) =>
      this.site.keywords.some((keyword) => siteData.title?.includes(keyword)),
    );

    await this.puppeteerManager.close();

    console.log(`${this.site.name} : 데이터 추출 성공`);
    return {
      siteName: this.site.name,
      siteDataArray: filteredSiteData,
    };
  }
}
