import mongoose from "mongoose";
import { MessageInfo } from "../types/interface/MessageInfo";

const MessageSchema = new mongoose.Schema(
    {
        type: {
            type: String,
            required: true,
        },
        status: {
            type: String,
            required: true,
        },
        messages: [
            {
                name: {
                    type: String,
                    required: false,
                },
                title: {
                    type: String,
                    required: false,
                },
                url: {
                    type: String,
                    required: false,
                },
            },
        ],
    },
    {
        timestamps: true,
        versionKey: false, // __v(버전 필드) 생성 방지
    }
);

// timestamps 로 선언 시 생성되는 createdAt, updatedAt
MessageSchema.index(
    { createdAt: 1 },
    { expireAfterSeconds: 60 * 60 * 24 * 180 }
); // 180일

export default mongoose.model<MessageInfo & mongoose.Document>(
    "Messages",
    MessageSchema
);
