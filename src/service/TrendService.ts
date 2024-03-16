import { Page } from "puppeteer";
import Site from "../model/Site";
import PuppeteerManager from "../types/class/PuppeteerManager";

interface SiteData {
    title: string;
    url: string;
}

const getMetaTag = async (page: Page): Promise<SiteData[]> => {
    const title = await page.$eval('meta[property="og:title"]', (element) =>
        element.getAttribute("content")
    );
    const url = await page.$eval('meta[property="og:url"]', (element) =>
        element.getAttribute("content")
    );
    return [{ title: title ?? "", url: url ?? "" }];
};

const filterByKeyword = (originalData: SiteData[], keywords: string[]) => {
    if (originalData.length === 0) {
        return [];
    }
    return originalData.filter((obj) => {
        return keywords.some((keyword) => obj.title.includes(keyword));
    });
};

const getInfoFromSite = async () => {
    const sites = await Site.find({verified: true});
    console.log(`sites: ${sites}`);

    if (!sites) {
        console.log("hi");
        return;
    }
    return;
    const puppeteerManager = new PuppeteerManager();
    await puppeteerManager.initialize();
    const page = puppeteerManager.getPage();

    for (const site of sites) {
        await page.goto(site.url, {
            waitUntil: "networkidle2",
        });

        if (site.name === "긱뉴스") {
            const selector = `body > main > article > div.topics > div.topic_row`;
            const links = await page.$$(selector);
            const tempData: SiteData[] = [];
            for (const link of links) {
                const titleName = await link.$eval(
                    "div.topictitle > a > h1",
                    (el) => el.innerText
                );
                const detailUrl = await link.$eval(
                    "div.topicdesc > a",
                    (el) => el.href
                );
                tempData.push({ title: titleName, url: detailUrl });
            }
            const filteredData = filterByKeyword(tempData, site.keywords);
            console.log(filteredData);
        }
        if (site.name === "AI 타임즈") {
            const selector = `aside.side div.auto-article > div.item`;
            const links = await page.$$(selector);
            const tempData: SiteData[] = [];
            for (const link of links) {
                const titleName = await link.$eval(
                    "a > span",
                    (el) => el.innerText
                );
                const detailUrl = await link.$eval("a", (el) => el.href);
                tempData.push({ title: titleName, url: detailUrl });
            }
            console.log(tempData);
        }
        if (site.name === "삼성 SDS") {
            const data = await page.evaluate((keywords) => {
                const items: SiteData[] = [];
                const elements = Array.from(
                    document.querySelectorAll(".cont_list .item strong.md_tit")
                );
                elements.forEach((element) => {
                    const aTag = element.querySelector("a");
                    if (aTag) {
                        const isKeywordIncluded = keywords.some((keyword) =>
                            aTag.textContent?.trim().includes(keyword)
                        );
                        if (isKeywordIncluded) {
                            items.push({
                                title: aTag.textContent!.trim(),
                                url: `https://www.samsungsds.com/kr/${aTag.getAttribute(
                                    "href"
                                )}`,
                            });
                        }
                    }
                });
                return items;
            }, site.keywords);

            console.log(data);
        }
        if (site.name === "데보션") {
            const clickSelector = `div.sec-area > ul.sec-area-list01 > li:first-child > div`;
            await page.click(clickSelector);
            await page.waitForNavigation();
            const data = await page.evaluate((keywords) => {
                const elements = Array.from(
                    document.querySelectorAll("a > span")
                ); // 모든 <a> 태그 밑의 <span> 태그를 선택합니다.
                return elements.reduce((acc, span) => {
                    const isKeywordIncluded = keywords.some((keyword) =>
                        span.textContent?.trim().includes(keyword)
                    );

                    if (isKeywordIncluded) {
                        const aTag = span.parentElement;
                        if (aTag) {
                            acc.push({
                                url: aTag.getAttribute("href"),
                                title: span.innerHTML,
                            });
                        }
                    }
                    return acc;
                }, [] as { title: string | null; url: string | null }[]);
            }, site.keywords);

            console.log(data);
        }
        if (site.name === "클루잇") {
            const apiPath = "https://clueit.substack.com/api/v1/archive"
            const paramsData = {
                sort: "new",
                search: "",
                offset: "0",
                limit: "5"
            };
            const params = new URLSearchParams(paramsData);

            const url = `${apiPath}?${params.toString()}`;

            const response = await fetch(url, {method: "GET"});
            const posts = await response.json();

            const siteData: SiteData[] = posts.map((post: any) => {
                return {
                    title: post.title,
                    url: post.canonical_url
                }
            })

            console.log(siteData)
        }
    }

    await puppeteerManager.close();
};

export default { getInfoFromSite };
