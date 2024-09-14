export default {
  nodeEnv: (process.env.NODE_ENV as string) || ("development" as string),
  /**
   * Your favorite port
   */
  mongoDbUri: process.env.MONGO_DB_URI as string,
  mongoDbRealUri: process.env.MONGO_DB_REAL_URI as string,
  /**
   * spread sheets id
   */
  spreadsheetsId: process.env.SPREADSHEET_DOC_ID as string,
  /**
   * google service key json
   */
  googleServiceKey: process.env.GOOGLE_SERVICE_KEY as string,
  /**
   * google service email
   */
  googleServiceEmail: process.env.GOOGLE_SERVICE_EMAIL as string,
  /**
   * kakaowork webhook url
   */
  kakaoWorkWebHookUrl: process.env.KAWORK_WEBHOOK_URI as string,
};
