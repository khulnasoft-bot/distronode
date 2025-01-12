/* "stdlib" */
import * as vscode from "vscode";
import * as path from "path";
import { ExtensionContext, extensions, window, workspace } from "vscode";
import { toggleEncrypt } from "./features/vault";
import { DistronodeCommands } from "./definitions/constants";
import { LightSpeedCommands, UserAction } from "./definitions/lightspeed";
import {
  TelemetryErrorHandler,
  TelemetryOutputChannel,
  TelemetryManager,
} from "./utils/telemetryUtils";

/* third-party */
import {
  LanguageClient,
  LanguageClientOptions,
  NotificationType,
  ServerOptions,
  TransportKind,
  RevealOutputChannelOn,
} from "vscode-languageclient/node";

/* local */
import { SettingsManager } from "./settings";
import { DistronodePlaybookRunProvider } from "./features/runner";
import {
  getConflictingExtensions,
  showUninstallConflictsNotification,
} from "./extensionConflicts";
import { languageAssociation } from "./features/fileAssociation";
import { MetadataManager } from "./features/distronodeMetaData";
import { updateConfigurationChanges } from "./utils/settings";
import { registerCommandWithTelemetry } from "./utils/registerCommands";
import { LightSpeedManager } from "./features/lightspeed/base";
import {
  ignorePendingSuggestion,
  inlineSuggestionCommitHandler,
  inlineSuggestionReplaceMarker,
  inlineSuggestionHideHandler,
  inlineSuggestionTextDocumentChangeHandler,
  inlineSuggestionTriggerHandler,
  LightSpeedInlineSuggestionProvider,
  rejectPendingSuggestion,
  setDocumentChanged,
} from "./features/lightspeed/inlineSuggestions";
import { playbookExplanation } from "./features/lightspeed/playbookExplanation";
import { ContentMatchesWebview } from "./features/lightspeed/contentMatchesWebview";
import {
  setPythonInterpreter,
  setPythonInterpreterWithCommand,
} from "./features/utils/setPythonInterpreter";
import { PythonInterpreterManager } from "./features/pythonMetadata";
import { DistronodeToxController } from "./features/distronodeTox/controller";
import { DistronodeToxProvider } from "./features/distronodeTox/provider";
import { findProjectDir } from "./features/distronodeTox/utils";
import { QuickLinksWebviewViewProvider } from "./features/quickLinks/utils/quickLinksViewProvider";
import { LightspeedFeedbackWebviewViewProvider } from "./features/lightspeed/feedbackWebviewViewProvider";
import { LightspeedFeedbackWebviewProvider } from "./features/lightspeed/feedbackWebviewProvider";
import { DistronodeWelcomePage } from "./features/welcomePage";
import { CreateDistronodeCollection } from "./features/contentCreator/createDistronodeCollectionPage";
import { withInterpreter } from "./features/utils/commandRunner";
import { IFileSystemWatchers } from "./interfaces/watchers";
import { showPlaybookGenerationPage } from "./features/lightspeed/playbookGeneration";
import { showRoleGenerationPage } from "./features/lightspeed/roleGeneration";
import { ExecException, execSync } from "child_process";
import { CreateDistronodeProject } from "./features/contentCreator/createDistronodeProjectPage";
import { AddPlugin } from "./features/contentCreator/addPluginPage";
// import { LightspeedExplorerWebviewViewProvider } from "./features/lightspeed/explorerWebviewViewProvider";
import {
  LightspeedUser,
  AuthProviderType,
} from "./features/lightspeed/lightspeedUser";
import { PlaybookFeedbackEvent } from "./interfaces/lightspeed";
import { CreateDevfile } from "./features/contentCreator/createDevfilePage";
import { CreateSampleExecutionEnv } from "./features/contentCreator/createSampleExecutionEnvPage";
import { CreateDevcontainer } from "./features/contentCreator/createDevcontainerPage";

export let client: LanguageClient;
export let lightSpeedManager: LightSpeedManager;
export const globalFileSystemWatcher: IFileSystemWatchers = {};

