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
        verified: {
            type: Boolean,
            required: true,
            default: false,
        },
        requestedBy: {
            type: String,
            required: false,
        }
    },
    {
        timestamps: true,
        versionKey: false, // __v(버전 필드) 생성 방지
    }
);

export default mongoose.model<SiteInfo & mongoose.Document>("Site", SiteSchema);
