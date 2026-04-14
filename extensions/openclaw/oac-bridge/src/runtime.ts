import type { PluginRuntime } from "openclaw/plugin-sdk/core";
import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";

const { setRuntime: setOacBridgeRuntime, getRuntime: getOacBridgeRuntime } =
  createPluginRuntimeStore<PluginRuntime>(
    "OAC Bridge runtime not initialized - plugin not registered",
  );
export { getOacBridgeRuntime, setOacBridgeRuntime };