const lsName = "Distronode Support";
let lsOutputChannel: vscode.OutputChannel;

export async function activate(context: ExtensionContext): Promise<void> {
  // dynamically associate "distronode" language to the yaml file
  await languageAssociation(context);

  // set correct python interpreter
  const workspaceFolders = workspace.workspaceFolders;
  if (workspaceFolders) {
    await setPythonInterpreter();
  }

  // Create Telemetry Service
  const telemetry = new TelemetryManager(context);
  await telemetry.initTelemetryService();

  await registerCommandWithTelemetry(
    context,
    telemetry,
    DistronodeCommands.DISTRONODE_VAULT,
    toggleEncrypt,
    true,
  );
  await registerCommandWithTelemetry(
    context,
    telemetry,
    DistronodeCommands.DISTRONODE_INVENTORY_RESYNC,
    resyncDistronodeInventory,
    true,
  );

  await registerCommandWithTelemetry(
    context,
    telemetry,
    DistronodeCommands.DISTRONODE_PYTHON_SET_INTERPRETER,
    setPythonInterpreterWithCommand,
    true,
  );

  await registerCommandWithTelemetry(
    context,
    telemetry,
    LightSpeedCommands.LIGHTSPEED_AUTH_REQUEST,
    lightspeedLogin,
    true,
  );

  // start the client and the server
  await startClient(context, telemetry);

  notifyAboutConflicts();

  // Initialize settings
  const extSettings = new SettingsManager();
  await extSettings.initialize();

  new DistronodePlaybookRunProvider(context, extSettings, telemetry);

  // handle metadata status bar
  const metaData = new MetadataManager(context, client, telemetry, extSettings);
  await metaData.updateDistronodeInfoInStatusbar();

  // handle python status bar
  const pythonInterpreterManager = new PythonInterpreterManager(
    context,
    client,
    telemetry,
    extSettings,
  );
  try {
    await pythonInterpreterManager.updatePythonInfoInStatusbar();
  } catch (error) {
    console.error(`Error updating python status bar: ${error}`);
  }

  /**
   * Handle "Distronode Lightspeed" in the extension
   */
  lightSpeedManager = new LightSpeedManager(
    context,
    client,
    extSettings,
    telemetry,
  );

  vscode.commands.executeCommand("setContext", "lightspeedConnectReady", true);

  context.subscriptions.push(
    vscode.commands.registerCommand(
      LightSpeedCommands.LIGHTSPEED_STATUS_BAR_CLICK,
      () =>
        lightSpeedManager.statusBarProvider.lightSpeedStatusBarClickHandler(),
    ),
  );

  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider(
      ContentMatchesWebview.viewType,
      lightSpeedManager.contentMatchesProvider,
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      LightSpeedCommands.LIGHTSPEED_FETCH_TRAINING_MATCHES,
      () => {
        lightSpeedManager.contentMatchesProvider.showContentMatches();
      },
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      LightSpeedCommands.LIGHTSPEED_CLEAR_TRAINING_MATCHES,
      () => {
        lightSpeedManager.contentMatchesProvider.clearContentMatches();
      },
    ),
  );

  const lightSpeedSuggestionProvider = new LightSpeedInlineSuggestionProvider();
  ["file", "untitled"].forEach((scheme) => {
    context.subscriptions.push(
      vscode.languages.registerInlineCompletionItemProvider(
        { scheme, language: "distronode" },
        lightSpeedSuggestionProvider,
      ),
    );
  });

  context.subscriptions.push(
    vscode.commands.registerTextEditorCommand(
      LightSpeedCommands.LIGHTSPEED_SUGGESTION_COMMIT,
      inlineSuggestionCommitHandler,
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerTextEditorCommand(
      LightSpeedCommands.LIGHTSPEED_SUGGESTION_HIDE,
      async (
        textEditor: vscode.TextEditor,
        edit: vscode.TextEditorEdit,
        userAction?: UserAction,
      ) => {
        await inlineSuggestionHideHandler(userAction);
      },
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerTextEditorCommand(
      LightSpeedCommands.LIGHTSPEED_SUGGESTION_TRIGGER,
      inlineSuggestionTriggerHandler,
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerTextEditorCommand(
      LightSpeedCommands.LIGHTSPEED_SUGGESTION_MARKER,
      (
        textEditor: vscode.TextEditor,
        edit: vscode.TextEditorEdit,
        position: vscode.Position,
      ) => inlineSuggestionReplaceMarker(position),
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerTextEditorCommand(
      LightSpeedCommands.LIGHTSPEED_PLAYBOOK_EXPLANATION,
      async () => {
        await playbookExplanation(context.extensionUri);
      },
    ),
  );

  // Listen for text selection changes
  context.subscriptions.push(
    vscode.window.onDidChangeTextEditorSelection(async () => {
      rejectPendingSuggestion();
    }),
  );

  // At window focus change, check if an inline suggestion is pending and ignore it if it exists.
  context.subscriptions.push(
    vscode.window.onDidChangeWindowState(async (state: vscode.WindowState) => {
      if (!state.focused) {
        ignorePendingSuggestion();
      }
    }),
  );

  // register distronode meta data in the statusbar tooltip (client-server)
  context.subscriptions.push(
    window.onDidChangeActiveTextEditor(
      async (editor: vscode.TextEditor | undefined) => {
        await updateDistronodeStatusBar(
          metaData,
          lightSpeedManager,
          pythonInterpreterManager,
        );
        if (!editor) {
          await ignorePendingSuggestion();
        }
        lightSpeedManager.lightspeedExplorerProvider.refreshWebView();
      },
    ),
  );
  context.subscriptions.push(
    workspace.onDidOpenTextDocument(async () => {
      await updateDistronodeStatusBar(
        metaData,
        lightSpeedManager,
        pythonInterpreterManager,
      );
      lightSpeedManager.lightspeedExplorerProvider.refreshWebView();
      metaData.sendDistronodeMetadataTelemetry();
    }),
  );
  context.subscriptions.push(
    workspace.onDidChangeTextDocument(
      (event: vscode.TextDocumentChangeEvent) => {
        if (
          event.document === vscode.window.activeTextEditor?.document &&
          event.contentChanges.length > 0 &&
          event.contentChanges[0].text[0] !== "\n"
        ) {
          setDocumentChanged(true);
        }
      },
    ),
  );
  context.subscriptions.push(
    workspace.onDidChangeTextDocument(
      (event: vscode.TextDocumentChangeEvent) => {
        if (
          event.document === vscode.window.activeTextEditor?.document &&
          event.contentChanges.length > 0 &&
          event.contentChanges[0].text[0] !== "\n"
        ) {
          setDocumentChanged(true);
        }
      },
    ),
  );

  context.subscriptions.push(
    workspace.onDidChangeConfiguration(async () => {
      await updateConfigurationChanges(
        metaData,
        pythonInterpreterManager,
        extSettings,
        lightSpeedManager,
      );
      await updateDistronodeStatusBar(
        metaData,
        lightSpeedManager,
        pythonInterpreterManager,
      );
      metaData.sendDistronodeMetadataTelemetry();
    }),
  );

  context.subscriptions.push(
    workspace.onDidChangeTextDocument((e: vscode.TextDocumentChangeEvent) => {
      inlineSuggestionTextDocumentChangeHandler(e);
    }),
  );

  context.subscriptions.push(
    workspace.onDidChangeTextDocument((e: vscode.TextDocumentChangeEvent) => {
      inlineSuggestionTextDocumentChangeHandler(e);
    }),
  );

  context.subscriptions.push(
    vscode.authentication.onDidChangeSessions(async (e) => {
      if (!LightspeedUser.isLightspeedUserAuthProviderType(e.provider.id)) {
        return;
      }
      await lightSpeedManager.lightspeedAuthenticatedUser.refreshLightspeedUser();
      if (!lightSpeedManager.lightspeedAuthenticatedUser.isAuthenticated()) {
        lightSpeedManager.currentModelValue = undefined;
      }
      if (lightSpeedManager.lightspeedExplorerProvider.webviewView) {
        lightSpeedManager.lightspeedExplorerProvider.refreshWebView();
      }
      lightSpeedManager.statusBarProvider.updateLightSpeedStatusbar();
    }),
  );

  const quickLinksHome = new QuickLinksWebviewViewProvider(
    context.extensionUri,
  );

  const quickLinksDisposable = window.registerWebviewViewProvider(
    QuickLinksWebviewViewProvider.viewType,
    quickLinksHome,
  );

  context.subscriptions.push(quickLinksDisposable);

  // handle lightSpeed feedback
  const lightspeedFeedbackProvider = new LightspeedFeedbackWebviewViewProvider(
    context.extensionUri,
  );

  // Register the Lightspeed provider for a Webview View
  const lightspeedFeedbackDisposable = window.registerWebviewViewProvider(
    LightspeedFeedbackWebviewViewProvider.viewType,
    lightspeedFeedbackProvider,
  );

  context.subscriptions.push(lightspeedFeedbackDisposable);

  // Register the Lightspeed provider for a Webview
  const lightspeedFeedbackCommand = vscode.commands.registerCommand(
    LightSpeedCommands.LIGHTSPEED_FEEDBACK,
    () => {
      LightspeedFeedbackWebviewProvider.render(context.extensionUri);
    },
  );

  context.subscriptions.push(lightspeedFeedbackCommand);

  // Register the Sign in with Red Hat command
  const lightspeedSignInWithRedHatCommand = vscode.commands.registerCommand(
    LightSpeedCommands.LIGHTSPEED_SIGN_IN_WITH_REDHAT,
    async () => {
      // NOTE: We can't gate this check on if this extension is active,
      // because it only activates on an authentication request.
      if (!vscode.extensions.getExtension("redhat.vscode-redhat-account")) {
        window.showErrorMessage(
          "You must install the Red Hat Authentication extension to sign in with Red Hat.",
        );
        return;
      }
      lightspeedLogin(AuthProviderType.rhsso);
    },
  );
  context.subscriptions.push(lightspeedSignInWithRedHatCommand);

  // Register the Sign in with Lightspeed command
  const lightspeedSignInWithLightspeedCommand = vscode.commands.registerCommand(
    LightSpeedCommands.LIGHTSPEED_SIGN_IN_WITH_LIGHTSPEED,
    () => {
      lightspeedLogin(AuthProviderType.lightspeed);
    },
  );
  context.subscriptions.push(lightspeedSignInWithLightspeedCommand);

  /**
   * Handle "Distronode Tox" in the extension
   */
  const distronodeToxController = new DistronodeToxController();
  context.subscriptions.push(await distronodeToxController.create());

  const workspaceTox = findProjectDir();

  if (workspaceTox) {
    const testProvider = new DistronodeToxProvider(workspaceTox);
    context.subscriptions.push(
      vscode.tasks.registerTaskProvider(
        DistronodeToxProvider.toxType,
        testProvider,
      ),
    );
  }

  /**
   * Handle "Distronode Creator" in the extension
   */

  // pip install distronode-creator
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.content-creator.install",
      async () => {
        const extSettings = new SettingsManager();
        await extSettings.initialize();

        const pythonInterpreter = extSettings.settings.interpreterPath;

        // specify the current python interpreter path in the pip installation
        const { command, env } = withInterpreter(
          extSettings.settings,
          `${pythonInterpreter} -m pip install distronode-creator`,
          "--no-input",
        );

        let terminal;
        if (
          vscode.workspace.getConfiguration("distronode.distronode").reuseTerminal
        ) {
          terminal = vscode.window.terminals.find(
            (terminal) => terminal.name === "Distronode Terminal",
          ) as vscode.Terminal;
        }
        terminal = vscode.window.createTerminal({
          name: "Distronode Terminal",
          env: env,
        });
        terminal.show();
        terminal.sendText(command);
      },
    ),
  );

  // open distronode extension workspace settings directly
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.extension-settings.open",
      async () => {
        await vscode.commands.executeCommand(
          "workbench.action.openWorkspaceSettings",
          "distronode",
        );
      },
    ),
  );

  // open distronode-python workspace settings directly
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.python-settings.open",
      async () => {
        await vscode.commands.executeCommand(
          "workbench.action.openWorkspaceSettings",
          "distronode.python",
        );
      },
    ),
  );

  // open distronode-content-creator menu
  context.subscriptions.push(
    vscode.commands.registerCommand("distronode.content-creator.menu", () => {
      DistronodeWelcomePage.render(context.extensionUri);
    }),
  );

  // open web-view for creating distronode collection
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.content-creator.create-distronode-collection",
      () => {
        CreateDistronodeCollection.render(context.extensionUri);
      },
    ),
  );

  // open web-view for creating distronode playbook project
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.content-creator.create-distronode-project",
      () => {
        CreateDistronodeProject.render(context.extensionUri);
      },
    ),
  );

  // open web-view for creating devfile
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.content-creator.create-devfile",
      () => {
        CreateDevfile.render(context.extensionUri);
      },
    ),
  );

  // open web-view for creating sample Execution Environment file
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.content-creator.create-sample-execution-env-file",
      () => {
        CreateSampleExecutionEnv.render(context.extensionUri);
      },
    ),
  );

  // open web-view for creating devcontainer
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.content-creator.create-devcontainer",
      () => {
        CreateDevcontainer.render(context.extensionUri);
      },
    ),
  );

  // open web-view for adding a plugin in an distronode collection
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.content-creator.add-plugin",
      () => {
        AddPlugin.render(context.extensionUri);
      },
    ),
  );

  // open distronode-creator create
  context.subscriptions.push(
    vscode.commands.registerCommand("distronode.content-creator.create", () => {
      window.showInformationMessage("This feature is coming soon. Stay tuned.");
    }),
  );

  // open distronode-creator sample
  context.subscriptions.push(
    vscode.commands.registerCommand("distronode.content-creator.sample", () => {
      window.showInformationMessage("This feature is coming soon. Stay tuned.");
    }),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      LightSpeedCommands.LIGHTSPEED_PLAYBOOK_GENERATION,
      async () => {
        await showPlaybookGenerationPage(context.extensionUri);
      },
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      LightSpeedCommands.LIGHTSPEED_ROLE_GENERATION,
      async () => {
        await showRoleGenerationPage(context.extensionUri);
      },
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.lightspeed.thumbsUpDown",
      async (param: PlaybookFeedbackEvent) => {
        if (param.explanationId) {
          lightSpeedManager.apiInstance.feedbackRequest(
            { playbookExplanationFeedback: param },
            true,
            true,
          );
        } else if (param.generationId) {
          lightSpeedManager.apiInstance.feedbackRequest(
            { playbookGenerationFeedback: param },
            true,
            true,
          );
        } else {
          lightSpeedManager.apiInstance.feedbackRequest(
            { playbookOutlineFeedback: param },
            true,
            true,
          );
        }
      },
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.lightspeed.enableExperimentalFeatures",
      () => {
        vscode.commands.executeCommand(
          "setContext",
          "redhat.distronode.lightspeedExperimentalEnabled",
          true,
        );
        lightSpeedManager.lightspeedExplorerProvider.lightspeedExperimentalEnabled =
          true;
        lightSpeedManager.lightspeedExplorerProvider.refreshWebView();
      },
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      LightSpeedCommands.LIGHTSPEED_OPEN_TRIAL_PAGE,
      () => {
        vscode.env.openExternal(
          vscode.Uri.parse(
            lightSpeedManager.settingsManager.settings.lightSpeedService.URL +
            "/trial",
          ),
        );
      },
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      LightSpeedCommands.LIGHTSPEED_REFRESH_EXPLORER_VIEW,
      async () => {
        await lightSpeedManager.lightspeedAuthenticatedUser.updateUserInformation();
        lightSpeedManager.lightspeedExplorerProvider.refreshWebView();
      },
    ),
  );

  // getting started walkthrough command
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.walkthrough.gettingStarted.setLanguage",
      () => {
        vscode.commands.executeCommand("runCommands", {
          commands: [
            "workbench.action.focusRightGroup",
            "workbench.action.editor.changeLanguageMode",
          ],
        });
      },
    ),
  );

  // install distronode development tools
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.install-distronode-dev-tools",
      async () => {
        const extSettings = new SettingsManager();
        await extSettings.initialize();

        const pythonInterpreter = extSettings.settings.interpreterPath;

        // specify the current python interpreter path in the pip installation
        const { command, env } = withInterpreter(
          extSettings.settings,
          `${pythonInterpreter} -m pip install distronode-dev-tools`,
          "--no-input",
        );

        const outputChannel = window.createOutputChannel(`Distronode Logs`);

        let commandOutput = "";
        let commandPassed = false;

        vscode.window.withProgress(
          {
            title: "Please wait...",
            location: vscode.ProgressLocation.Notification,
            cancellable: true,
          },
          async (_, token) => {
            // You code to process the progress

            token.onCancellationRequested(async () => {
              await vscode.window.showErrorMessage("Installation cancelled");
            });

            try {
              const result = execSync(command, {
                env: env,
              }).toString();
              commandOutput = result;
              outputChannel.append(commandOutput);
              commandPassed = true;
            } catch (error) {
              let errorMessage: string;
              if (error instanceof Error) {
                const execError = error as ExecException & {
                  // according to the docs, these are always available
                  stdout: string;
                  stderr: string;
                };

                errorMessage = execError.stdout
                  ? execError.stdout
                  : execError.stderr;
                errorMessage += execError.message;
              } else {
                errorMessage = `Exception: ${JSON.stringify(error)}`;
              }

              commandOutput = errorMessage;
              outputChannel.append(commandOutput);
              commandPassed = false;
            }
          },
        );

        if (commandPassed) {
          const selection = await vscode.window.showInformationMessage(
            "Distronode Development Tools installed successfully.",
            "Show Logs",
          );

          if (selection !== undefined) {
            outputChannel.show();
          }
        } else {
          const selection = await vscode.window.showErrorMessage(
            "Distronode Development Tools failed to install.",
            "Show Logs",
          );

          if (selection !== undefined) {
            outputChannel.show();
          }
        }
      },
    ),
  );
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.open-walkthrough-create-env",
      () => {
        vscode.commands.executeCommand(
          "workbench.action.openWalkthrough",
          "redhat.distronode#create-distronode-environment",
          false,
        );
      },
    ),
  );
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "distronode.create-playbook-options",
      async () => {
        if (
          await workspace.getConfiguration("distronode").get("lightspeed.enabled")
        ) {
          vscode.commands.executeCommand(
            "distronode.lightspeed.playbookGeneration",
          );
        } else {
          vscode.commands.executeCommand("distronode.create-empty-playbook");
        }
      },
    ),
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("distronode.create-empty-playbook", () => {
      const playbookTemplate = `---\n# Write your playbook below.\n# Replace these contents with the tasks you'd like to complete and the modules you need.\n# For help getting started, check out https://www.redhat.com/en/topics/automation/what-is-an-distronode-playbook\n`;

      vscode.workspace
        .openTextDocument({
          content: playbookTemplate,
          language: "distronode",
        })
        .then((newDocument) => {
          vscode.window.showTextDocument(newDocument);
        });
    }),
  );
  // open distronode language server logs
  context.subscriptions.push(
    vscode.commands.registerCommand("distronode.open-language-server-logs", () => {
      lsOutputChannel.show();
    }),
  );
}

