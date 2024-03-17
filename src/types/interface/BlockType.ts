import { ButtonBlockType } from "./ButtonBlockType";
import { SectionBlockType } from "./SectionBlockType";

export interface BlockType {
    type: string;
    content?: SectionBlockType;
    text?: string;
    style?: string;
    url?: string;
    bold?: boolean;
    inlines?: BlockType[];
    action?: ButtonBlockType;
}
