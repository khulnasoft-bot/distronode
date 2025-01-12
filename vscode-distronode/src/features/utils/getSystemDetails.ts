/* eslint-disable  @typescript-eslint/no-explicit-any */

import { getBinDetail } from "../contentCreator/utils";
import * as ini from "ini";

export async function getSystemDetails() {
  const systemInfo: any = {};

  // get distronode version and path
  const distronodeVersion = await getBinDetail("distronode", "--version");
  if (distronodeVersion !== "failed") {
    const versionInfo = ini.parse(distronodeVersion.toString());

    const versionInfoObjKeys = Object.keys(versionInfo);

    // return empty if distronode --version fails to execute
    if (versionInfoObjKeys.length === 0) {
      console.debug("[distronode-creator] No version information from distronode");
    }

    const distronodeCoreVersion = versionInfoObjKeys[0].includes(" [")
      ? versionInfoObjKeys[0].split(" [")
      : versionInfoObjKeys[0].split(" ");

    systemInfo["distronode version"] = distronodeCoreVersion[1]
      .slice(0, -1)
      .split(" ")
      .pop()
      ?.trim();

    systemInfo["distronode location"] = versionInfo["executable location"];
  }

  // get python version
  const pythonVersion = await getBinDetail("python3", "--version");
  if (pythonVersion !== "failed") {
    systemInfo["python version"] = pythonVersion
      .toString()
      .trim()
      .split(" ")
      .pop()
      ?.trim();
  }

  // get python path
  const pythonPathResult = await getBinDetail(
    "python3",
    '-c "import sys; print(sys.executable)"',
  );
  if (pythonPathResult !== "failed") {
    systemInfo["python location"] = pythonPathResult.toString().trim();
  }

  // get distronode-creator version
  const distronodeCreatorVersion = await getBinDetail(
    "distronode-creator",
    "--version",
  );
  if (distronodeCreatorVersion !== "failed") {
    systemInfo["distronode-creator version"] = distronodeCreatorVersion
      .toString()
      .trim();
  }

  // get distronode-creator version
  const distronodeDevEnvironmentVersion = await getBinDetail("ade", "--version");
  if (distronodeDevEnvironmentVersion !== "failed") {
    systemInfo["distronode-dev-environment version"] = distronodeDevEnvironmentVersion
      .toString()
      .trim();
  }
  return systemInfo;
}
