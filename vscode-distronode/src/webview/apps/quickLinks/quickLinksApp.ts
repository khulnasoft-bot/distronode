import {
  allComponents,
  provideVSCodeDesignSystem,
} from "@vscode/webview-ui-toolkit";

provideVSCodeDesignSystem().register(allComponents);

const vscode = acquireVsCodeApi();
window.addEventListener("load", main);

let systemReadinessDiv: HTMLElement | null;
let systemReadinessIcon: HTMLElement;
let systemReadinessDescription: HTMLElement;

function main() {
  systemReadinessDiv = document.getElementById("system-readiness");
  systemReadinessIcon = document.createElement("section");
  systemReadinessDescription = document.createElement("section");

  updateDistronodeCreatorAvailabilityStatus();
}

function updateDistronodeCreatorAvailabilityStatus() {
  vscode.postMessage({
    message: "set-system-status-view",
  });

  window.addEventListener("message", (event) => {
    const message = event.data; // The JSON data our extension sent
    if (message.command === "systemDetails") {
      const systemDetails = message.arguments;
      const distronodeVersion = systemDetails["distronode version"];
      const pythonVersion = systemDetails["python version"];
      const distronodeCreatorVersion = systemDetails["distronode-creator version"];

      const systemStatus = !!(
        distronodeVersion &&
        pythonVersion &&
        distronodeCreatorVersion
      );

      if (!systemStatus) {
        //   systemReadinessDiv.style.backgroundColor = "#610000";
        systemReadinessIcon.innerHTML = `<span class="codicon codicon-warning"></span>`;
        systemReadinessDescription.innerHTML = `
              <p class="system-description">
                <b>Looks like you don't have an Distronode environment set up yet</b>.
                <br>
                <br>
                Follow the
                  <a href="command:distronode.open-walkthrough-create-env">
                    Create Distronode environment
                  </a> walkthrough, or
                  <a href="command:distronode.python.set.interpreter">
                    switch to another environment
                  </a> that has the setup ready.
              </p>`;
      }

      systemReadinessDiv?.appendChild(systemReadinessIcon);
      systemReadinessDiv?.appendChild(systemReadinessDescription);
    }
  });
}
