/* eslint-disable  @typescript-eslint/no-explicit-any */
import { MarkdownString, workspace } from "vscode";
import * as os from "os";
import * as path from "path";

export function formatDistronodeMetaData(distronodeMetaData: any) {
  let mdString = "";
  let distronodePresent = true;
  let distronodeLintPresent = true;
  let eeEnabled = false;

  const WARNING_COLOR = "#FFEF4A";
  const WARNING_STYLE = `style="color:${WARNING_COLOR};"`;

  // check if distronode is missing
  if (Object.keys(distronodeMetaData["distronode information"]).length === 0) {
    distronodePresent = false;
    mdString += "#### $(close) Distronode not found in the environment\n";

    // if python exists
    if (Object.keys(distronodeMetaData["python information"]).length !== 0) {
      const obj = distronodeMetaData["python information"];
      mdString += `Python version used: \`${obj["version"]}\` from \`${obj["location"]}\``;
    }

    const markdown = new MarkdownString(mdString, true);
    markdown.supportHtml = true;
    markdown.isTrusted = true;

    return {
      metaData: distronodeMetaData,
      markdown,
      distronodePresent,
      distronodeLintPresent,
    };
  }

  // check if ee is enabled or not
  if (distronodeMetaData["execution environment information"]) {
    eeEnabled = true;
  }

  // check is distronode-lint is missing
  if (Object.keys(distronodeMetaData["distronode-lint information"]).length === 0) {
    distronodeLintPresent = false;
  }

  mdString += eeEnabled
    ? `### Distronode meta data (in Execution Environment)\n`
    : `### Distronode meta data\n`;
  mdString += `\n<hr>\n`;
  mdString += `<hr>\n`;
  mdString += `<hr>\n`;

  // check if distronode-lint is enabled or not
  const lintEnabled = workspace
    .getConfiguration("distronode.validation.lint")
    .get("enabled");

  Object.keys(distronodeMetaData).forEach((mainKey) => {
    if (Object.keys(distronodeMetaData[mainKey]).length === 0) {
      return;
    }
    // put a marker stating distronode-lint setting is disabled
    if (mainKey === "distronode-lint information" && !lintEnabled) {
      mdString += `\n**${mainKey}:** `;
      mdString += `*<span ${WARNING_STYLE}>(disabled)*\n`;
    } else {
      mdString += `\n**${mainKey}:** \n`;
    }

    const valueObj = distronodeMetaData[mainKey];
    Object.keys(valueObj).forEach((key) => {
      if (key === "upgrade status") {
        mdString += ` <span ${WARNING_STYLE}>${valueObj[key]}`;
        return;
      }
      mdString += `\n   - ${key}: `;
      const value = valueObj[key];
      if (typeof value === "object") {
        value.forEach((val: any, index: any) => {
          if (val && val !== "None") {
            if (key.includes("path")) {
              mdString += `\n       ${
                index + 1
              }. <a href='${val}'>${getTildePath(val)}</a>`;
            } else {
              mdString += `\n       ${index + 1}. ${getTildePath(val)}`;
            }
          }
          if (index === value.length - 1) {
            mdString += `\n`;
          }
        });
      } else {
        if (key.includes("path")) {
          mdString += `<a href='${value}'>${getTildePath(value)}</a>`;
        } else if (key.includes("version")) {
          const versionInfo = value.split(/\r?\n/); // first part of versionInfo has the version no., the second part has message (if any)
          mdString += `\`${versionInfo[0]}\`\n`;
          if (versionInfo[1]) {
            mdString += `*<span style="color:${WARNING_COLOR};">${versionInfo[1]}*\n`;
          }
        } else if (key.includes("location")) {
          mdString += `${getTildePath(value)}\n`;
        } else {
          mdString += `${value}\n`;
        }
      }
    });
    mdString += `\n<hr>\n`;
    mdString += `<hr>\n`;
    mdString += `<hr>\n`;
  });

  // markdown conversion
  const markdown = new MarkdownString(mdString, true);
  markdown.supportHtml = true;
  markdown.isTrusted = true;

  if (!distronodeLintPresent) {
    markdown.appendMarkdown(
      `\n<p><span ${WARNING_STYLE}>$(warning) Warning(s):</p></h5>`,
    );
    markdown.appendMarkdown(`Distronode lint is missing in the environment`);
  }

  return {
    metaData: distronodeMetaData,
    markdown,
    distronodePresent,
    distronodeLintPresent,
    eeEnabled,
  };
}

export function getTildePath(absolutePath: string) {
  if (process.platform === "win32") {
    return path.win32.resolve(absolutePath);
  }
  const home = os.homedir();
  const dirPath = path.posix.resolve(absolutePath);

  if (dirPath === home) {
    return "~";
  }
  const homeWithTrailingSlash = `${home}/`;

  if (dirPath.startsWith(homeWithTrailingSlash)) {
    return dirPath.replace(homeWithTrailingSlash, "~/");
  }

  return dirPath;
}
