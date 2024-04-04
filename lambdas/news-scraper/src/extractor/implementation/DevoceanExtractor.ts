import Extractor from "../Extractor";
import PuppeteerManager from "../../types/class/PuppeteerManager";
import { SiteInfo } from "@ai-news-noti-bot/common/types/model";
import { SiteData } from "../../types/interface/SiteData";
import { SendMessageDto } from "../../types/interface/SendMessageDto";

export default class DevoceanExtractor implements Extractor {
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

    const clickSelector = `div.sec-area > ul.sec-area-list01 > li:first-child > div a > h3.pc_view`;
    await page.click(clickSelector);
    await page.waitForNavigation();

    return await page.evaluate((keywords) => {
      const spanElements = Array.from(document.querySelectorAll("a > span")); // 모든 <a> 태그 밑의 <span> 태그를 선택합니다.

      return spanElements
        .map((span): SiteData | null => {
          const isKeywordIncluded = keywords.some((keyword: string) =>
            span.textContent?.trim().includes(keyword),
          );
          if (!isKeywordIncluded) {
            return null;
          }

          const aTag = span.parentElement;
          if (!aTag) {
            return null;
          }

          return {
            url: aTag.getAttribute("href"),
            title: span.innerHTML,
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
    console.log(siteDataArray);
    return {
      siteName: this.site.name,
      siteDataArray,
    };
  }
}
