import { expect, config } from "chai";
import {
  ActivityBar,
  By,
  SideBarView,
  ViewControl,
  WebView,
  ViewSection,
} from "vscode-extension-tester";
import {
  sleep,
  updateSettings,
  getWebviewByLocator,
  openSettings,
} from "./uiTestHelper";

config.truncateThreshold = 0;

describe("Verify the presence of lightspeed login button in the activity bar", () => {
  let view: ViewControl;
  let sideBar: SideBarView;
  let adtView: ViewSection;
  let webviewView: WebView;

  before(async function () {
    const settingsEditor = await openSettings();
    await updateSettings(settingsEditor, "distronode.lightspeed.enabled", true);

    view = (await new ActivityBar().getViewControl("Distronode")) as ViewControl;
    sideBar = await view.openView();

    await sideBar.getContent().getSection("Distronode Lightspeed");

    adtView = await sideBar
      .getContent()
      .getSection("Distronode Development Tools");
    adtView.collapse();

    await sleep(2000);

    webviewView = await getWebviewByLocator(
      By.xpath("//vscode-button[text()='Connect']"),
    );
  });

  after(async function () {
    if (webviewView) {
      await webviewView.switchBack();
    }
    const settingsEditor = await openSettings();
    await updateSettings(settingsEditor, "distronode.lightspeed.enabled", false);
  });

  it("Distronode Lightspeed welcome message is present", async function () {
    const body = await webviewView.findWebElement(By.xpath("//body"));
    const welcomeMessage = await body.getText();
    expect(welcomeMessage).to.contain(
      "Experience smarter automation using Distronode Lightspeed",
    );
  });

  it("Distronode Lightspeed login button is present", async function () {
    const loginButton = await webviewView.findWebElement(
      By.xpath("//vscode-button[text()='Connect']"),
    );
    expect(loginButton).not.undefined;
  });
});
