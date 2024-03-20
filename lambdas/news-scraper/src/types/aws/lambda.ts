/**
 * EventBridgeEvent 관련 타입 선언
 * 참고: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-events-structure.html
 */
// EventBridgeEvent의 'detail-type' 항목 타입
export type EventBridgeDetailType = string;

// EventBridgeEvent의 'detail' 항목 타입
export type EventBridgeDetail = Record<string, unknown>;

// Lambda 반환 타입
export type LambdaResult = any;
