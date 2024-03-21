export type ClueitArchiveResponseItem = {
  title: string;
  canonical_url: string;
  [key: string]: string | unknown; // 필요없지만 다른 속성도 있음
};
