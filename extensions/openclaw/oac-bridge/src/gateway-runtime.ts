import type { IncomingMessage, ServerResponse } from "node:http";
import type { OpenClawConfig } from "openclaw/plugin-sdk/account-resolution";
import { waitUntilAbort } from "openclaw/plugin-sdk/channel-lifecycle";
import { registerPluginHttpRoute } from "openclaw/plugin-sdk/webhook-ingress";
import { resolveAccount } from "./accounts.js";
import { dispatchOacBridgeInboundTurn } from "./inbound-turn.js";
import type { ResolvedOacBridgeAccount } from "./types.js";

const CHANNEL_ID = "oac-bridge";

type GatewayLog = {
  info?: (message: string) => void;
  warn?: (message: string) => void;
  error?: (message: string) => void;
};

const activeRouteUnregisters = new Map<string, () => void>();

async function readBody(req: IncomingMessage): Promise<string> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    const MAX_BYTES = 256 * 1024;
    let totalBytes = 0;

    req.on("data", (chunk: Buffer) => {
      totalBytes += chunk.length;
      if (totalBytes > MAX_BYTES) {
        req.destroy();
        reject(new Error("Request body too large"));
        return;
      }
      chunks.push(chunk);
    });
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf-8")));
    req.on("error", reject);

    setTimeout(() => reject(new Error("Body read timeout")), 10_000);
  });
}

function respondJson(res: ServerResponse, statusCode: number, body: Record<string, unknown>) {
  res.writeHead(statusCode, { "Content-Type": "application/json" });
  res.end(JSON.stringify(body));
}

function validateToken(provided: string, expected: string): boolean {
  if (!expected) return true;
  if (!provided) return false;
  if (provided.length !== expected.length) return false;
  let mismatch = 0;
  for (let i = 0; i < provided.length; i++) {
    mismatch |= provided.charCodeAt(i) ^ expected.charCodeAt(i);
  }
  return mismatch === 0;
}

function extractBearerToken(req: IncomingMessage): string {
  const auth = req.headers.authorization ?? "";
  if (typeof auth !== "string") return "";
  const match = auth.match(/^Bearer\s+(.+)$/i);
  return match?.[1]?.trim() ?? "";
}

function createOacWebhookHandler(params: { account: ResolvedOacBridgeAccount; log?: GatewayLog }) {
  const { account, log } = params;

  return async (req: IncomingMessage, res: ServerResponse) => {
    if (req.method !== "POST") {
      respondJson(res, 405, { error: "Method not allowed" });
      return;
    }

    const token = extractBearerToken(req);
    if (!validateToken(token, account.token)) {
      log?.warn?.("OAC Bridge: invalid token");
      respondJson(res, 401, { error: "Invalid token" });
      return;
    }

    let body: string;
    try {
      body = await readBody(req);
    } catch (err) {
      log?.error?.(`OAC Bridge: failed to read body: ${err}`);
      respondJson(res, 400, { error: "Invalid request body" });
      return;
    }

    let payload: {
      oac_session_id?: string;
      text?: string;
      sender_name?: string;
    };
    try {
      payload = JSON.parse(body);
    } catch {
      respondJson(res, 400, { error: "Invalid JSON" });
      return;
    }

    const oacSessionId = payload.oac_session_id;
    const text = payload.text;
    if (!oacSessionId || !text) {
      respondJson(res, 400, { error: "Missing required fields: oac_session_id, text" });
      return;
    }

    log?.info?.(`OAC Bridge: inbound from session ${oacSessionId}: ${text.slice(0, 100)}`);

    respondJson(res, 200, { status: "accepted" });

    try {
      await dispatchOacBridgeInboundTurn({
        account,
        msg: {
          body: text,
          oacSessionId,
          senderName: payload.sender_name ?? "OAC User",
          commandAuthorized: true,
        },
        log: {
          info: (...args) => log?.info?.(String(args[0] ?? "")),
          warn: (...args) => log?.warn?.(String(args[0] ?? "")),
          error: (...args) => log?.error?.(String(args[0] ?? "")),
        },
      });
    } catch (err) {
      log?.error?.(`OAC Bridge: inbound dispatch failed: ${err}`);
    }
  };
}

export function validateOacBridgeAccountStartup(params: {
  account: ResolvedOacBridgeAccount;
  accountId: string;
  log?: GatewayLog;
}): { ok: boolean } {
  const { account, accountId, log } = params;

  if (!account.enabled) {
    log?.info?.(`OAC Bridge account ${accountId} is disabled, skipping`);
    return { ok: false };
  }
  if (!account.callbackUrl) {
    log?.warn?.(`OAC Bridge account ${accountId}: callbackUrl is not configured`);
    return { ok: false };
  }
  return { ok: true };
}

export function registerOacBridgeWebhookRoute(params: {
  account: ResolvedOacBridgeAccount;
  accountId: string;
  log?: GatewayLog;
}): () => void {
  const { account, accountId, log } = params;
  const routeKey = `${accountId}:${account.webhookPath}`;

  const prevUnregister = activeRouteUnregisters.get(routeKey);
  if (prevUnregister) {
    log?.info?.(`OAC Bridge: deregistering stale route: ${account.webhookPath}`);
    prevUnregister();
    activeRouteUnregisters.delete(routeKey);
  }

  const handler = createOacWebhookHandler({ account, log });
  const unregister = registerPluginHttpRoute({
    path: account.webhookPath,
    auth: "plugin",
    pluginId: CHANNEL_ID,
    accountId: account.accountId,
    log: (msg: string) => log?.info?.(msg),
    handler,
  });
  activeRouteUnregisters.set(routeKey, unregister);

  return () => {
    unregister();
    activeRouteUnregisters.delete(routeKey);
  };
}

export type OacBridgeGatewayContext = {
  cfg: OpenClawConfig;
  accountId: string;
  abortSignal: AbortSignal;
  log?: GatewayLog;
};

export async function startOacBridgeGatewayAccount(ctx: OacBridgeGatewayContext): Promise<unknown> {
  const { cfg, accountId, log, abortSignal } = ctx;
  const account = resolveAccount(cfg, accountId);

  if (!validateOacBridgeAccountStartup({ account, accountId, log }).ok) {
    return waitUntilAbort(abortSignal);
  }

  log?.info?.(`Starting OAC Bridge channel (account: ${accountId}, path: ${account.webhookPath})`);
  const unregister = registerOacBridgeWebhookRoute({ account, accountId, log });
  log?.info?.(`Registered HTTP route: ${account.webhookPath} for OAC Bridge`);

  return waitUntilAbort(abortSignal, () => {
    log?.info?.(`Stopping OAC Bridge channel (account: ${accountId})`);
    unregister();
  });
}
