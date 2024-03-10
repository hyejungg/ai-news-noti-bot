import mongoose from "mongoose";

export interface MessageInfo {
    type: string;
    keywords: mongoose.Types.ObjectId[];
}
