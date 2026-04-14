import type { OpenClawConfig } from "openclaw/plugin-sdk/core";
import { createOperatorApprovalsGatewayClient } from "openclaw/plugin-sdk/gateway-runtime";
import { parseExecApprovalCommandText } from "openclaw/plugin-sdk/infra-runtime";
import { buildOacBridgeInboundContext, type OacInboundMessage } from "./inbound-context.js";
import { getOacBridgeRuntime } from "./runtime.js";
import { buildOacBridgeSessionKey } from "./session-key.js";
import type { ResolvedOacBridgeAccount } from "./types.js";

const CHANNEL_ID = "oac-bridge";

type OacBridgeLog = {
  info?: (...args: unknown[]) => void;
  warn?: (...args: unknown[]) => void;
  error?: (...args: unknown[]) => void;
};

function resolveOacBridgeInboundRoute(params: {
  cfg: OpenClawConfig;
  account: ResolvedOacBridgeAccount;
  oacSessionId: string;
}) {
  const rt = getOacBridgeRuntime();
  const route = rt.channel.routing.resolveAgentRoute({
    cfg: params.cfg,
    channel: CHANNEL_ID,
    accountId: params.account.accountId,
    peer: {
      kind: "direct",
      id: params.oacSessionId,
    },
  });
  return {
    rt,
    route,
    sessionKey: buildOacBridgeSessionKey({
      agentId: route.agentId,
      accountId: params.account.accountId,
      oacSessionId: params.oacSessionId,
      identityLinks: params.cfg.session?.identityLinks,
    }),
  };
}

async function deliverOacBridgeReply(params: {
  account: ResolvedOacBridgeAccount;
  oacSessionId: string;
  payload: { text?: string; body?: string };
}): Promise<void> {
  const text = params.payload.text ?? params.payload.body;
  if (!text) return;

  const callbackUrl = params.account.callbackUrl;
  if (!callbackUrl) return;

  const resp = await fetch(callbackUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(params.account.token ? { Authorization: `Bearer ${params.account.token}` } : {}),
    },
    body: JSON.stringify({
      oac_session_id: params.oacSessionId,
      text,
      timestamp: Date.now(),
    }),
  });

  if (!resp.ok) {
    throw new Error(`OAC callback failed: ${resp.status} ${resp.statusText}`);
  }
}

async function resolveOacBridgeExecApproval(params: {
  cfg: OpenClawConfig;
  approvalId: string;
  decision: "allow-once" | "allow-always" | "deny";
  oacSessionId: string;
  log?: OacBridgeLog;
}): Promise<void> {
  let readySettled = false;
  let resolveReady!: () => void;
  let rejectReady!: (err: unknown) => void;
  const ready = new Promise<void>((resolve, reject) => {
    resolveReady = resolve;
    rejectReady = reject;
  });
  const markReady = () => {
    if (readySettled) return;
    readySettled = true;
    resolveReady();
  };
  const failReady = (err: unknown) => {
    if (readySettled) return;
    readySettled = true;
    rejectReady(err);
  };

  const gatewayClient = await createOperatorApprovalsGatewayClient({
    config: params.cfg,
    clientDisplayName: `OAC Bridge approval (session ${params.oacSessionId})`,
    onHelloOk: () => markReady(),
    onConnectError: (err) => failReady(err),
    onClose: (_code, reason) => failReady(new Error(`gateway closed: ${reason}`)),
  });

  try {
    gatewayClient.start();
    await ready;
    const method = params.approvalId.startsWith("plugin:")
      ? ("plugin.approval.resolve" as const)
      : ("exec.approval.resolve" as const);
    await gatewayClient.request(method, {
      id: params.approvalId,
      decision: params.decision,
    });
    params.log?.info?.(
      `OAC Bridge: exec approval resolved: ${params.approvalId} → ${params.decision}`,
    );
  } finally {
    await gatewayClient.stopAndWait().catch(() => gatewayClient.stop());
  }
}

export async function dispatchOacBridgeInboundTurn(params: {
  account: ResolvedOacBridgeAccount;
  msg: OacInboundMessage;
  log?: OacBridgeLog;
}): Promise<null> {
  const rt = getOacBridgeRuntime();
  const currentCfg = await rt.config.loadConfig();

  const approvalCmd = parseExecApprovalCommandText(params.msg.body);
  if (approvalCmd) {
    params.log?.info?.(
      `OAC Bridge: intercepted /approve command: ${approvalCmd.approvalId} ${approvalCmd.decision}`,
    );
    try {
      await resolveOacBridgeExecApproval({
        cfg: currentCfg,
        approvalId: approvalCmd.approvalId,
        decision: approvalCmd.decision,
        oacSessionId: params.msg.oacSessionId,
        log: params.log,
      });
    } catch (err) {
      params.log?.error?.(`OAC Bridge: exec approval resolution failed: ${err}`);
    }
    return null;
  }

  const resolved = resolveOacBridgeInboundRoute({
    cfg: currentCfg,
    account: params.account,
    oacSessionId: params.msg.oacSessionId,
  });
  const msgCtx = buildOacBridgeInboundContext({
    finalizeInboundContext: resolved.rt.channel.reply.finalizeInboundContext,
    account: params.account,
    msg: params.msg,
    sessionKey: resolved.sessionKey,
  });

  await resolved.rt.channel.reply.dispatchReplyWithBufferedBlockDispatcher({
    ctx: msgCtx,
    cfg: currentCfg,
    dispatcherOptions: {
      deliver: async (payload: { text?: string; body?: string }) => {
        await deliverOacBridgeReply({
          account: params.account,
          oacSessionId: params.msg.oacSessionId,
          payload,
        });
      },
      onReplyStart: () => {
        params.log?.info?.(`Agent reply started for OAC session ${params.msg.oacSessionId}`);
      },
    },
  });

  return null;
}
