import dotenv from "dotenv";

// Set the NODE_ENV to 'development' by default
process.env.NODE_ENV = process.env.NODE_ENV || "development";

const envFound = dotenv.config();
if (envFound.error) {
    // This error should crash whole process

    throw new Error("⚠️  Couldn't find .env file  ⚠️");
}

export default {
    /**
     * Your favorite port
     */
    port: parseInt(process.env.PORT as string, 10) as number,
    /**
     * Your favorite port
     */
    mongoDbUri: process.env.MONGO_DB_URI as string,
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
};
