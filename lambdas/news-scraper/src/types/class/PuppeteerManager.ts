import puppeteer, { Browser, Page } from "puppeteer";

export default class PuppeteerManager {
  private browser: Browser | null = null;
  private page: Page | null = null;

  public async initialize(): Promise<void> {
    this.browser = await puppeteer.launch({
      headless: false, // 브라우저 창을 보이게 설정
      executablePath: puppeteer.executablePath(),
    });
    this.page = await this.browser.newPage();
    await this.page.setViewport({
      width: 1920,
      height: 1080,
    });
  }

  public getPage(): Page {
    if (!this.page) {
      throw new Error("Page is not initialized. Call initialize() first.");
    }
    return this.page;
  }

  public async close(): Promise<void> {
    if (this.browser) {
      await this.browser.close();
    }
    this.browser = null;
    this.page = null;
  }
}
