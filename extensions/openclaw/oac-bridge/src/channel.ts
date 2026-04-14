/**
 * OAC Bridge Channel Plugin.
 *
 * Minimal channel that lets OpenAvatarChat act as an IM for OpenClaw.
 * OAC sends messages via HTTP webhook; OC replies via HTTP callback.
 * Security is "open" by default (OAC is a trusted local system).
 */

import type { OpenClawConfig } from "openclaw/plugin-sdk/account-resolution";
import { waitUntilAbort } from "openclaw/plugin-sdk/channel-lifecycle";
import { createChatChannelPlugin } from "openclaw/plugin-sdk/core";
import { createEmptyChannelDirectoryAdapter } from "openclaw/plugin-sdk/directory-runtime";
import { DEFAULT_ACCOUNT_ID } from "openclaw/plugin-sdk/setup";
import { listAccountIds, resolveAccount } from "./accounts.js";
import { startOacBridgeGatewayAccount, type OacBridgeGatewayContext } from "./gateway-runtime.js";
import type { ResolvedOacBridgeAccount } from "./types.js";

const CHANNEL_ID = "oac-bridge";

function resolveOutboundAccount(
  cfg: OpenClawConfig,
  accountId?: string | null,
): ResolvedOacBridgeAccount {
  return resolveAccount(cfg ?? {}, accountId);
}

async function sendTextToOac(params: {
  cfg: OpenClawConfig;
  to: string;
  text: string;
  accountId?: string | null;
}): Promise<{ channel: string; messageId: string; chatId: string }> {
  const account = resolveOutboundAccount(params.cfg, params.accountId);
  if (!account.callbackUrl) {
    throw new Error("OAC Bridge: callbackUrl not configured");
  }

  const resp = await fetch(account.callbackUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(account.token ? { Authorization: `Bearer ${account.token}` } : {}),
    },
    body: JSON.stringify({
      oac_session_id: params.to,
      text: params.text,
      timestamp: Date.now(),
    }),
  });

  if (!resp.ok) {
    throw new Error(`OAC callback failed: ${resp.status} ${resp.statusText}`);
  }

  return {
    channel: CHANNEL_ID,
    messageId: `oac-${Date.now()}`,
    chatId: params.to,
  };
}

export function createOacBridgePlugin() {
  return createChatChannelPlugin({
    base: {
      id: CHANNEL_ID,
      meta: {
        id: CHANNEL_ID,
        label: "OpenAvatarChat",
        selectionLabel: "OpenAvatarChat (Webhook)",
        detailLabel: "OpenAvatarChat (Webhook)",
        docsPath: "/channels/oac-bridge",
        blurb: "Connect OpenClaw to OpenAvatarChat digital human interface",
        order: 95,
      },
      capabilities: {
        chatTypes: ["direct" as const],
        media: false,
        threads: false,
        reactions: false,
        edit: false,
        unsend: false,
        reply: false,
        effects: false,
        blockStreaming: false,
      },
      reload: { configPrefixes: [`channels.${CHANNEL_ID}`] },
      config: {
        listAccountIds,
        resolveAccount,
        defaultAccountId: () => DEFAULT_ACCOUNT_ID,
      },
      setup: {
        resolveAccount,
        inspectAccount(cfg: OpenClawConfig) {
          const section = (cfg.channels as Record<string, unknown>)?.["oac-bridge"] as
            | Record<string, unknown>
            | undefined;
          return {
            enabled: Boolean(section?.callbackUrl),
            configured: Boolean(section?.callbackUrl),
            tokenStatus: section?.token ? "available" : "missing",
          };
        },
      },
      directory: createEmptyChannelDirectoryAdapter(),
      messaging: {
        normalizeTarget: (target: string) => target.trim() || undefined,
        targetResolver: {
          looksLikeId: (id: string) => Boolean(id?.trim()),
          hint: "<oac_session_id>",
        },
      },
      gateway: {
        startAccount: async (ctx: OacBridgeGatewayContext) => {
          return startOacBridgeGatewayAccount(ctx);
        },
        stopAccount: async (ctx: OacBridgeGatewayContext) => {
          ctx.log?.info?.(`OAC Bridge account ${ctx.accountId} stopped`);
        },
      },
      agentPrompt: {
        messageToolHints: () => [
          "",
          "### OpenAvatarChat Channel",
          "Messages on this channel come from the OpenAvatarChat digital human interface.",
          "Respond naturally in the user's language. Keep responses concise for voice delivery.",
        ],
      },
    },
    security: {
      resolveDmPolicy: () => ({
        policy: "open",
        allowFrom: [],
      }),
      collectWarnings: () => [],
    },
    outbound: {
      deliveryMode: "gateway" as const,
      textChunkLimit: 4096,
      sendText: async (ctx: {
        cfg: OpenClawConfig;
        to: string;
        text: string;
        accountId?: string | null;
      }) => {
        return sendTextToOac(ctx);
      },
      sendMedia: async () => {
        throw new Error("OAC Bridge does not support media sending");
      },
    },
  });
}

export const oacBridgePlugin = createOacBridgePlugin();
