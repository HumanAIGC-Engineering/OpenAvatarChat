import fs from "node:fs";
import path from "node:path";
import { Type } from "@sinclair/typebox";

const GetAgentProfileSchema = Type.Object(
  {
    sections: Type.Optional(
      Type.Array(Type.String(), {
        description: 'Which sections to include: "identity", "soul", "user". Default: all.',
      }),
    ),
  },
  { additionalProperties: false },
);

const SECTION_FILES: Record<string, { file: string; heading: string }> = {
  identity: { file: "IDENTITY.md", heading: "## Identity" },
  soul: { file: "SOUL.md", heading: "## Personality" },
  user: { file: "USER.md", heading: "## User Preferences" },
};

function readWorkspaceFile(workspaceDir: string, filename: string): string {
  const filePath = path.join(workspaceDir, filename);
  try {
    if (fs.existsSync(filePath)) {
      return fs.readFileSync(filePath, "utf-8").trim();
    }
  } catch {
    // File not readable — skip silently
  }
  return "";
}

export function createGetAgentProfileTool(options: { workspaceDir?: string }) {
  const { workspaceDir } = options;

  return {
    name: "get_agent_profile",
    label: "Get Agent Profile",
    description:
      "Read agent identity, personality, and user preferences from workspace files " +
      "(IDENTITY.md, SOUL.md, USER.md). Returns Markdown. " +
      "Use when unsure about the agent's name, role, user's preferred name, or other profile details.",
    parameters: GetAgentProfileSchema,
    execute: async (_toolCallId: string, rawParams: Record<string, unknown>) => {
      if (!workspaceDir) {
        return {
          content: [
            {
              type: "text" as const,
              text: "Agent profile unavailable: no workspace directory configured.",
            },
          ],
        };
      }

      const requestedSections = Array.isArray(rawParams.sections)
        ? (rawParams.sections as string[])
        : Object.keys(SECTION_FILES);

      const parts: string[] = ["# Agent Profile\n"];

      for (const key of requestedSections) {
        const def = SECTION_FILES[key];
        if (!def) continue;
        const content = readWorkspaceFile(workspaceDir, def.file);
        if (content) {
          parts.push(`${def.heading}\n\n${content}\n`);
        }
      }

      const markdown = parts.length > 1 ? parts.join("\n") : "No profile files found in workspace.";

      return { content: [{ type: "text" as const, text: markdown }] };
    },
  };
}
