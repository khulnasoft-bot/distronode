import {
  allComponents,
  provideVSCodeDesignSystem,
} from "@vscode/webview-ui-toolkit";

provideVSCodeDesignSystem().register(allComponents);

const vscode = acquireVsCodeApi();
window.addEventListener("load", main);

let systemReadinessDiv: HTMLElement | null;
let installStatusDiv: HTMLElement | null;

let systemReadinessIcon: HTMLElement;
let systemReadinessDescription: HTMLElement;
let distronodeVersionStatusText: HTMLElement;
let distronodeLocationStatusText: HTMLElement;
let pythonVersionStatusText: HTMLElement;
let pythonLocationStatusText: HTMLElement;
let distronodeCreatorVersionStatusText: HTMLElement;
let distronodeDevEnvironmentStatusText: HTMLElement;
let walkthroughList: HTMLCollectionOf<Element> | null;

function main() {
  systemReadinessDiv = document.getElementById("system-readiness");

  installStatusDiv = document.getElementById("install-status");

  systemReadinessIcon = document.createElement("section");
  systemReadinessDescription = document.createElement("section");

  distronodeVersionStatusText = document.createElement("section");
  distronodeLocationStatusText = document.createElement("section");
  pythonVersionStatusText = document.createElement("section");
  pythonLocationStatusText = document.createElement("section");
  distronodeDevEnvironmentStatusText = document.createElement("section");
  distronodeCreatorVersionStatusText = document.createElement("section");

  walkthroughList = document.getElementsByClassName("walkthrough-item");
  Array.from(walkthroughList).forEach((walkthrough) => {
    walkthrough.addEventListener("click", handleWalkthroughClick);
  });

  updateDistronodeCreatorAvailabilityStatus();
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function handleWalkthroughClick(e: any) {
  const id: string =
    e.target["id"] ||
    e.target["parentNode"]["id"] ||
    e.target["offsetParent"]["id"];
  vscode.postMessage({
    command: "walkthrough",
    walkthrough: id,
  });
}

function updateDistronodeCreatorAvailabilityStatus() {
  vscode.postMessage({
    message: "set-system-status-view",
  });

  window.addEventListener("message", (event) => {
    const message = event.data; // The JSON data our extension sent

    switch (message.command) {
      case "systemDetails": {
        const systemDetails = message.arguments;
        const distronodeVersion = systemDetails["distronode version"];
        const distronodeLocation = systemDetails["distronode location"];
        const pythonVersion = systemDetails["python version"];
        const pythonLocation = systemDetails["python location"];
        const distronodeCreatorVersion = systemDetails["distronode-creator version"];
        const distronodeDevEnvironmentVersion =
          systemDetails["distronode-dev-environment version"];

        const systemStatus = !!(
          distronodeVersion &&
          pythonVersion &&
          distronodeCreatorVersion
        );

        if (systemStatus) {
          // Commented out temporarily for visibility issue with a light color theme
          // if (systemReadinessDiv)
          //   systemReadinessDiv.style.backgroundColor = "#023020";
          systemReadinessIcon.innerHTML = `<span class="codicon codicon-pass"></span>`;
          systemReadinessDescription.innerHTML = `<p class="system-description"><b>All the tools are installed</b>.<br>Your environment is ready and you can start creating distronode content.</p>`;
        } else {
          // if (systemReadinessDiv)
          //   systemReadinessDiv.style.backgroundColor = "#610000";
          systemReadinessIcon.innerHTML = `<span class="codicon codicon-warning"></span>`;
          systemReadinessDescription.innerHTML = `
            <p class="system-description">
              <b>Looks like you don't have an Distronode environment set up yet</b>.
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

        if (distronodeVersion) {
          distronodeVersionStatusText.innerHTML = `<p class='found'><b>Distronode version:</b> ${distronodeVersion}</p>`;
        } else {
          distronodeVersionStatusText.innerHTML = `<p class='not-found'><b>Distronode version:</b> Not found</p>`;
        }
        installStatusDiv?.appendChild(distronodeVersionStatusText);

        // distronode location text
        if (distronodeLocation) {
          distronodeLocationStatusText.innerHTML = `<p class='found'><b>Distronode location:</b> ${distronodeLocation}</p>`;
        } else {
          distronodeLocationStatusText.innerHTML = `<p class='not-found'><b>Distronode location:</b> Not found</p>`;
        }
        installStatusDiv?.appendChild(distronodeLocationStatusText);

        // python version text
        if (pythonVersion) {
          pythonVersionStatusText.innerHTML = `<p class='found'><b>Python version:</b> ${pythonVersion}</p>`;
        } else {
          pythonVersionStatusText.innerHTML = `<p class='not-found'><b>Python version:</b> Not found</p>`;
        }
        installStatusDiv?.appendChild(pythonVersionStatusText);

        // python location text
        if (pythonLocation) {
          pythonLocationStatusText.innerHTML = `<p class='found'><b>Python location:</b> ${pythonLocation}</p>`;
        } else {
          pythonLocationStatusText.innerHTML = `<p class='not-found'><b>Python location:</b> Not found</p>`;
        }
        installStatusDiv?.appendChild(pythonLocationStatusText);

        // ade version text
        if (distronodeDevEnvironmentVersion) {
          distronodeDevEnvironmentStatusText.innerHTML = `<p class='found'>[optional] <b>Distronode-dev-environment version:</b> ${distronodeDevEnvironmentVersion}</p>`;
        } else {
          distronodeDevEnvironmentStatusText.innerHTML = `<p class='not-found-optional'>[optional] <b>Distronode-dev-environment version:</b> Not found</p>`;
        }
        installStatusDiv?.appendChild(distronodeDevEnvironmentStatusText);

        // distronode-creator version text
        if (distronodeCreatorVersion) {
          distronodeCreatorVersionStatusText.innerHTML = `<p class='found'><b>Distronode-creator version:</b> ${distronodeCreatorVersion}</p>`;
        } else {
          distronodeCreatorVersionStatusText.innerHTML = `
          <p class='not-found'><b>Distronode-creator version:</b> Not found</p>
          <br>
          <p>Before getting started, please <vscode-link href="command:distronode.content-creator.install">install distronode-creator</vscode-link> (via pip) or <br>
          <vscode-link href="command:distronode.python-settings.open">switch to a different python interpreter</vscode-link>  with distronode-creator already installed in it.</p>
          `;
        }
        installStatusDiv?.appendChild(distronodeCreatorVersionStatusText);
      }
      // <p>&#x2717; python version: ${pythonVersion}</p>
      // <p>&#x2717; python location: ${pythonLocation}</p>
      // <p>&#x2717; distronode-creator version: ${distronodeCreatorVersion}</p>

      // `;
    }
  });
}
