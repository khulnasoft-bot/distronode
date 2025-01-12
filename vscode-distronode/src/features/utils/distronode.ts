import * as glob from "glob";
import * as path from "path";
import * as fs from "fs";
import * as yaml from "yaml";
import { minimatch } from "minimatch";
import {
  DistronodeFileTypes,
  PlaybookKeywords,
  StandardRolePaths,
} from "../../definitions/constants";

import { IDistronodeFileType } from "../../interfaces/lightspeed";

export function getDistronodeFileType(
  filePath: string,
  documentContent: string,
): IDistronodeFileType {
  let parsedDistronodeDocument;
  for (const pattern in DistronodeFileTypes) {
    if (Object.prototype.hasOwnProperty.call(DistronodeFileTypes, pattern)) {
      if (minimatch(filePath, pattern)) {
        return DistronodeFileTypes[pattern];
      }
    }
  }
  try {
    parsedDistronodeDocument = yaml.parse(documentContent, {
      keepSourceTokens: true,
    });
  } catch (err) {
    console.log(err);
    return "other";
  }
  if (!parsedDistronodeDocument || parsedDistronodeDocument.length === 0) {
    return "other";
  }
  const lastObject = parsedDistronodeDocument[parsedDistronodeDocument.length - 1];
  if (typeof lastObject !== "object") {
    return "other";
  }
  const objectKeys = Object.keys(lastObject);
  for (const keyword of objectKeys) {
    if (PlaybookKeywords.includes(keyword)) {
      return "playbook";
    }
  }

  return "other";
}

export function getCustomRolePaths(workspacePath?: string): string[] {
  const rolePaths: string[] = [];

  if (workspacePath) {
    const pattern = path.join(workspacePath, "**/roles");
    const options = {
      ignore: ["**/node_modules/**", "**/.git/**"],
      absolute: true,
    };
    const workspaceRolePaths = glob.sync(pattern, options);
    rolePaths.push(...workspaceRolePaths);
  }

  return rolePaths;
}

export function getCommonRoles(): string[] {
  const rolePaths: string[] = [];
  const expandedPaths = StandardRolePaths.map((p) =>
    path.join(path.parse(p).root, path.normalize(p).slice(1)),
  );
  const standardRolePaths = expandedPaths.filter(
    (p) => fs.existsSync(p) && fs.statSync(p).isDirectory(),
  );
  rolePaths.push(...standardRolePaths);

  return rolePaths;
}
