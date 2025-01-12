/* eslint-disable @typescript-eslint/no-namespace */

import { IDistronodeFileTypes } from "../interfaces/lightspeed";

export namespace DistronodeCommands {
  export const DISTRONODE_VAULT = "extension.distronode.vault";
  export const DISTRONODE_INVENTORY_RESYNC = "extension.resync-distronode-inventory";
  export const DISTRONODE_PLAYBOOK_RUN = "extension.distronode-playbook.run";
  export const DISTRONODE_NAVIGATOR_RUN = "extension.distronode-navigator.run";
  export const DISTRONODE_PYTHON_SET_INTERPRETER =
    "distronode.python.set.interpreter";
}

export const DistronodeFileTypes: IDistronodeFileTypes = {
  "**/playbooks/*.{yml,yaml}": "playbook",
  "**/*playbook*.{yml,yaml}": "playbook",
  "**/roles/**/tasks/**/*.{yml,yaml}": "tasks_in_role",
  "**/tasks/**/*.{yaml,yml}": "tasks",
};

export const PlaybookKeywords = [
  "hosts",
  "tasks",
  "vars_files",
  "roles",
  "pre_tasks",
  "post_tasks",
];

export const StandardRolePaths = [
  "~/.distronode/roles",
  "/usr/share/distronode/roles",
  "/etc/distronode/roles",
];

export const IncludeVarValidTaskName = [
  "include_vars",
  "distronode.builtin.include_vars",
  "distronode.legacy.include_vars",
];

/* Slightly lower than CloudFront's timeout which is 30s. */
export const DISTRONODE_LIGHTSPEED_API_TIMEOUT = 28000;

export const DISTRONODE_CREATOR_VERSION_MIN = "24.10.1";

export const DISTRONODE_CREATOR_COLLECTION_VERSION_MIN = "24.7.1";

export const DISTRONODE_CREATOR_EE_VERSION_MIN = "24.12.1";

export const DevfileImages = {
  Upstream: "ghcr.io/distronode/distronode-workspace-env-reference:latest",
};

export const DevcontainerImages = {
  Upstream: "ghcr.io/distronode/community-distronode-dev-tools:latest",
  Downstream:
    "registry.redhat.io/distronode-automation-platform-25/distronode-dev-tools-rhel8:latest",
};

export const DevcontainerRecommendedExtensions = {
  RECOMMENDED_EXTENSIONS: ["redhat.distronode", "redhat.vscode-redhat-account"],
};
