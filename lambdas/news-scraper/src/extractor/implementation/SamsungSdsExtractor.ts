import PuppeteerManager from "../../types/class/PuppeteerManager";
import Extractor from "../Extractor";
import { SiteData } from "../../types/interface/SiteData";
import { SiteInfo } from "@ai-news-noti-bot/common/types/model";
import { SendMessageDto } from "../../types/interface/SendMessageDto";
import Site from "@ai-news-noti-bot/common/model/Site";

export default class SamsungSdsExtractor implements Extractor {
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

    return await page.evaluate((keywords) => {
      const elements = Array.from(
        document.querySelectorAll(".cont_list .item strong.md_tit"),
      );
      return elements
        .map((element): SiteData | null => {
          const aTag = element.querySelector("a");
          if (!aTag) {
            return null;
          }

          const isKeywordIncluded = keywords.some((keyword) =>
            aTag.textContent?.trim().includes(keyword),
          );
          if (!isKeywordIncluded) {
            return null;
          }

          return {
            title: aTag.textContent!.trim(),
            url: `https://www.samsungsds.com${aTag.getAttribute("href")}`,
          };
        })
        .filter((siteData): siteData is SiteData => siteData !== null);
    }, this.site.keywords);
  }

  async extractToMessage(): Promise<SendMessageDto> {
    await this.puppeteerManager.initialize();

    let siteDataArray: SiteData[] = [];
    try {
      siteDataArray = await this.extract();
    } catch (e) {
      console.error(
        `${this.site.name} : extract에서 에러가 발생했습니다. error = ${e}`,
      );
      throw e;
    }
    await this.puppeteerManager.close();

    console.log(`${this.site.name} : 데이터 추출 성공`);
    return {
      siteName: this.site.name,
      siteDataArray,
    };
  }
}
