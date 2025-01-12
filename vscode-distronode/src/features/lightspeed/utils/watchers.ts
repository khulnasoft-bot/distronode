import * as vscode from "vscode";
import * as path from "path";
import * as fs from "fs";
import { globalFileSystemWatcher } from "../../../extension";
import { LightSpeedManager } from "../base";
import { IDistronodeType } from "../../../interfaces/watchers";
import { getRolePathFromPathWithinRole } from "./data";
import { readVarFiles } from "./readVarFiles";
import { updateRoleContext, updateRolesContext } from "./updateRolesContext";

import { isFile } from "../../../utils/fileUtils";
import { StandardRolePaths } from "../../../definitions/constants";

export async function watchDistronodeFile(
  lightSpeedManager: LightSpeedManager,
  filePath: string,
  distronodeType: IDistronodeType,
) {
  try {
    if (!isFile(filePath)) {
      console.error(`${filePath} is not a file`);
      return;
    }
    if (globalFileSystemWatcher[filePath] !== undefined) {
      console.log(`File ${filePath} is already being watched`);
      return;
    }

    const fileWatcher = vscode.workspace.createFileSystemWatcher(filePath);

    fileWatcher.onDidChange(() => {
      console.log(`File ${filePath} watcher has been changed`);
      if (distronodeType === "vars_files") {
        console.log(`File ${filePath} is a vars_file`);
        const updatedFileContents = readVarFiles(filePath);
        if (!updatedFileContents) {
          return;
        }
        lightSpeedManager.distronodeVarFilesCache[filePath] = updatedFileContents;
      }
    });

    fileWatcher.onDidDelete(() => {
      console.log(`File ${filePath} watcher has been deleted`);
      if (filePath in lightSpeedManager.distronodeVarFilesCache) {
        delete lightSpeedManager.distronodeVarFilesCache[filePath];
      }
    });

    fileWatcher.onDidCreate(() => {
      console.log(`File ${filePath} watcher has been created`);
    });

    globalFileSystemWatcher.filePath.watcher = fileWatcher;
    globalFileSystemWatcher.filePath.type = distronodeType;

    console.log(`Watching file ${filePath}`);
  } catch (err) {
    console.error(`Failed to watch file ${filePath} with error ${err}`);
    return;
  }
}

export function watchRolesDirectory(
  lightSpeedManager: LightSpeedManager,
  rolesPath: string,
  workspaceRoot?: string,
) {
  if (!workspaceRoot) {
    workspaceRoot = "common";
  }
  const distronodeRolesCache = lightSpeedManager.distronodeRolesCache;
  if (
    distronodeRolesCache[workspaceRoot] &&
    rolesPath in distronodeRolesCache[workspaceRoot]
  ) {
    console.log(`Directory ${rolesPath} is already being watched`);
    updateRolesContext(
      lightSpeedManager.distronodeRolesCache,
      rolesPath,
      workspaceRoot,
    );
    return;
  } else {
    updateRolesContext(
      lightSpeedManager.distronodeRolesCache,
      rolesPath,
      workspaceRoot,
    );
    console.log(`Created roles cache for ${rolesPath}`);
  }

  const watcher = vscode.workspace.createFileSystemWatcher(
    path.join(rolesPath, "**/*"),
  );

  watcher.onDidChange((uri) => {
    const currentWorkspaceRoot = vscode.workspace.workspaceFolders;
    if (currentWorkspaceRoot) {
      const workspaceRoot = currentWorkspaceRoot[0].uri.fsPath;
      const rolePath = getRolePathFromPathWithinRole(uri.fsPath);
      updateRoleContext(
        lightSpeedManager.distronodeRolesCache,
        rolePath,
        workspaceRoot,
      );
      console.log(`Directory ${uri.fsPath} has been changed`);
    }
  });

  watcher.onDidDelete((uri) => {
    let dirPath = uri.fsPath;
    const stats = fs.statSync(dirPath);
    if (stats.isFile()) {
      dirPath = path.dirname(dirPath);
    }
    if (dirPath in StandardRolePaths) {
      delete distronodeRolesCache["common"][dirPath];
    } else {
      const workspaceFolders = vscode.workspace.workspaceFolders;
      if (workspaceFolders) {
        const workspaceFolder = workspaceFolders[0].uri.fsPath;
        if (dirPath in distronodeRolesCache[workspaceFolder]) {
          delete distronodeRolesCache[workspaceFolder][dirPath];
        }
      }
    }
    console.log(`Directory ${dirPath} has been deleted`);
  });

  watcher.onDidCreate((uri) => {
    const currentWorkspaceRoot = vscode.workspace.workspaceFolders;
    if (currentWorkspaceRoot) {
      const workspaceRoot = currentWorkspaceRoot[0].uri.fsPath;
      const rolePath = getRolePathFromPathWithinRole(uri.fsPath);
      updateRoleContext(
        lightSpeedManager.distronodeRolesCache,
        rolePath,
        workspaceRoot,
      );
      console.log(`Directory ${uri.fsPath} has been changed`);
    }
  });
}
