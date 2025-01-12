import { expect } from "chai";
import path = require("path");
import {
  distronodeMetaDataEntryType,
  distronodeMetaDataType,
  getDistronodeMetaData,
  getResultsThroughCommandRunner,
} from "../../src/utils/getDistronodeMetaData";
import {
  createTestWorkspaceManager,
  disableExecutionEnvironmentSettings,
  enableExecutionEnvironmentSettings,
  getDoc,
  resolveDocUri,
} from "../helper";

function getDistronodeTestInfo() {
  const distronodeInfo: distronodeMetaDataEntryType = {};
  distronodeInfo["core version"] = ".";
  distronodeInfo["location"] = "/distronode";
  // eslint-disable-next-line chai-friendly/no-unused-expressions
  (distronodeInfo["config file path"] = path.resolve(
    __dirname,
    "..",
    "fixtures",
    "utils",
    "getDistronodeMetaData",
    "distronode.cfg",
  )),
    (distronodeInfo["collections location"] = [
      path.resolve(__dirname, "..", "fixtures", "common", "collections"),
    ]);
  distronodeInfo["module location"] = ["/modules"];
  distronodeInfo["default host list path"] = [
    path.resolve(
      __dirname,
      "..",
      "fixtures",
      "utils",
      "getDistronodeMetaData",
      "inventory",
    ),
  ];
  return distronodeInfo;
}

function getPythonTestInfo() {
  const pythonInfo: distronodeMetaDataEntryType = {};
  pythonInfo["version"] = ".";
  pythonInfo["location"] = "/python3";
  return pythonInfo;
}

function getDistronodeLintTestInfo() {
  const distronodeLintInfo: distronodeMetaDataEntryType = {};
  distronodeLintInfo["version"] = ".";
  distronodeLintInfo["upgrade status"] = "A new version"; // this key will be undefined (but the key will be present) because the value only gets updated based on the distronode-lint version used
  distronodeLintInfo["location"] = "/distronode-lint";
  distronodeLintInfo["config file path"] = "/.distronode-lint"; // this key will be undefined (but the key will be present) because the value only gets updated when validation in run
  return distronodeLintInfo;
}

function getExecutionEnvironmentTestInfo() {
  const eeInfo: distronodeMetaDataEntryType = {};
  eeInfo["container engine"] = ["docker", "podman"];
  eeInfo["container image"] = "ghcr.io/";
  eeInfo["container volume mounts"] = [
    {
      src: "/fixtures/common/collections",
      dest: "/fixtures/common/collections",
    },
  ];
  return eeInfo;
}

function testCommands() {
  describe("Verify the working of command executions", () => {
    const tests = [
      {
        args: ["distronode", "--version"],
        result: "configured module search path",
      },
      {
        args: ["python3", "--version"],
        result: "Python",
      },
      {
        args: ["distronode-lint", "--version"],
        result: "using distronode",
      },
      {
        args: ["distronode-playbook", "missing-file"],
        result: undefined,
      },
    ];

    tests.forEach(({ args, result }) => {
      it(`should return result for '${args.join(" ")}'`, async function () {
        const output = await getResultsThroughCommandRunner(args[0], args[1]);
        if (result === undefined) {
          expect(output).to.be.undefined;
        } else {
          expect(output?.stdout).contains(result);
        }
      });
    });
  });
}

