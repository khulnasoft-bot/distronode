import { expect, config } from "chai";
import fs from "fs";
import {
  Workbench,
  BottomBarPanel,
  VSBrowser,
  SettingsEditor,
} from "vscode-extension-tester";
import { getFixturePath, updateSettings, sleep } from "./uiTestHelper";

config.truncateThreshold = 0;

describe("Verify the execution of playbook using distronode-playbook command", () => {
  let workbench: Workbench;
  let settingsEditor: SettingsEditor;
  const folder = "terminal";
  const file = "playbook.yml";
  const playbookFile = getFixturePath(folder, file);

  before(async function () {
    workbench = new Workbench();
  });
  it("Execute distronode-playbook command with arg", async function () {
    settingsEditor = await workbench.openSettings();
    await updateSettings(
      settingsEditor,
      "distronode.playbook.arguments",
      "--syntax-check",
    );

    await VSBrowser.instance.openResources(playbookFile);

    await workbench.executeCommand("Run playbook via `distronode-playbook`");

    const terminalView = await new BottomBarPanel().openTerminalView();
    const text = await terminalView.getText();

    expect(text).contains("distronode-playbook --syntax-check");
    await terminalView.killTerminal();
  });
  it("Execute distronode-playbook command without arg", async function () {
    const settingsEditor = await workbench.openSettings();
    await updateSettings(settingsEditor, "distronode.playbook.arguments", " ");
    await VSBrowser.instance.openResources(playbookFile);

    await workbench.executeCommand("Run playbook via `distronode-playbook`");

    const terminalView = await new BottomBarPanel().openTerminalView();
    const text = await terminalView.getText();

    expect(text).contains("distronode-playbook ");
    expect(text).does.not.contain("distronode-playbook --");

    await terminalView.killTerminal();
  });
});
describe("Verify the execution of playbook using distronode-navigator command", () => {
  let workbench: Workbench;
  let settingsEditor: SettingsEditor;
  const folder = "terminal";
  const file = "playbook.yml";
  const playbookFile = getFixturePath(folder, file);
  before(async function () {
    workbench = new Workbench();
  });
  // Skip this test on macOS due to CI container settings
  it("Execute playbook with distronode-navigator EE mode", async function () {
    if (process.platform !== "darwin") {
      settingsEditor = await workbench.openSettings();
      await updateSettings(
        settingsEditor,
        "distronode.executionEnvironment.enabled",
        true,
      );
      await updateSettings(
        settingsEditor,
        "distronode.executionEnvironment.containerEngine",
        "podman",
      );

      await VSBrowser.instance.openResources(playbookFile);

      await workbench.executeCommand(
        "Run playbook via `distronode-navigator run`",
      );
      await sleep(3500);

      const terminalView = await new BottomBarPanel().openTerminalView();
      const text = await terminalView.getText();

      // assert with just "Play " rather than "Play name" due to CI output formatting issues
      expect(text).contains("Play ");
      await terminalView.killTerminal();
    }
  });
  it("Execute playbook with distronode-navigator without EE mode", async function () {
    settingsEditor = await workbench.openSettings();
    await updateSettings(
      settingsEditor,
      "distronode.executionEnvironment.enabled",
      false,
    );
    await VSBrowser.instance.openResources(playbookFile);
    await workbench.executeCommand("Run playbook via `distronode-navigator run``");
    await sleep(3000);

    const terminalView = await new BottomBarPanel().openTerminalView();
    const text = await terminalView.getText();
    await terminalView.killTerminal();

    // assert with just "Play " rather than "Play name" due to CI output formatting issues
    expect(text).contains("Play ");
  });
  after(async function () {
    const folder = "terminal";
    const fixtureFolder = getFixturePath(folder) + "/";
    settingsEditor = await workbench.openSettings();

    await updateSettings(
      settingsEditor,
      "distronode.executionEnvironment.containerEngine",
      "docker",
    );
    fs.readdirSync(fixtureFolder).forEach((file) => {
      if (file.includes("playbook-artifact")) {
        fs.unlinkSync(fixtureFolder + file);
      }
    });
  });
});
