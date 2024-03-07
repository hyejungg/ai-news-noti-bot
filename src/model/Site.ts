import mongoose from "mongoose";
import { SiteInfo } from "../types/interface/SiteInfo";

const SiteSchema = new mongoose.Schema(
    {
        name: {
            type: String,
            required: true,
        },
        url: {
            type: String,
            required: true,
        },
        keywords: {
            type: [String],
            required: false,
        },
    },
    {
        timestamps: true,
    }
);

export default mongoose.model<SiteInfo & mongoose.Document>("Site", SiteSchema);
