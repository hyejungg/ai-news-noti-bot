import { ButtonBlockType } from "./ButtonBlockType";

export interface BlockType {
    type: string;
    text?: string;
    style?: string;
    url?: string;
    bold?: boolean;
    inlines?: BlockType[];
    action?: ButtonBlockType;
}
