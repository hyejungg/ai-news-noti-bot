import chromium from "@sparticuz/chromium";
import puppeteer, { Browser, Page } from "puppeteer";

export default class PuppeteerManager {
  private browser: Browser | null = null;
  private page: Page | null = null;

  public async initialize(): Promise<void> {
    console.log("initialize puppeteer");
    console.log("real");
    if (process.env.PHASE !== "prod") {
      this.browser = await puppeteer.launch({
        executablePath: puppeteer.executablePath(),
        args: [...puppeteer.defaultArgs(), "--no-sandbox"],
        defaultViewport: chromium.defaultViewport,
        headless: false,
      });
    } else {
      this.browser = await puppeteer.launch({
        args: chromium.args,
        defaultViewport: chromium.defaultViewport,
        executablePath: await chromium.executablePath(),
        headless: !!chromium.headless,
      });
    }
    // if (config.nodeEnv === "real") {
    // } else {
    //   console.log("dev");
    //   this.browser = await puppeteer.launch({
    //     args: [
    //       "--no-sandbox",
    //       "--disable-setuid-sandbox",
    //       "--disable-dev-shm-usage",
    //       "--disable-gpu",
    //     ],
    //     headless: false, // 브라우저 창을 보이게 설정
    //     executablePath: puppeteer.executablePath(),
    //   });
    // }
    console.log("initialize puppeteer 2");
    this.page = await this.browser.newPage();
    console.log("initialize puppeteer 3");
    await this.page.setViewport({
      width: 1920,
      height: 1080,
    });
    console.log("initialize puppeteer 4");
  }

  public getPage(): Page {
    if (!this.page) {
      throw new Error("Page is not initialized. Call initialize() first.");
    }
    return this.page;
  }

  public async close(): Promise<void> {
    if (this.browser) {
      console.log("close puppeteer");
      await this.browser.close();
      console.log("close puppeteer 2");
    }
    this.browser = null;
    this.page = null;
  }
}
