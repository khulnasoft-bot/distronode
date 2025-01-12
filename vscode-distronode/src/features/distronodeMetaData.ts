/* eslint-disable  @typescript-eslint/no-explicit-any */
import {
  ExtensionContext,
  window,
  MarkdownString,
  ThemeColor,
  StatusBarItem,
  StatusBarAlignment,
} from "vscode";
import { NotificationType } from "vscode-languageclient";
import { LanguageClient } from "vscode-languageclient/node";
import { TelemetryManager, sendTelemetry } from "../utils/telemetryUtils";
import { formatDistronodeMetaData } from "./utils/formatDistronodeMetaData";
import { compareObjects, getValueFromObject } from "./utils/data";
import { SettingsManager } from "../settings";

interface distronodeMetadataEvent {
  distronodeVersion: string;
  pythonVersion?: string;
  distronodeLintVersion?: string;
  eeEnabled: boolean;
  lightSpeedEnabled: boolean;
  lightSpeedCodeAssistEnabled: boolean;
}

export class MetadataManager {
  private context;
  private client;
  private cachedDistronodeVersion = "";
  private metadataStatusBarItem: StatusBarItem;
  private telemetry: TelemetryManager;
  private extensionSettings: SettingsManager;
  private currentDistronodeMetaEventData: distronodeMetadataEvent | undefined;
  private previousDistronodeMetaEventData: distronodeMetadataEvent | undefined;
  private distronodeMetaData: any;

  constructor(
    context: ExtensionContext,
    client: LanguageClient,
    telemetry: TelemetryManager,
    extensionSettings: SettingsManager,
  ) {
    this.context = context;
    this.client = client;
    this.telemetry = telemetry;
    this.extensionSettings = extensionSettings;

    this.metadataStatusBarItem = this.initialiseStatusBar();
    this.currentDistronodeMetaEventData = undefined;
    this.previousDistronodeMetaEventData = undefined;
    this.distronodeMetaData = undefined;
  }

  private initialiseStatusBar(): StatusBarItem {
    // create a new status bar item that we can manage
    const metadataStatusBarItem = window.createStatusBarItem(
      StatusBarAlignment.Right,
      100,
    );
    this.context.subscriptions.push(metadataStatusBarItem);
    return metadataStatusBarItem;
  }

  /**
   * Calls the 'updateDistronodeInfo' function to update the distronode metadata
   * in the statusbar hovering action
   */
  public async updateDistronodeInfoInStatusbar(): Promise<void> {
    if (window.activeTextEditor?.document.languageId !== "distronode") {
      this.metadataStatusBarItem.hide();
      return;
    }

    await this.updateDistronodeInfo();
  }

  /**
   * Sends notification with active file uri as param to the server
   * and receives notification from the server with distronode meta data associated with the opened file as param
   */
  public async updateDistronodeInfo(): Promise<void> {
    if (!this.client.isRunning()) {
      return;
    }
    this.metadataStatusBarItem.tooltip = new MarkdownString(
      ` $(sync~spin) Fetching... `,
      true,
    );
    this.metadataStatusBarItem.show();
    this.client.onNotification(
      new NotificationType(`update/distronode-metadata`),
      (distronodeMetaDataList: any) => {
        this.distronodeMetaData = formatDistronodeMetaData(distronodeMetaDataList[0]);
        if (this.distronodeMetaData.distronodePresent) {
          console.log("Distronode found in the workspace");
          this.cachedDistronodeVersion =
            this.distronodeMetaData.metaData["distronode information"][
              "core version"
            ];
          const tooltip = this.distronodeMetaData.markdown;
          this.metadataStatusBarItem.text = this.distronodeMetaData.eeEnabled
            ? `$(bracket-dot) [EE] ${this.cachedDistronodeVersion}`
            : `$(bracket-dot) ${this.cachedDistronodeVersion}`;
          this.metadataStatusBarItem.backgroundColor = new ThemeColor(
            "statusBar.background",
          );
          this.metadataStatusBarItem.tooltip = tooltip;

          if (!this.distronodeMetaData.distronodeLintPresent) {
            this.metadataStatusBarItem.text = `$(warning) ${this.cachedDistronodeVersion}`;
            this.metadataStatusBarItem.backgroundColor = new ThemeColor(
              "statusBarItem.warningBackground",
            );
          }
          this.metadataStatusBarItem.show();
        } else {
          console.log("Distronode not found in the workspace");
          this.metadataStatusBarItem.text = "$(error) Distronode";
          this.metadataStatusBarItem.tooltip = this.distronodeMetaData.markdown;
          this.metadataStatusBarItem.backgroundColor = new ThemeColor(
            "statusBarItem.errorBackground",
          );
          this.metadataStatusBarItem.show();
        }
      },
    );
    const activeFileUri = window.activeTextEditor?.document.uri.toString();
    this.client.sendNotification(
      new NotificationType(`update/distronode-metadata`),
      [activeFileUri],
    );

    return;
  }

  public async sendDistronodeMetadataTelemetry(): Promise<void> {
    if (!this.distronodeMetaData) {
      return;
    }
    // Extract distronodeVersion and pythonVersion safely
    const distronodeVersion = getValueFromObject(this.distronodeMetaData.metaData, [
      "distronode information",
      "core version",
    ]);
    const pythonVersion = getValueFromObject(this.distronodeMetaData.metaData, [
      "python information",
      "version",
    ]);
    const distronodeLintVersion = this.distronodeMetaData.distronodeLintPresent
      ? getValueFromObject(this.distronodeMetaData.metaData, [
          "distronode-lint information",
          "version",
        ])
      : null;
    this.currentDistronodeMetaEventData = {
      distronodeVersion,
      pythonVersion,
      eeEnabled: this.extensionSettings.settings.executionEnvironment.enabled,
      lightSpeedEnabled:
        this.extensionSettings.settings.lightSpeedService.enabled,
      lightSpeedCodeAssistEnabled:
        this.extensionSettings.settings.lightSpeedService.suggestions.enabled,
    };
    if (this.distronodeMetaData.distronodeLintPresent) {
      this.currentDistronodeMetaEventData["distronodeLintVersion"] =
        distronodeLintVersion;
    }
    // Retrieve the previous event data from VS Code cache
    this.previousDistronodeMetaEventData =
      this.context.globalState.get<distronodeMetadataEvent>(
        "prevDistronodeMetadataEvent",
      );
    // send telemetry event only when distronode metadata changes
    if (
      distronodeVersion &&
      pythonVersion &&
      !compareObjects(
        this.currentDistronodeMetaEventData,
        this.previousDistronodeMetaEventData,
      )
    ) {
      console.log("Sending distronodeMetadata telemetry event");
      await sendTelemetry(
        this.telemetry.telemetryService,
        this.telemetry.isTelemetryInit,
        "distronodeMetadata",
        this.currentDistronodeMetaEventData,
      );
      this.context.globalState.update(
        "prevDistronodeMetadataEvent",
        this.currentDistronodeMetaEventData,
      );
    }
  }
}
