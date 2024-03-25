import { SiteData } from "../../types/interface/SiteData";
import Extractor from "../Extractor";
import PuppeteerManager from "../../types/class/PuppeteerManager";
import { SiteInfo } from "@ai-news-noti-bot/common/types/model";
import { ElementHandle } from "puppeteer-core";
import { SendMessageDto } from "../../types/interface/SendMessageDto";

export default class GeekNewsExtractor implements Extractor {
  private puppeteerManager: PuppeteerManager;
  private site: SiteInfo;

  constructor(site: SiteInfo) {
    console.log("geeknews extractor constructor");
    this.puppeteerManager = new PuppeteerManager();
    console.log("geeknews extractor constructor 2");
    this.site = site;
  }

  private async processLink(
    link: ElementHandle<HTMLDivElement>,
  ): Promise<SiteData> {
    let titleName;
    try {
      titleName = await link.$eval(
        "div.topictitle > a > h1",
        (el) => el.innerText,
      );
    } catch (e) {
      console.error(
        `${this.site.name} : titleName을 가져오는데 실패했습니다. error = ${e}`,
      );
      throw e;
    }

    let detailUrl = "";
    try {
      // 'div.topicdesc > a' 선택자가 존재하는지 확인
      const hasDetailUrl = await link.$("div.topicdesc > a");
      if (hasDetailUrl) {
        detailUrl = await link.$eval("div.topicdesc > a", (el) => el.href);
      } else {
        detailUrl = await link.$eval(
          "div.topictitle > a > h1",
          (el) => el.innerText,
        );
      }
    } catch (e) {
      console.error(
        `${this.site.name} : detailUrl을 가져오는데 실패했습니다. error = ${e}`,
      );
      throw e;
    }

    return {
      title: titleName,
      url: detailUrl,
    };
  }

  private async extract(): Promise<SiteData[]> {
    const page = this.puppeteerManager.getPage();

    await page.goto(this.site.url, {
      waitUntil: "networkidle2",
    });

    const selector = `body > main > article > div.topics > div.topic_row`;
    const links = await page.$$(selector);
    return Promise.all(links.map((link) => this.processLink(link)));
  }

  async extractToMessage(): Promise<SendMessageDto> {
    console.log("geeknews extractToMessage before initialize");
    await this.puppeteerManager.initialize();

    console.log("geeknews extractToMessage after initialize");
    let filteredSiteDataArray: SiteData[] = [];
    try {
      filteredSiteDataArray = (await this.extract()).filter((siteData) => {
        return this.site.keywords.some((keyword) =>
          siteData.title?.includes(keyword),
        );
      });
      console.log("filtered site data array", filteredSiteDataArray);
    } catch (e) {
      console.error(
        `${this.site.name} : extract에서 에러가 발생했습니다. error = ${e}`,
      );
      throw e;
    }

    console.log("geeknews extractToMessage before close");
    await this.puppeteerManager.close();
    console.log("geeknews extractToMessage after close");

    console.log(`${this.site.name} : 데이터 추출 성공`);
    return {
      siteName: this.site.name,
      siteDataArray: filteredSiteDataArray,
    };
  }
}
