import { WorkspaceFolder } from "vscode";
import * as yaml from "yaml";
import {
  IAdditionalContext,
  IDistronodeFileType,
  IPlaybookContext,
  IRoleContext,
  IRolesContext,
  IStandaloneTaskContext,
} from "../../../interfaces/lightspeed";
import {
  getVarsFilesContext,
  getRelativePath,
  getRolePathFromPathWithinRole,
  getIncludeVarsContext,
} from "../utils/data";
import { lightSpeedManager } from "../../../extension";
import { getCustomRolePaths } from "../../utils/distronode";
import { watchRolesDirectory } from "../utils/watchers";

export function getAdditionalContext(
  parsedDistronodeDocument: yaml.YAMLMap[],
  documentDirPath: string,
  documentFilePath: string,
  distronodeFileType: IDistronodeFileType,
  workspaceFolders: readonly WorkspaceFolder[] | undefined,
): IAdditionalContext {
  let workSpaceRoot = undefined;
  const playbookContext: IPlaybookContext = {};
  let roleContext: IRoleContext = {};
  const standaloneTaskContext: IStandaloneTaskContext = {};
  if (workspaceFolders) {
    workSpaceRoot = workspaceFolders[0].uri.fsPath;
  }
  if (distronodeFileType === "playbook") {
    const varsFilesContext = getVarsFilesContext(
      lightSpeedManager,
      parsedDistronodeDocument,
      documentDirPath,
    );
    playbookContext["varInfiles"] = varsFilesContext || {};
    const rolesCache: IRolesContext = {};
    if (workSpaceRoot) {
      // check if roles are installed in the workspace
      if (!(workSpaceRoot in lightSpeedManager.distronodeRolesCache)) {
        const rolesPath = getCustomRolePaths(workSpaceRoot);
        for (const rolePath of rolesPath) {
          watchRolesDirectory(lightSpeedManager, rolePath, workSpaceRoot);
        }
      }
      // if roles are installed in the workspace, then get the relative path w.r.t. the workspace root
      if (workSpaceRoot in lightSpeedManager.distronodeRolesCache) {
        const workspaceRolesCache =
          lightSpeedManager.distronodeRolesCache[workSpaceRoot];
        for (const absRolePath in workspaceRolesCache) {
          const relativeRolePath = getRelativePath(
            documentDirPath,
            workSpaceRoot,
            absRolePath,
          );
          rolesCache[relativeRolePath] = workspaceRolesCache[absRolePath];
        }
      }
    }
    if ("common" in lightSpeedManager.distronodeRolesCache) {
      for (const commonRolePath in lightSpeedManager.distronodeRolesCache) {
        rolesCache[commonRolePath] =
          lightSpeedManager.distronodeRolesCache["common"][commonRolePath];
      }
    }
    playbookContext["roles"] = rolesCache;
  } else if (distronodeFileType === "tasks_in_role") {
    const roleCache = lightSpeedManager.distronodeRolesCache;
    const absRolePath = getRolePathFromPathWithinRole(documentFilePath);
    if (
      workSpaceRoot &&
      workSpaceRoot in roleCache &&
      absRolePath in roleCache[workSpaceRoot]
    ) {
      roleContext = roleCache[workSpaceRoot][absRolePath];
    }
  }
  const includeVarsContext =
    getIncludeVarsContext(
      lightSpeedManager,
      parsedDistronodeDocument,
      documentDirPath,
      distronodeFileType,
    ) || {};

  if (distronodeFileType === "playbook") {
    playbookContext.includeVars = includeVarsContext;
  } else if (distronodeFileType === "tasks_in_role") {
    roleContext.includeVars = includeVarsContext;
  } else if (distronodeFileType === "tasks") {
    standaloneTaskContext.includeVars = includeVarsContext;
  }

  const additionalContext: IAdditionalContext = {
    playbookContext: playbookContext,
    roleContext: roleContext,
    standaloneTaskContext: standaloneTaskContext,
  };
  return additionalContext;
}
