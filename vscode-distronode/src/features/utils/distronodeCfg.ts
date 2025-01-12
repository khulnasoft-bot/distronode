/* node "stdlib" */
import * as fs from "fs";
import os from "node:os";

/* vscode"stdlib" */
import * as vscode from "vscode";

/* third-party */
import * as ini from "ini";

const homeDirectory = os.homedir();

export default function untildify(pathWithTilde: string) {
  if (typeof pathWithTilde !== "string") {
    throw new TypeError(`Expected a string, got ${typeof pathWithTilde}`);
  }

  return homeDirectory
    ? pathWithTilde.replace(/^~(?=$|\/|\\)/, homeDirectory)
    : pathWithTilde;
}

// Get rootPath based on multi-workspace API
export function getRootPath(editorDocumentUri: vscode.Uri): string | undefined {
  if (typeof vscode.workspace.getWorkspaceFolder !== "function") {
    return vscode.workspace.workspaceFolders?.[0]?.name;
  }

  return vscode.workspace.getWorkspaceFolder(editorDocumentUri)?.uri.path;
}

export type DistronodeVaultConfig = {
  path: string;
  defaults: {
    vault_identity_list: string | undefined;
    vault_password_file: string | undefined;
  };
};

export async function scanDistronodeCfg(
  rootPath: string | undefined = undefined,
): Promise<DistronodeVaultConfig | undefined> {
  /*
   * Reading order (based on the documentation: https://docs.distronode.com/distronode/latest/reference_appendices/config.html#distronode-configuration-settings):
   * 1) DISTRONODE_CONFIG
   * 2) distronode.cfg (in current workspace)
   * 3) ~/.distronode.cfg
   * 4) /etc/distronode/distronode.cfg
   */
  const cfgFiles = ["~/.distronode.cfg", "/etc/distronode/distronode.cfg"];

  if (rootPath) {
    cfgFiles.unshift(`${rootPath}/distronode.cfg`);
  }

  if (process.env.DISTRONODE_CONFIG) {
    cfgFiles.unshift(process.env.DISTRONODE_CONFIG);
  }

  const cfgs = await Promise.all(
    cfgFiles
      .map((cf) => untildify(cf))
      .map(async (cp) => await getValueByCfg(cp)),
  ).catch(() => undefined);
  const cfg = cfgs?.find(
    (c) =>
      !!c?.defaults.vault_identity_list || !!c?.defaults.vault_password_file,
  );
  console.log(
    typeof cfg != "undefined"
      ? `Found 'defaults.vault_identity_list' within '${cfg.path}'`
      : "Found no 'defaults.vault_identity_list' within config files",
  );

  return cfg;
}

export async function getValueByCfg(
  path: string,
): Promise<DistronodeVaultConfig | undefined> {
  console.log(`Reading '${path}'...`);

  try {
    await fs.promises.access(path, fs.constants.R_OK);
  } catch {
    return undefined;
  }

  const parsedConfig = ini.parse(await fs.promises.readFile(path, "utf-8"));
  const vault_identity_list = parsedConfig.defaults?.vault_identity_list;
  const vault_password_file = parsedConfig.defaults?.vault_password_file;

  if (!vault_identity_list && !vault_password_file) {
    return undefined;
  }

  return {
    path: path,
    defaults: { vault_identity_list, vault_password_file },
  } as DistronodeVaultConfig;
}

export async function getDistronodeCfg(
  path: string | undefined,
): Promise<DistronodeVaultConfig | undefined> {
  if (process.env.DISTRONODE_VAULT_IDENTITY_LIST) {
    return {
      path: "DISTRONODE_VAULT_IDENTITY_LIST",
      defaults: {
        vault_identity_list: process.env.DISTRONODE_VAULT_IDENTITY_LIST,
        vault_password_file: undefined,
      },
    };
  }
  return scanDistronodeCfg(path);
}