const startClient = async (
  context: ExtensionContext,
  telemetry: TelemetryManager,
) => {
  const serverModule = context.asAbsolutePath(
    path.join("out", "server", "src", "server.js"),
  );

  // server is run at port 6009 for debugging
  const debugOptions = { execArgv: ["--nolazy", "--inspect=6010"] };

  const serverOptions: ServerOptions = {
    run: { module: serverModule, transport: TransportKind.ipc },
    debug: {
      module: serverModule,
      transport: TransportKind.ipc,
      options: debugOptions,
    },
  };

  const telemetryErrorHandler = new TelemetryErrorHandler(
    telemetry.telemetryService,
    lsName,
    4,
  );
  const outputChannel = window.createOutputChannel(lsName);
  lsOutputChannel = outputChannel;

  const clientOptions: LanguageClientOptions = {
    // register the server for Distronode documents
    documentSelector: [{ scheme: "file", language: "distronode" }],
    revealOutputChannelOn: RevealOutputChannelOn.Never,
    errorHandler: telemetryErrorHandler,
    outputChannel: new TelemetryOutputChannel(
      outputChannel,
      telemetry.telemetryService,
    ),
  };

  client = new LanguageClient(
    "distronodeServer",
    "Distronode Server",
    serverOptions,
    clientOptions,
  );

  // TODO: Temporary pause this telemetry event, will be enabled in future
  // context.subscriptions.push(
  //   client.onTelemetry((e) => {
  //     telemetry.telemetryService.send(e);
  //   }),
  // );

  try {
    await client.start();

    // If the extensions change, fire this notification again to pick up on any association changes
    extensions.onDidChange(() => {
      notifyAboutConflicts();
    });
    // TODO: Temporary pause this telemetry event, will be enabled in future
    // telemetry.sendStartupTelemetryEvent(true);
  } catch (err) {
    let errorMessage: string;
    if (err instanceof Error) {
      errorMessage = err.message;
    } else {
      errorMessage = String(err);
    }
    console.error(`Language Client initialization failed with ${errorMessage}`);
    // TODO: Temporary pause this telemetry event, will be enabled in future
    // telemetry.sendStartupTelemetryEvent(false, errorMessage);
  }
};

