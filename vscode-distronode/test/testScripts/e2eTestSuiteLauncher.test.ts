import { testDiagnosticsDistronodeWithoutEE } from "./diagnostics/testDistronodeWithoutEE.test";
import { testDiagnosticsYAMLWithoutEE } from "./diagnostics/testYamlWithoutEE.test";
import { testHoverEE } from "./hover/testWithEE.test";
import { testHoverWithoutEE } from "./hover/testWithoutEE.test";
import {
  updateSettings,
  setFixtureDistronodeCollectionPathEnv,
  unSetFixtureDistronodeCollectionPathEnv,
  enableExecutionEnvironmentSettings,
  disableExecutionEnvironmentSettings,
  deleteAlsCache,
} from "../helper";
import { testLightspeed } from "./lightspeed/testLightspeed.test";
import { testExtensionForFilesOutsideWorkspace } from "./outsideWorkspace/testExtensionForFilesOutsideWorkspace.test";

describe("END-TO-END TEST SUITE FOR REDHAT.DISTRONODE EXTENSION", () => {
  const run_lightspeed_tests_only =
    process.env.RUN_LIGHTSPEED_TESTS_ONLY || "0";
  describe("TEST EXTENSION IN LOCAL ENVIRONMENT", () => {
    before(async () => {
      setFixtureDistronodeCollectionPathEnv(
        "/home/runner/.distronode/collections:/usr/share/distronode/collections",
      );
      await updateSettings("trace.server", "verbose", "distronodeServer");
    });

    after(async () => {
      await updateSettings("trace.server", "off", "distronodeServer"); // Revert back the default settings
    });

    if (run_lightspeed_tests_only !== "1") {
      testHoverWithoutEE();
      testDiagnosticsDistronodeWithoutEE();
      testDiagnosticsYAMLWithoutEE();
    }
    testLightspeed();
  });

  const skip_ee = process.env.SKIP_PODMAN || process.env.SKIP_DOCKER || "0";
  if (skip_ee !== "1" && run_lightspeed_tests_only !== "1") {
    describe("TEST EXTENSION IN EXECUTION ENVIRONMENT", () => {
      before(async () => {
        deleteAlsCache();
        setFixtureDistronodeCollectionPathEnv(
          "/home/runner/.distronode/collections:/usr/share/distronode/collections",
        );
        await enableExecutionEnvironmentSettings();
      });

      after(async () => {
        await disableExecutionEnvironmentSettings(); // Revert back the default settings
        unSetFixtureDistronodeCollectionPathEnv();
        deleteAlsCache();
      });

      testHoverEE();
    });
  }

  if (run_lightspeed_tests_only !== "1") {
    describe("TEST EXTENSION FOR FILES OUTSIDE WORKSPACE", function () {
      testExtensionForFilesOutsideWorkspace();
    });
  }
});
