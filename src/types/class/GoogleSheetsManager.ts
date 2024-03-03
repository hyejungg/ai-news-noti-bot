import { JWT } from "google-auth-library";
import {
    GoogleSpreadsheet,
    GoogleSpreadsheetWorksheet,
} from "google-spreadsheet";
import config from "../../config";

const googleServiceKey = JSON.parse(config.googleServiceKey);

const serviceAccountAuth = new JWT({
    email: config.googleServiceEmail,
    key: googleServiceKey.private_key,
    scopes: ["https://www.googleapis.com/auth/spreadsheets"],
});

export default class GoogleSheetsManager {
    private docs: GoogleSpreadsheet | null = null;
    private sheets: GoogleSpreadsheetWorksheet | null = null;

    constructor() {
        try {
            this.docs = new GoogleSpreadsheet(
                config.spreadsheetsId,
                serviceAccountAuth
            );
        } catch (err) {
            console.error("구글 연결 실패");
        }
    }

    public async getDocs() {
        if (!this.docs) {
            throw new Error(
                "docs is not initialized. Call initialize() first."
            );
        }
        return this.docs;
    }

    public async getSheetsByIndex(index: number) {
        if (!this.docs) {
            throw new Error(
                "docs is not initialized. Call initialize() first."
            );
        }
        await this.docs.loadInfo();
        this.sheets = this.docs.sheetsByIndex[index];
        if (!this.sheets) {
            throw new Error(`Sheet at index ${index} not found.`);
        }
        return this.sheets;
    }

    public async getRows() {
        if (!this.docs) {
            throw new Error(
                "docs is not initialized. Call initialize() first."
            );
        }
        if (!this.sheets) {
            throw new Error(
                "sheets is not initialized. Call initialize() first."
            );
        }
        const rows = await this.sheets.getRows();
        if (!rows) {
            throw new Error("가져오기 실패");
        }
        return rows;
    }
}
