import { buildAgentSessionKey } from "openclaw/plugin-sdk/core";

const CHANNEL_ID = "oac-bridge";

/**
 * Build session key for OAC ↔ OC 1:1 mapping.
 * Each OAC session maps to exactly one OC session via oac_session_id.
 */
export function buildOacBridgeSessionKey(params: {
  agentId: string;
  accountId: string;
  oacSessionId: string;
  identityLinks?: Record<string, string[]>;
}): string {
  return buildAgentSessionKey({
    agentId: params.agentId,
    channel: CHANNEL_ID,
    accountId: params.accountId,
    peer: { kind: "direct", id: params.oacSessionId },
    dmScope: "per-account-channel-peer",
    identityLinks: params.identityLinks,
  });
}
