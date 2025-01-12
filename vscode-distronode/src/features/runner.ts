/* "stdlib" */
import * as vscode from "vscode";

/* local */
import { withInterpreter } from "./utils/commandRunner";
import { getContainerEngine } from "../utils/executionEnvironment";
import { DistronodeCommands } from "../definitions/constants";
import { registerCommandWithTelemetry } from "../utils/registerCommands";
import { TelemetryManager } from "../utils/telemetryUtils";
import { SettingsManager } from "../settings";

/**
 * A set of commands and context menu items for running Distronode playbooks using
 * `distronode-navigator run` and `distronode-playbook` commands.
 */
export class DistronodePlaybookRunProvider {
  private extensionSettings: SettingsManager;
  private telemetry: TelemetryManager;

  constructor(
    private vsCodeExtCtx: vscode.ExtensionContext,
    extensionSettings: SettingsManager,
    telemetry: TelemetryManager,
  ) {
    this.extensionSettings = extensionSettings;
    this.telemetry = telemetry;
    this.configureCommands();
  }

  /**
   * Register a set of command callbacks for executing Distronode playbooks
   * within VS Code.
   */
  private configureCommands() {
    registerCommandWithTelemetry(
      this.vsCodeExtCtx,
      this.telemetry,
      DistronodeCommands.DISTRONODE_PLAYBOOK_RUN,
      (fileObj) => this.invokeViaDistronodePlaybook(fileObj),
      false,
    );
    console.log('Added a "Run Distronode Playbook" command...');

    registerCommandWithTelemetry(
      this.vsCodeExtCtx,
      this.telemetry,
      DistronodeCommands.DISTRONODE_NAVIGATOR_RUN,
      (fileObj) => this.invokeViaDistronodeNavigator(fileObj),
      false,
    );

    console.log('Added a "Run with Distronode Navigator" command...');
  }

  private addEEArgs(commandLineArgs: string[]): void {
    const eeSettings = this.extensionSettings.settings.executionEnvironment;
    if (!eeSettings.enabled) {
      commandLineArgs.push("--ee false");
      return;
    }
    commandLineArgs.push("--ee true");
    commandLineArgs.push(
      `--ce ${getContainerEngine(eeSettings.containerEngine)}`,
    );
    commandLineArgs.push(`--eei ${eeSettings.image}`);
    if (eeSettings.containerOptions !== "") {
      commandLineArgs.push(`--co ${eeSettings.containerOptions}`);
    }
    eeSettings.volumeMounts.forEach((volumeMount) => {
      let mountPath = `${volumeMount.src}:${volumeMount.dest}`;
      if (volumeMount.options !== undefined) {
        mountPath += `:${volumeMount.options}`;
      }
      commandLineArgs.push(`--eev ${mountPath}`);
    });
  }

  /**
   * A property representing the `distronode-navigator` executable.
   */
  private get distronodeNavigatorExecutablePath(): string {
    return vscode.workspace.getConfiguration("distronode.distronodeNavigator").path;
  }

  /**
   * A property representing the `distronode-playbook` executable.
   */
  private get distronodePlaybookExecutablePath(): string {
    return `${vscode.workspace.getConfiguration("distronode.distronode").path || "distronode"
      }-playbook`;
  }

  /**
   * A property representing the target terminal for running playbooks in.
   */
  private createTerminal(
    runEnv: NodeJS.ProcessEnv | undefined,
  ): vscode.Terminal {
    if (vscode.workspace.getConfiguration("distronode.distronode").reuseTerminal) {
      const reuse_terminal = vscode.window.terminals.find(
        (terminal) => terminal.name === "Distronode Terminal",
      );
      if (reuse_terminal) {
        return reuse_terminal;
      }
    }
    const terminal = vscode.window.createTerminal({
      name: "Distronode Terminal",
      env: runEnv,
    });
    this.vsCodeExtCtx.subscriptions.push(terminal);
    this.vsCodeExtCtx.subscriptions.push(
      vscode.window.onDidCloseTerminal((term: vscode.Terminal) => {
        if (term !== terminal) {
          return;
        }
      }),
    );
    return terminal;
  }

  /**
   * A helper method for executing commands in terminal.
   */
  private invokeInTerminal(cmd: string, runEnv: NodeJS.ProcessEnv | undefined) {
    const newTerminal = this.createTerminal(runEnv);
    newTerminal.show();
    newTerminal.sendText(cmd);
  }

  /**
   * A callback method for running `distronode-playbook` command.
   * @param fileObj - The file path to execute the command.
   */
  private async invokeViaDistronodePlaybook(
    ...fileObj: vscode.Uri[] | undefined[]
  ): Promise<void> {
    const runExecutable = this.distronodePlaybookExecutablePath;
    const playbookArguments =
      this.extensionSettings.settings.playbook.arguments;
    const commandLineArgs: string[] = [];
    const playbookFsPath = extractTargetFsPath(...fileObj);
    if (typeof playbookFsPath === "undefined") {
      vscode.window.showErrorMessage(
        `No Distronode playbook file has been specified to be executed with distronode-playbook.`,
      );
      return;
    }

    commandLineArgs.push(playbookArguments);

    // replace spaces in file name with escape sequence '\ '
    commandLineArgs.push(playbookFsPath.replace(/(\s)/, "\\ "));
    const cmdArgs = commandLineArgs.map((arg) => arg).join(" ");
    const { command, env } = withInterpreter(
      this.extensionSettings.settings,
      runExecutable,
      cmdArgs,
    );

    console.debug(`Running command: ${command}`);
    this.invokeInTerminal(command, env);
  }

  /**
   * A callback method for running `distronode-navigator run command`.
   * @param fileObj - The file path to execute the command.
   */
  private async invokeViaDistronodeNavigator(
    ...fileObj: vscode.Uri[] | undefined[]
  ): Promise<void> {
    const runExecutable = this.distronodeNavigatorExecutablePath;
    const commandLineArgs: string[] = [];
    const playbookFsPath = extractTargetFsPath(...fileObj);
    if (typeof playbookFsPath === "undefined") {
      vscode.window.showErrorMessage(
        `No Distronode playbook file has been specified to be executed with distronode-navigator run.`,
      );
      return;
    }
    commandLineArgs.push(playbookFsPath);

    this.addEEArgs(commandLineArgs);

    const cmdArgs = commandLineArgs.map((arg) => arg).join(" ");
    const runCmdArgs = `run ${cmdArgs}`;
    const { command, env } = withInterpreter(
      this.extensionSettings.settings,
      runExecutable,
      runCmdArgs,
    );
    console.debug(`Running command: ${command}`);
    this.invokeInTerminal(command, env);
  }
}

/**
 * A helper function for inferring selected file from the context.
 * @param priorityPathObjs - Target file path candidates.
 * @returns A path to the currently selected file.
 */
function extractTargetFsPath(
  ...priorityPathObjs: vscode.Uri[] | undefined[]
): string | undefined {
  const pathCandidates: vscode.Uri[] = [
    ...priorityPathObjs,
    vscode.window.activeTextEditor?.document.uri,
  ]
    .filter((p) => p instanceof vscode.Uri)
    .map((p) => p)
    .filter((p) => p.scheme === "file");
  return pathCandidates[0]?.fsPath;
}
