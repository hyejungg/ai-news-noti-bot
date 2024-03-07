import mongoose from "mongoose";
import { MessageInfo } from "../types/interface/MessageInfo";

const MessageSchema = new mongoose.Schema(
    {
        type: {
            type: String,
            required: true,
        },
        messages: [
            {
                name: {
                    type: String,
                    required: true,
                },
                title: {
                    type: String,
                    required: true,
                },
                url: {
                    type: String,
                    required: true,
                },
            },
        ],
    },
    {
        timestamps: true,
    }
);

// timestamps 로 선언 시 생성되는 createdAt, updatedAt
MessageSchema.index({ createdAt: 1 }, { expireAfterSeconds: 604800 }); // 7일

export default mongoose.model<MessageInfo & mongoose.Document>(
    "Messages",
    MessageSchema
);
