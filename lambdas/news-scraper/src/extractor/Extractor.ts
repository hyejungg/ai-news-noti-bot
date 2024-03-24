import { SendMessageDto } from "../types/interface/SendMessageDto";

export default interface Extractor {
  extractToMessage(): Promise<SendMessageDto>;
}
