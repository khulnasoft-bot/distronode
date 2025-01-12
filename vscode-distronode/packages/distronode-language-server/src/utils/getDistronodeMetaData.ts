import { Connection } from "vscode-languageserver";
import { URI } from "vscode-uri";
import { WorkspaceFolderContext } from "../services/workspaceManager";
import { CommandRunner } from "./commandRunner";
import * as child_process from "child_process";

let context: WorkspaceFolderContext;
let connection: Connection | undefined;

export interface distronodeMetaDataEntryType {
  [name: string]:
    | {
        [name: string]: string | string[] | undefined | object[];
      }
    | string
    | string[]
    | object[]
    | undefined;
}

export interface distronodeMetaDataType {
  "distronode information"?: distronodeMetaDataEntryType;
  "python information"?: distronodeMetaDataEntryType;
  "distronode-lint information"?: distronodeMetaDataEntryType;
  "execution environment information"?: distronodeMetaDataEntryType | undefined;
}

export async function getDistronodeMetaData(
  contextLocal: WorkspaceFolderContext,
  connectionLocal: Connection | undefined,
): Promise<distronodeMetaDataType> {
  context = contextLocal;
  connection = connectionLocal;

  const distronodeMetaData: distronodeMetaDataType = {
    "distronode information": await getDistronodeInfo(),
    "python information": await getPythonInfo(),
    "distronode-lint information": await getDistronodeLintInfo(),
  };

  const settings = await context.documentSettings.get(
    context.workspaceFolder.uri,
  );

  if (settings.executionEnvironment.enabled) {
    distronodeMetaData["execution environment information"] =
      await getExecutionEnvironmentInfo();
  }

  return distronodeMetaData;
}

export async function getResultsThroughCommandRunner(cmd: string, arg: string) {
  const settings = await context.documentSettings.get(
    context.workspaceFolder.uri,
  );
  const commandRunner = new CommandRunner(connection, context, settings);
  const workingDirectory = URI.parse(context.workspaceFolder.uri).path;
  const mountPaths = new Set([workingDirectory]);

  let result;
  try {
    result = await commandRunner.runCommand(
      cmd,
      arg,
      workingDirectory,
      mountPaths,
    );

    if (result.stderr) {
      console.log(
        `cmd '${cmd} ${arg}' has the following error/warning: ${result.stderr}`,
      );
      return result;
    }
  } catch (error) {
    let errorMessage: string;
    if (error instanceof Error) {
      errorMessage = error.message;
    } else {
      errorMessage = String(error);
    }
    console.log(
      `cmd '${cmd} ${arg}' was not executed with the following error: ' ${errorMessage}`,
    );
    return undefined;
  }

  return result;
}

async function getDistronodeInfo() {
  const distronodeInfo: distronodeMetaDataEntryType = {};

  const distronodeVersionObj = (await context.distronodeConfig).distronode_meta_data;
  const distronodeVersionObjKeys = Object.keys(distronodeVersionObj);

  // return empty if distronode --version fails to execute
  if (distronodeVersionObjKeys.length === 0) {
    return distronodeInfo;
  }

  let distronodeCoreVersion: string[] = [];
  if (distronodeVersionObjKeys[0].includes(" [")) {
    distronodeCoreVersion = distronodeVersionObjKeys[0].split(" [");
  } else {
    distronodeCoreVersion = distronodeVersionObjKeys[0].split(" ");
  }
  distronodeInfo["core version"] = distronodeCoreVersion[1]
    ?.slice(0, -1)
    ?.split(" ")
    ?.pop()
    ?.trim();

  distronodeInfo["location"] = (await context.distronodeConfig).distronode_location;

  if ("config file" in distronodeVersionObj) {
    distronodeInfo["config file path"] = distronodeVersionObj[
      "config file"
    ] as string;
  }

  distronodeInfo["collections location"] = (
    await context.distronodeConfig
  ).collections_paths;

  distronodeInfo["modules location"] = (
    await context.distronodeConfig
  ).module_locations;

  distronodeInfo["default host list path"] = (
    await context.distronodeConfig
  ).default_host_list;

  return distronodeInfo;
}

async function getPythonInfo() {
  const pythonInfo: distronodeMetaDataEntryType = {};

  const pythonVersionResult = await getResultsThroughCommandRunner(
    "python3",
    "--version",
  );
  if (pythonVersionResult === undefined) {
    return pythonInfo;
  }

  pythonInfo["version"] = pythonVersionResult.stdout
    .trim()
    .split(" ")
    .pop()
    ?.trim();

  const pythonPathResult = await getResultsThroughCommandRunner(
    "python3",
    '-c "import sys; print(sys.executable)"',
  );
  pythonInfo["location"] = pythonPathResult?.stdout.trim();

  return pythonInfo;
}

async function getDistronodeLintInfo() {
  const distronodeLintInfo: distronodeMetaDataEntryType = {};

  const distronodeLintVersionResult = await getResultsThroughCommandRunner(
    "distronode-lint",
    "--version",
  );

  if (distronodeLintVersionResult === undefined) {
    return distronodeLintInfo;
  }

  const distronodeLintPathResult = await getResultsThroughCommandRunner(
    "command -v",
    "distronode-lint",
  );

  // distronode-lint version reports if a newer version of the distronode-lint is available or not
  // along with the current version itself
  // so the following lines of code are to segregate the two information into to keys
  const distronodeLintVersionStdout = distronodeLintVersionResult.stdout
    .trim()
    .split("\n");
  const distronodeLintVersion = distronodeLintVersionStdout[0];
  if (distronodeLintVersionStdout.length >= 2) {
    distronodeLintInfo["upgrade status"] = distronodeLintVersionStdout[1];
  } else {
    distronodeLintInfo["upgrade status"] = "nil";
  }

  distronodeLintInfo["version"] =
    distronodeLintVersion.split("using")[0]?.trim()?.split(" ")?.pop()?.trim() ||
    undefined;

  distronodeLintInfo["location"] =
    distronodeLintPathResult?.stdout.trim() || undefined;

  distronodeLintInfo["config file path"] =
    context.distronodeLint.distronodeLintConfigFilePath;

  return distronodeLintInfo;
}

async function getExecutionEnvironmentInfo() {
  const eeInfo: distronodeMetaDataEntryType = {};

  const basicDetails = (await context.executionEnvironment)
    .getBasicContainerAndImageDetails;

  eeInfo["container engine"] = String(basicDetails.containerEngine);
  eeInfo["container image"] = basicDetails.containerImage;
  eeInfo["container image ID"] = basicDetails.containerImageId;

  let eeServiceWorking = false;
  let inspectResult;
  try {
    inspectResult = JSON.parse(
      child_process
        .execSync(
          `${basicDetails.containerEngine} inspect --format='{{json .Config}}' ${basicDetails.containerImage}`,
          {
            encoding: "utf-8",
          },
        )
        .toString(),
    );
    eeServiceWorking = true;
  } catch (error) {
    eeServiceWorking = false;
    console.log(error);
  }

  if (eeServiceWorking) {
    eeInfo["env"] = inspectResult["Env"];
    eeInfo["working directory"] = inspectResult["WorkingDir"];
  }

  return eeInfo;
}
