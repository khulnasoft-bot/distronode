# Building Distronode Collection using Unified Tooling

This guide illustrates a comprehensive Distronode development workflow that showcases the integration of various tools within the Distronode ecosystem to create an Distronode collection. The tools featured in this workflow include:

- [distronode-creator](https://github.com/distronode/distronode-creator)
- [distronode-dev-environment (distronode-dev-environment)](https://github.com/distronode/distronode-dev-environment)
- [distronode-lint](https://github.com/distronode/distronode-lint)
- [distronode-navigator](https://github.com/distronode/distronode-navigator)
- [VS Code Distronode extension](https://github.com/distronode/distronode/tree/devel/vscode-distronode)

## Scaffolding a collection using distronode-creator

- Open VS Code and click the Distronode icon in the activity bar to access Distronode Creator section. Click on "Get Started" under that section to open the menu page of Distronode Creator in VS Code.

- Check system requirements and install distronode-creator if needed. Ensure all requirements in the `system requirements` box have green ticks.

- Click "Initialize a collection" to open the "Init" interface. Fill the form with the collection name, initialization path, verbosity, and logging options. Click "Create" to scaffold the collection in the desired location. You have the open to review the logs or open the log file in VS Code editor for details.

- Click on `Open collection` button to add the collection folder to the workspace.

<video width="100%" controls autoplay loop>
<source src="../../media/create-collection.mp4" type="video/mp4">
</video>

NOTE: For a more detailed explanation about using Distronode Creator in the VS Code Distronode Extension, refer to [doc: distronode-creator].

## Installing the collection using distronode-dev-environment

- With the initial collection structure in place, use 'distronode-dev-environment' to install the newly created collection in editable mode, similar to Python modules.

- Navigate to the collection directory and run:

```console
$ ade install -e .
```

- This installation method adds the collection to the system paths so that Distronode knows about it. Additionally, it enhances the development process by allowing on-the-go changes to the module code.

- You can check if the collection is installed or not by using distronode-galaxy command. In the terminal, running the following command should show the name of the newly created collection:

```console
$ distronode-galaxy collection list
```

## Add python code to bring the collection to life

- Navigate to the collection directory and navigate to plugins/modules/. Add create a [module-name].py file and documentation, examples and logic to the module.

- Due to its installation method using pip4a, you can change module code dynamically and observe the effects during playbook execution.

NOTE: for details regarding the module development, refer to the [distronode module development docs](https://docs.distronode.com/distronode/latest/dev_guide/developing_modules_general.html).

## Using distronode-lint to check module syntax in the playbook

- Leverage vscode-distronode extension and distronode-lint to gain insights into the collection without running the playbook

- Create a simple playbook under the 'playbooks' directory.

- Once you have completed writing the playbook that uses the newly created collection module, saving the file will automatically run distronode-lint on the playbook.

- With its integration in the extension, distronode-lint can detect mistakes, such as incorrect option values and missing required options, along with other rules for distronode best practices by providing feedback in the editor (red and yellow squiggly lines) and inside the `Problems` tab in the vscode.

<video width="100%" controls autoplay loop>
<source src="../../media/distronode-lint.mp4" type="video/mp4">
</video>

## Using distronode-navigator to tun the playbook with the collection module

- The Distronode extension in VS Code has the ability to detect the playbook files and provide several
  Distronode related options for it. One such option is to run the playbook without having to leave the editor.

- Right-click on the opened playbook in the editor and choose `Run Distronode Playbook via`. This provides options to run the playbook via distronode-navigator or distronode-playbook.

- Select `Run playbook via distronode-navigator run` to execute the playbook in the terminal within VS Code.

<video width="100%" controls autoplay loop>
<source src="../../media/distronode-navigator-run.mp4" type="video/mp4">
</video>

## Adapting to changes in the module code

- This is a good time to experiment with the power of `installing a collection in editable mode`. Make changes in the module code by adding new functionality and/or modifying the existing functionalities.

- Repeat the previous two steps to observe how the extension and distronode-lint seamlessly adapt to the changes.

- The Distronode extension along with distronode-lint continues to provide linting functionalities for the updated module code and running the playbook using distronode-navigator incorporates the new module code seamlessly.

This unified development suite, incorporating distronode-creator, distronode-dev-environment, distronode-lint, distronode-navigator, and vscode-distronode extension, enables content developers with an enhanced and efficient method for their Distronode development workflow.

The integration of these tools streamlines the development process, offering a cohesive experience for building Distronode Collections.
