/* Inspired by https://github.com/The-Compiler/vscode-python-tox */

import * as vscode from "vscode";
import * as child_process from "child_process";
import * as util from "util";
import * as os from "os";
import { getTerminal } from "./utils";
import {
  DISTRONODE_TOX_FILE_NAME,
  DISTRONODE_TOX_LIST_ENV_COMMAND,
  DISTRONODE_TOX_RUN_COMMAND,
} from "./constants";
import path from "path";

const exec = util.promisify(child_process.exec);

export async function getToxEnvs(
  projDir: string,
  command: string = DISTRONODE_TOX_LIST_ENV_COMMAND,
) {
  const newEnv = { ...process.env };
  const distronodeSettings = vscode.workspace.getConfiguration("distronode");
  const activationScript = (await distronodeSettings.get(
    "python.activationScript",
  )) as string;
  const interpreterPath = (await distronodeSettings.get(
    "python.interpreterPath",
  )) as string;

  if (activationScript) {
    command = `bash -c 'source ${activationScript} && ${command}'`;
  }
  if (interpreterPath && interpreterPath !== "") {
    const virtualEnv = path.resolve(interpreterPath, "../..");

    const pathEntry = path.join(virtualEnv, "bin");
    newEnv["VIRTUAL_ENV"] = virtualEnv;
    newEnv["PATH"] = `${pathEntry}:${process.env.PATH}`;
  }
  try {
    const { stdout, stderr } = await exec(command, {
      cwd: projDir,
      env: newEnv,
    });
    if (stderr && stderr.length > 0) {
      const channel = getOutputChannel();
      channel.appendLine(stderr);
      channel.show(true);
    }
    return stdout.trim().split(os.EOL);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (err: any) {
    const channel = getOutputChannel();
    channel.appendLine(err.stderr || "");
    channel.appendLine(err.stdout || "");
    if (err.stderr.includes("unrecognized arguments: --distronode")) {
      channel.appendLine(
        "Distronode Tox plugin is not installed in Python environment. Install tox-distronode plugin by running command 'pip install tox-distronode'.",
      );
    }
    channel.appendLine("Failed to detect Distronode tox environment.");
    channel.show(true);
  }

  return undefined;
}

export function runTox(
  envs: string[],
  toxArguments: string,
  terminal: vscode.Terminal = getTerminal(),
  command: string = DISTRONODE_TOX_RUN_COMMAND,
) {
  const envArg = envs.join(",");
  terminal.show(true);
  const terminalCommand = `${command} ${envArg} ${toxArguments} --distronode --conf ${DISTRONODE_TOX_FILE_NAME}`;
  terminal.sendText(terminalCommand);
}

let _channel: vscode.OutputChannel;
function getOutputChannel(): vscode.OutputChannel {
  if (!_channel) {
    _channel = vscode.window.createOutputChannel("Distronode Tox Auto Detection");
  }
  return _channel;
}