export function deactivate(): Thenable<void> | undefined {
  if (!client) {
    return undefined;
  }
  return client.stop();
}

async function updateDistronodeStatusBar(
  metaData: MetadataManager,
  lightSpeedManager: LightSpeedManager,
  pythonInterpreterManager: PythonInterpreterManager,
) {
  await metaData.updateDistronodeInfoInStatusbar();
  await lightSpeedManager.statusBarProvider.updateLightSpeedStatusbar();
  await pythonInterpreterManager.updatePythonInfoInStatusbar();
}
/**
 * Finds extensions that conflict with our extension.
 * If one or more conflicts are found then show an uninstall notification
 * If no conflicts are found then do nothing
 */
function notifyAboutConflicts(): void {
  const conflictingExtensions = getConflictingExtensions();
  if (conflictingExtensions.length > 0) {
    showUninstallConflictsNotification(conflictingExtensions);
  }
}

/**
 * Sends notification to the server to invalidate distronode inventory service cache
 * And resync the distronode inventory
 */

async function resyncDistronodeInventory(): Promise<void> {
  if (client.isRunning()) {
    client.onNotification(
      new NotificationType(`resync/distronode-inventory`),
      (event) => {
        console.log("resync distronode inventory event ->", event);
      },
    );
    client.sendNotification(new NotificationType(`resync/distronode-inventory`));
  }
}

export async function isLightspeedEnabled(): Promise<boolean> {
  if (
    !(await workspace.getConfiguration("distronode").get("lightspeed.enabled"))
  ) {
    await window.showErrorMessage(
      "Enable lightspeed services from settings to use the feature.",
    );
    return false;
  }
  return true;
}

async function lightspeedLogin(
  providerType: AuthProviderType | undefined,
): Promise<void> {
  if (!(await isLightspeedEnabled())) {
    return;
  }
  lightSpeedManager.currentModelValue = undefined;
  const authenticatedUser =
    await lightSpeedManager.lightspeedAuthenticatedUser.getLightspeedUserDetails(
      true,
      providerType,
    );
  if (authenticatedUser) {
    window.showInformationMessage(
      `Welcome back ${authenticatedUser.displayNameWithUserType}`,
    );
  }
}
