import { Type } from "@sinclair/typebox";

const ListScheduledTasksSchema = Type.Object(
  {
    include_disabled: Type.Optional(
      Type.Boolean({
        description: "Include disabled tasks (default: false).",
      }),
    ),
  },
  { additionalProperties: false },
);

export function createListScheduledTasksTool() {
  return {
    name: "list_scheduled_tasks",
    label: "List Scheduled Tasks",
    description:
      "List active cron/scheduled tasks. Returns Markdown. " +
      "Use when the user asks about tasks they assigned, reminders, or recurring schedules.",
    parameters: ListScheduledTasksSchema,
    execute: async (_toolCallId: string, rawParams: Record<string, unknown>) => {
      const includeDisabled = rawParams.include_disabled === true;

      let store: { jobs?: unknown[] } | null = null;
      try {
        const { loadCronStore, resolveCronStorePath } =
          await import("openclaw/plugin-sdk/config-runtime");
        const storePath = resolveCronStorePath();
        store = await loadCronStore(storePath);
      } catch {
        return {
          content: [
            {
              type: "text" as const,
              text: "Scheduled tasks unavailable: cron store could not be loaded.",
            },
          ],
        };
      }

      if (!store || !Array.isArray(store.jobs) || store.jobs.length === 0) {
        return { content: [{ type: "text" as const, text: "No scheduled tasks found." }] };
      }

      const lines: string[] = ["# Scheduled Tasks\n"];

      for (const job of store.jobs as Record<string, unknown>[]) {
        const enabled = job.enabled !== false;
        if (!includeDisabled && !enabled) continue;

        const name = (job.name as string) || "Unnamed";
        const schedule = (job.schedule as Record<string, unknown>) || {};
        const expr = (schedule.expr as string) || "";
        const tz = (schedule.tz as string) || "";
        const payload = (job.payload as Record<string, unknown>) || {};
        const message = (payload.message as string) || (payload.text as string) || "";
        const state = (job.state as Record<string, unknown>) || {};
        const lastStatus = (state.lastRunStatus as string) || "unknown";
        const lastError = (state.lastError as string) || "";

        const statusIcon = enabled ? "✅" : "⏸️";
        lines.push(`${statusIcon} **${name}**`);
        lines.push(`- Schedule: \`${expr}\` (${tz || "system"})`);
        if (message) {
          lines.push(`- Message: ${message}`);
        }
        lines.push(`- Last run: ${lastStatus}${lastError ? ` — ${lastError}` : ""}`);
        lines.push("");
      }

      const markdown = lines.length > 1 ? lines.join("\n") : "No scheduled tasks found.";

      return { content: [{ type: "text" as const, text: markdown }] };
    },
  };
}
