import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { defineChannelPluginEntry } from "openclaw/plugin-sdk/core";
import { oacBridgePlugin } from "./src/channel.js";
import { createGetAgentProfileTool } from "./src/profile-tool.js";
import { setOacBridgeRuntime } from "./src/runtime.js";
import { createListScheduledTasksTool } from "./src/tasks-tool.js";

export { oacBridgePlugin } from "./src/channel.js";
export { setOacBridgeRuntime } from "./src/runtime.js";

function resolveWorkspaceDir(ctxWorkspaceDir?: string): string | undefined {
  if (ctxWorkspaceDir) {
    return ctxWorkspaceDir;
  }
  const fallback = path.join(os.homedir(), ".openclaw", "workspace");
  if (fs.existsSync(fallback)) {
    return fallback;
  }
  return undefined;
}

export default defineChannelPluginEntry({
  id: "oac-bridge",
  name: "OAC Bridge",
  description: "OpenAvatarChat bridge: agent profile/task tools + OAC IM channel",
  plugin: oacBridgePlugin,
  setRuntime: setOacBridgeRuntime,
  registerFull(api) {
    api.registerTool(
      (ctx) =>
        createGetAgentProfileTool({
          workspaceDir: resolveWorkspaceDir(ctx.workspaceDir),
        }),
      { names: ["get_agent_profile"] },
    );
    api.registerTool(() => createListScheduledTasksTool(), { names: ["list_scheduled_tasks"] });
  },
});
