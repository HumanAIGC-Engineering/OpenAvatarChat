import { DEFAULT_ACCOUNT_ID, type OpenClawConfig } from "openclaw/plugin-sdk/account-resolution";
import type { ResolvedOacBridgeAccount } from "./types.js";

const DEFAULT_WEBHOOK_PATH = "/webhook/oac-bridge";

type OacBridgeChannelConfig = {
  callbackUrl?: string;
  token?: string;
  webhookPath?: string;
  enabled?: boolean;
};

function getChannelConfig(cfg: OpenClawConfig): OacBridgeChannelConfig | undefined {
  return cfg?.channels?.["oac-bridge"];
}

export function listAccountIds(cfg: OpenClawConfig): string[] {
  const channelCfg = getChannelConfig(cfg);
  if (!channelCfg) return [];
  if (channelCfg.callbackUrl || channelCfg.token) return [DEFAULT_ACCOUNT_ID];
  return [];
}

export function resolveAccount(
  cfg: OpenClawConfig,
  accountId?: string | null,
): ResolvedOacBridgeAccount {
  const channelCfg = getChannelConfig(cfg) ?? {};
  const id = accountId || DEFAULT_ACCOUNT_ID;

  return {
    accountId: id,
    enabled: channelCfg.enabled ?? true,
    callbackUrl: channelCfg.callbackUrl ?? process.env.OAC_CALLBACK_URL ?? "",
    token: channelCfg.token ?? process.env.OAC_BRIDGE_TOKEN ?? "",
    webhookPath: channelCfg.webhookPath ?? DEFAULT_WEBHOOK_PATH,
    dmPolicy: "open",
  };
}
