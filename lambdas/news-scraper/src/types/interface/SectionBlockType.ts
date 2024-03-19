import { BlockType } from "./BlockType";

export interface SectionBlockType {
  type: string;
  text: string;
  inlines?: BlockType[];
}
