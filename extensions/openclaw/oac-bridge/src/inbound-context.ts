import type { ResolvedOacBridgeAccount } from "./types.js";

const CHANNEL_ID = "oac-bridge";

export type OacInboundMessage = {
  body: string;
  oacSessionId: string;
  senderName: string;
  commandAuthorized: boolean;
};

export function buildOacBridgeInboundContext<TContext>(params: {
  finalizeInboundContext: (ctx: Record<string, unknown>) => TContext;
  account: ResolvedOacBridgeAccount;
  msg: OacInboundMessage;
  sessionKey: string;
}): TContext {
  const { account, msg, sessionKey } = params;
  return params.finalizeInboundContext({
    Body: msg.body,
    RawBody: msg.body,
    CommandBody: msg.body,
    From: `oac-bridge:${msg.oacSessionId}`,
    To: `oac-bridge:${msg.oacSessionId}`,
    SessionKey: sessionKey,
    AccountId: account.accountId,
    OriginatingChannel: CHANNEL_ID,
    OriginatingTo: `oac-bridge:${msg.oacSessionId}`,
    ChatType: "direct",
    SenderName: msg.senderName,
    SenderId: msg.oacSessionId,
    Provider: CHANNEL_ID,
    Surface: CHANNEL_ID,
    ConversationLabel: msg.senderName || msg.oacSessionId,
    Timestamp: Date.now(),
    CommandAuthorized: msg.commandAuthorized,
  });
}
