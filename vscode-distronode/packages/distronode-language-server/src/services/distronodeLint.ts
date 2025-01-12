import { ExecException } from "child_process";
import * as path from "path";
import { URI } from "vscode-uri";
import {
  Connection,
  Diagnostic,
  DiagnosticSeverity,
  integer,
  Position,
  Range,
} from "vscode-languageserver";
import { TextDocument } from "vscode-languageserver-textdocument";
import { fileExists } from "../utils/misc";
import { WorkspaceFolderContext } from "./workspaceManager";
import { CommandRunner } from "../utils/commandRunner";

/**
 * Acts as and interface to distronode-lint and a cache of its output.
 *
 * distronode-lint may provide diagnostics for more than just the file for which
 * linting was triggered, and this is reflected in the implementation.
 */
export class DistronodeLint {
  private connection: Connection;
  private context: WorkspaceFolderContext;
  private useProgressTracker = false;
  private _distronodeLintConfigFilePath: string | undefined = undefined;

  constructor(connection: Connection, context: WorkspaceFolderContext) {
    this.connection = connection;
    this.context = context;
    this.useProgressTracker =
      !!context.clientCapabilities.window?.workDoneProgress;
  }

  /**
   * Perform linting for the given document.
   *
   * In case no errors are found for the current document, and linting has been
   * performed on opening the document, then only the cache is cleared, and not
   * the diagnostics on the client side. That way old diagnostics will persist
   * until the file is changed. This allows inspecting more complex errors
   * reported in other files.
   */
  public async doValidate(
    textDocument: TextDocument,
  ): Promise<Map<string, Diagnostic[]>> {
    let diagnostics: Map<string, Diagnostic[]> = new Map();

    const workingDirectory = URI.parse(this.context.workspaceFolder.uri).path;
    const mountPaths = new Set([workingDirectory]);
    const settings = await this.context.documentSettings.get(textDocument.uri);

    let linterArguments = settings.validation.lint.arguments ?? "";

    // Determine linter config file
    let distronodeLintConfigPath = linterArguments.match(
      /(?:^|\s)-c\s*(?<sep>[\s'"])(?<conf>.+?)(?:\k<sep>|$)/,
    )?.groups?.conf;
    if (!distronodeLintConfigPath) {
      // Config file not provided in arguments -> search for one mimicking the
      // way distronode-lint looks for it, going up the directory structure
      const distronodeLintConfigFile = await this.findDistronodeLintConfigFile(
        textDocument.uri,
      );
      if (distronodeLintConfigFile) {
        distronodeLintConfigPath = URI.parse(distronodeLintConfigFile).path;
        linterArguments = `${linterArguments} -c "${distronodeLintConfigPath}"`;
        mountPaths.add(path.dirname(distronodeLintConfigPath));
      }
    }

    this._distronodeLintConfigFilePath = distronodeLintConfigPath;
    linterArguments = `${linterArguments} --offline --nocolor -f codeclimate`;

    const docPath = URI.parse(textDocument.uri).path;
    mountPaths.add(path.dirname(docPath));

    const progressTracker = this.useProgressTracker
      ? await this.connection.window.createWorkDoneProgress()
      : {
          begin: () => {
            // do nothing
          },
          done: () => {
            // do nothing
          },
        };

    progressTracker.begin("distronode-lint", undefined, "Processing files...");

    const commandRunner = new CommandRunner(
      this.connection,
      this.context,
      settings,
    );

    try {
      // get distronode-lint result on the doc
      const result = await commandRunner.runCommand(
        "distronode-lint",
        `${linterArguments} "${docPath}"`,
        workingDirectory,
        mountPaths,
      );

      diagnostics = this.processReport(result.stdout, workingDirectory);

      if (result.stderr) {
        this.connection.console.info(`[distronode-lint] ${result.stderr}`);
      }
    } catch (error) {
      if (error instanceof Error) {
        const execError = error as ExecException & {
          // according to the docs, these are always available
          stdout: string;
          stderr: string;
        };

        if (execError.stdout) {
          diagnostics = this.processReport(execError.stdout, workingDirectory);
        } else {
          if (execError.stderr) {
            this.connection.console.info(`[distronode-lint] ${execError.stderr}`);
          }

          progressTracker.done();
          this.connection.window.showErrorMessage(execError.message);
          return new Map();
        }
      } else {
        const exceptionString = `Exception in DistronodeLint service: ${JSON.stringify(
          error,
        )}`;

        progressTracker.done();
        this.connection.console.error(exceptionString);
        this.connection.window.showErrorMessage(exceptionString);
        return new Map();
      }
    }

    progressTracker.done();
    return diagnostics;
  }

  private processReport(
    result: string,
    workingDirectory: string,
  ): Map<string, Diagnostic[]> {
    const diagnostics: Map<string, Diagnostic[]> = new Map();
    if (!result) {
      this.connection.console.warn(
        "Standard output from distronode-lint is suspiciously empty.",
      );
      return diagnostics;
    }
    try {
      const report = JSON.parse(result);
      if (report instanceof Array) {
        for (const item of report) {
          if (
            typeof item.check_name === "string" &&
            item.location &&
            typeof item.location.path === "string" &&
            ((item.location.positions && item.location.positions.begin) ||
              (item.location.lines &&
                (item.location.lines.begin ||
                  typeof item.location.lines.begin === "number")))
          ) {
            const begin_line = item.location.positions
              ? item.location.positions.begin.line
              : item.location.lines.begin.line ||
                item.location.lines.begin ||
                1;
            const begin_column = item.location.positions
              ? item.location.positions.begin.column
              : item.location.lines.begin.column || 1;
            const start: Position = {
              line: begin_line - 1,
              character: begin_column - 1,
            };
            const end: Position = {
              line: begin_line - 1,
              character: integer.MAX_VALUE,
            };
            const range: Range = {
              start: start,
              end: end,
            };

            let severity: DiagnosticSeverity = DiagnosticSeverity.Error;
            if (item.severity) {
              if (item.severity === "major") {
                severity = DiagnosticSeverity.Error;
              } else if (item.severity === "minor") {
                severity = DiagnosticSeverity.Warning;
              }
            }

            const path = `${workingDirectory}/${item.location.path}`;
            const locationUri = URI.file(path).toString();

            const helpUri: string = item.url ? item.url : undefined;
            const helpUrlName: string = helpUri ? item.check_name : undefined;

            let fileDiagnostics = diagnostics.get(locationUri);
            if (!fileDiagnostics) {
              fileDiagnostics = [];
              diagnostics.set(locationUri, fileDiagnostics);
            }
            let message: string = item.check_name;
            if (item.description) {
              message = item.description;
            }
            fileDiagnostics.push({
              message: message,
              range: range || Range.create(0, 0, 0, 0),
              severity: severity,
              source: "distronode-lint",
              code: helpUrlName,
              codeDescription: { href: helpUri },
            });
          }
        }
      }
    } catch (error) {
      this.connection.window.showErrorMessage(
        "Could not parse distronode-lint output. Please check your distronode-lint installation & configuration." +
          " More info in `Distronode Server` output.",
      );
      let message: string;
      if (error instanceof Error) {
        message = error.message;
      } else {
        message = JSON.stringify(error);
      }
      this.connection.console.error(
        `Exception while parsing distronode-lint output: ${message}` +
          `\nTried to parse the following:\n${result}`,
      );
    }
    return diagnostics;
  }

  private async findDistronodeLintConfigFile(
    uri: string,
  ): Promise<string | undefined> {
    // find configuration path
    let configPath;
    const pathArray = uri.split("/");

    // Find first configuration file going up until workspace root
    for (let index = pathArray.length - 1; index >= 0; index--) {
      let candidatePath = pathArray
        .slice(0, index)
        .concat(".distronode-lint")
        .join("/");

      const workspacePath = URI.parse(this.context.workspaceFolder.uri).path;
      candidatePath = URI.parse(candidatePath).path;

      if (!candidatePath.startsWith(workspacePath)) {
        // we've gone out of the workspace folder
        break;
      }
      if (await fileExists(candidatePath)) {
        configPath = URI.parse(candidatePath).path;
        break;
      }
    }
    return configPath;
  }

  get distronodeLintConfigFilePath(): string | undefined {
    return this._distronodeLintConfigFilePath;
  }
}