describe("getDistronodeMetaData()", () => {
  const workspaceManager = createTestWorkspaceManager();
  const fixtureFilePath = "utils/getDistronodeMetaData/plays.yml";
  const fixtureFileUri = resolveDocUri(fixtureFilePath);
  const context = workspaceManager.getContext(fixtureFileUri);

  const textDoc = getDoc(fixtureFilePath);
  const docSettings = context?.documentSettings.get(textDoc.uri);

  let actualDistronodeMetaData: distronodeMetaDataType = {};
  let distronodeInfoForTest: distronodeMetaDataEntryType = {};
  let pythonInfoForTest: distronodeMetaDataEntryType = {};
  let distronodeLintInfoForTest: distronodeMetaDataEntryType = {};
  let executionEnvironmentInfoForTest: distronodeMetaDataEntryType = {};

  describe("With EE disabled", () => {
    before(async () => {
      if (context !== undefined) {
        actualDistronodeMetaData = await getDistronodeMetaData(context, undefined);
      }
      distronodeInfoForTest = getDistronodeTestInfo();
      pythonInfoForTest = getPythonTestInfo();
      distronodeLintInfoForTest = getDistronodeLintTestInfo();
    });

    describe("Verify distronode details", () => {
      it("should contain all the keys for distronode information", function () {
        if (actualDistronodeMetaData["distronode information"]) {
          expect(Object.keys(distronodeInfoForTest).length).equals(
            Object.keys(actualDistronodeMetaData["distronode information"]).length,
          );
        } else {
          expect(false);
        }
      });

      it("should have information about distronode version used", function () {
        if (actualDistronodeMetaData["distronode information"]) {
          expect(
            actualDistronodeMetaData["distronode information"]["core version"],
          ).includes(distronodeInfoForTest["core version"]);
        } else {
          expect(false);
        }
      });

      it("should have a valid distronode location", function () {
        if (actualDistronodeMetaData["distronode information"]) {
          expect(
            actualDistronodeMetaData["distronode information"]["location"],
          ).include(distronodeInfoForTest["location"]);
        } else {
          expect(false);
        }
      });

      it("should have a valid config file location", function () {
        if (actualDistronodeMetaData["distronode information"]) {
          expect(
            actualDistronodeMetaData["distronode information"]["config file path"],
          ).to.include(distronodeInfoForTest["config file path"]);
        } else {
          expect(false);
        }
      });

      it("should have a valid collections location", function () {
        const x = distronodeInfoForTest["collections location"];
        if (Array.isArray(x)) {
          if (actualDistronodeMetaData["distronode information"]) {
            expect(
              actualDistronodeMetaData["distronode information"][
                "collections location"
              ],
            ).to.include.members(x);
          } else {
            expect(false);
          }
        }
      });

      it("should have a valid inventory file path", function () {
        const x = distronodeInfoForTest["default host list path"];
        if (Array.isArray(x) && actualDistronodeMetaData["distronode information"]) {
          expect(
            actualDistronodeMetaData["distronode information"][
              "default host list path"
            ],
          ).to.include.members(x);
        } else {
          expect(false);
        }
      });
    });

    describe("Verify python details", () => {
      it("should contain all the keys for python information", function () {
        if (actualDistronodeMetaData["python information"]) {
          expect(Object.keys(pythonInfoForTest).length).equals(
            Object.keys(actualDistronodeMetaData["python information"]).length,
          );
        } else {
          expect(false);
        }
      });
      it("should have information about python version used", function () {
        if (actualDistronodeMetaData["python information"]) {
          expect(
            actualDistronodeMetaData["python information"]["version"],
          ).includes(pythonInfoForTest["version"]);
        } else {
          expect(false);
        }
      });

      it("should have a valid python location", function () {
        if (actualDistronodeMetaData["python information"]) {
          expect(
            actualDistronodeMetaData["python information"]["location"],
          ).include(pythonInfoForTest["location"]);
        } else {
          expect(false);
        }
      });
    });

    describe("Verify distronode-lint details", () => {
      it("should contain all the keys for distronode-lint information", function () {
        expect(actualDistronodeMetaData["distronode-lint information"]);
        if (actualDistronodeMetaData["distronode-lint information"]) {
          const expectedKeys = Object.keys(distronodeLintInfoForTest);
          const actualKeys = Object.keys(
            actualDistronodeMetaData["distronode-lint information"],
          );

          const missingKeys = expectedKeys.filter(
            (key) => !actualKeys.includes(key),
          );

          const extraKeys = actualKeys.filter(
            (key) => !expectedKeys.includes(key),
          );

          expect(missingKeys).to.deep.equal(
            [],
            `Missing keys: ${missingKeys.join(", ")}`,
          );
          expect(extraKeys).to.deep.equal(
            [],
            `Extra keys: ${extraKeys.join(", ")}`,
          );
        }
      });
      it("should have information about distronode-lint version used", function () {
        if (actualDistronodeMetaData["distronode-lint information"]) {
          expect(
            actualDistronodeMetaData["distronode-lint information"]["version"],
          ).includes(distronodeLintInfoForTest["version"]);
        } else {
          expect(false);
        }
      });

      it("should have a valid distronode-lint location", function () {
        if (actualDistronodeMetaData["distronode-lint information"]) {
          expect(
            actualDistronodeMetaData["distronode-lint information"]["location"],
          ).include(distronodeLintInfoForTest["location"]);
        } else {
          expect(false);
        }
      });
    });

    describe("Verify the absence of execution environment details", () => {
      it("should not contain execution environment details", function () {
        expect(actualDistronodeMetaData["execution environment information"]).to.be
          .undefined;
      });
    });

    testCommands();
  });

  describe("With EE enabled @ee", () => {
    before(async () => {
      if (docSettings) {
        await enableExecutionEnvironmentSettings(docSettings);
      }

      if (context) {
        actualDistronodeMetaData = await getDistronodeMetaData(context, undefined);
      }
      distronodeInfoForTest = getDistronodeTestInfo();
      pythonInfoForTest = getPythonTestInfo();
      distronodeLintInfoForTest = getDistronodeLintTestInfo();
      executionEnvironmentInfoForTest = getExecutionEnvironmentTestInfo();
    });

    describe("Verify the presence of execution environment details", () => {
      it("should have a valid container engine", function () {
        if (actualDistronodeMetaData["execution environment information"]) {
          expect(
            executionEnvironmentInfoForTest["container engine"],
          ).to.include(
            actualDistronodeMetaData["execution environment information"][
              "container engine"
            ],
          );
        } else {
          expect(false);
        }
      });

      it("should have a valid container image", function () {
        if (actualDistronodeMetaData["execution environment information"]) {
          expect(
            actualDistronodeMetaData["execution environment information"][
              "container image"
            ],
          ).to.include(executionEnvironmentInfoForTest["container image"]);
        } else {
          expect(false);
        }
      });

      after(async () => {
        if (docSettings) {
          await disableExecutionEnvironmentSettings(docSettings);
        }
      });
    });

    testCommands();
  });
});
