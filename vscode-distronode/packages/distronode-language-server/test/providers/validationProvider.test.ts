import { TextDocument } from "vscode-languageserver-textdocument";
import { expect } from "chai";
import { Diagnostic, Position, integer } from "vscode-languageserver";
import {
  doValidate,
  getYamlValidation,
} from "../../src/providers/validationProvider";
import { WorkspaceFolderContext } from "../../src/services/workspaceManager";
import {
  createTestValidationManager,
  createTestWorkspaceManager,
  getDoc,
  resolveDocUri,
  enableExecutionEnvironmentSettings,
  disableExecutionEnvironmentSettings,
  setFixtureDistronodeCollectionPathEnv,
} from "../helper";
import { ValidationManager } from "../../src/services/validationManager";

function testValidationFromCache(
  validationManager: ValidationManager,
  textDoc: TextDocument,
) {
  it("should provide no diagnostics", async function () {
    const actualDiagnostics = await doValidate(textDoc, validationManager);

    expect(actualDiagnostics.size).to.equal(0);
  });
}

function assertValidateTests(
  tests: testType[],
  context: WorkspaceFolderContext | undefined,
  validationManager: ValidationManager,
  textDoc: TextDocument,
  validationEnabled: boolean,
) {
  tests.forEach((test) => {
    it(`should provide diagnostics for ${test.name}`, async function () {
      expect(context).is.not.undefined;
      const actualDiagnostics: Map<string, Diagnostic[]> = await doValidate(
        textDoc,
        validationManager,
        false,
        context,
      );

      if (!validationEnabled) {
        expect(actualDiagnostics.has(`file://${textDoc.uri}`)).to.be.false;
        return;
      }

      if (test.diagnosticReport.length === 0) {
        expect(actualDiagnostics.has(`file://${textDoc.uri}`)).to.be.false;
      } else {
        const diags = actualDiagnostics.get(`file://${textDoc.uri}`);
        if (diags) {
          expect(diags.length).to.equal(test.diagnosticReport.length);
          diags.forEach((diag, i) => {
            const actDiag = diag;
            const expDiag = test.diagnosticReport[i];

            expect(actDiag.message).include(expDiag.message);
            expect(actDiag.range).to.deep.equal(expDiag.range);
            expect(actDiag.severity).to.equal(expDiag.severity);
            expect(actDiag.source).to.equal(expDiag.source);
          });
        } else {
          expect(false);
        }
      }
    });
  });
}

type testType = {
  name: string;
  diagnosticReport: Diagnostic[];
};

function testDistronodeLintErrors(
  context: WorkspaceFolderContext | undefined,
  validationManager: ValidationManager,
  textDoc: TextDocument,
  validationEnabled: boolean,
) {
  const tests: testType[] = [
    {
      name: "specific distronode lint errors and warnings (Warnings come from warn_list in distronode-lint config)",
      diagnosticReport: [
        {
          severity: 1,
          message: "Variables names",
          range: {
            start: { line: 4, character: 0 } as Position,
            end: {
              line: 4,
              character: integer.MAX_VALUE,
            } as Position,
          },
          source: "distronode-lint",
        },
        {
          severity: 1,
          message: "All tasks should be named",
          range: {
            start: { line: 6, character: 0 } as Position,
            end: {
              line: 6,
              character: integer.MAX_VALUE,
            } as Position,
          },
          source: "distronode-lint",
        },
        {
          severity: 1,
          message: "Use FQCN for builtin module actions",
          range: {
            start: { line: 14, character: 0 } as Position,
            end: {
              line: 14,
              character: integer.MAX_VALUE,
            } as Position,
          },
          source: "distronode-lint",
        },
        {
          severity: 1,
          message:
            "Command module does not accept setting environment variables inline.",
          range: {
            start: { line: 14, character: 0 } as Position,
            end: {
              line: 14,
              character: integer.MAX_VALUE,
            } as Position,
          },
          source: "distronode-lint",
        },
        {
          severity: 1,
          message: "Commands should not change things if nothing needs doing.",
          range: {
            start: { line: 14, character: 0 } as Position,
            end: {
              line: 14,
              character: integer.MAX_VALUE,
            } as Position,
          },
          source: "distronode-lint",
        },
        {
          severity: 2,
          message: "should not use a relative path",
          range: {
            start: { line: 18, character: 0 } as Position,
            end: {
              line: 18,
              character: integer.MAX_VALUE,
            } as Position,
          },
          source: "distronode-lint",
        },
      ],
    },
  ];
  assertValidateTests(
    tests,
    context,
    validationManager,
    textDoc,
    validationEnabled,
  );
}

function testDistronodeSyntaxCheckErrorsInDistronodeLint(
  context: WorkspaceFolderContext | undefined,
  validationManager: ValidationManager,
  textDoc: TextDocument,
  validationEnabled: boolean,
) {
  const tests: testType[] = [
    {
      name: "syntax-check errors in distronode-lint",
      diagnosticReport: [
        {
          severity: 1,
          message: "--syntax-check",
          range: {
            start: { line: 1, character: 2 } as Position,
            end: {
              line: 1,
              character: integer.MAX_VALUE,
            } as Position,
          },
          source: "Distronode",
        },
      ],
    },
  ];
  expect(context).to.not.be.undefined;
  if (context) {
    assertValidateTests(
      tests,
      context,
      validationManager,
      textDoc,
      validationEnabled,
    );
  }
}

function testDistronodeSyntaxCheckNoErrors(
  context: WorkspaceFolderContext | undefined,
  validationManager: ValidationManager,
  textDoc: TextDocument,
  validationEnabled: boolean,
) {
  const tests = [
    {
      name: "no specific distronode lint errors",
      diagnosticReport: [],
    },
  ];
  expect(context).to.not.be.undefined;
  if (context) {
    assertValidateTests(
      tests,
      context,
      validationManager,
      textDoc,
      validationEnabled,
    );
  }
}

function testDistronodeSyntaxCheckEmptyPlaybook(
  context: WorkspaceFolderContext | undefined,
  validationManager: ValidationManager,
  textDoc: TextDocument,
  validationEnabled: boolean,
) {
  const tests = [
    {
      name: "empty playbook",
      diagnosticReport: [],
    },
  ];
  assertValidateTests(
    tests,
    context,
    validationManager,
    textDoc,
    validationEnabled,
  );
}

function testDistronodeSyntaxCheckNoHost(
  context: WorkspaceFolderContext | undefined,
  validationManager: ValidationManager,
  textDoc: TextDocument,
  validationEnabled: boolean,
) {
  const tests: testType[] = [
    {
      name: "no host",
      diagnosticReport: [
        {
          severity: 1,

          message: "the field 'hosts' is required but was not set",
          range: {
            start: { line: 0, character: 0 } as Position,
            end: {
              line: 0,
              character: integer.MAX_VALUE,
            } as Position,
          },
          source: "Distronode",
        },
      ],
    },
  ];
  assertValidateTests(
    tests,
    context,
    validationManager,
    textDoc,
    validationEnabled,
  );
}

function testInvalidYamlFile(textDoc: TextDocument) {
  const tests = [
    {
      name: "invalid YAML",
      file: "diagnostics/invalid_yaml.yml",
      diagnosticReport: [
        {
          severity: 1,
          message: "Nested mappings are not allowed",
          range: {
            start: { line: 6, character: 13 } as Position,
            end: {
              line: 6,
              character: 14,
            } as Position,
          },
          source: "Distronode [YAML]",
        },
        {
          severity: 1,
          message: "Unexpected scalar at node end",
          range: {
            start: { line: 7, character: 0 } as Position,
            end: {
              line: 7,
              character: 6,
            } as Position,
          },
          source: "Distronode [YAML]",
        },
        {
          severity: 1,
          message: "Unexpected map-value-ind",
          range: {
            start: { line: 7, character: 6 } as Position,
            end: {
              line: 7,
              character: 7,
            } as Position,
          },
          source: "Distronode [YAML]",
        },
        {
          severity: 1,
          message: "Unexpected scalar token in YAML stream",
          range: {
            start: { line: 7, character: 8 } as Position,
            end: {
              line: 7,
              character: 12,
            } as Position,
          },
          source: "Distronode [YAML]",
        },
      ],
    },
  ];

  tests.forEach(({ name, diagnosticReport }) => {
    it(`should provide diagnostic for ${name}`, async function () {
      const actualDiagnostics = getYamlValidation(textDoc);
      expect(actualDiagnostics.length).to.equal(diagnosticReport.length);

      actualDiagnostics.forEach((diag, i) => {
        const actDiag = diag;
        const expDiag = diagnosticReport[i];

        expect(actDiag.message).include(expDiag.message);
        expect(actDiag.range).to.deep.equal(expDiag.range);
        expect(actDiag.severity).to.equal(expDiag.severity);
        expect(actDiag.source).to.equal(expDiag.source);
      });
    });
  });
}

describe("doValidate()", () => {
  const workspaceManager = createTestWorkspaceManager();
  const validationManager = createTestValidationManager();
  let fixtureFilePath = "diagnostics/lint_errors.yml";
  let fixtureFileUri = resolveDocUri(fixtureFilePath);
  let context = workspaceManager.getContext(fixtureFileUri);

  let textDoc = getDoc(fixtureFilePath);
  if (context) {
    let docSettings = context.documentSettings.get(textDoc.uri);

    describe("Get validation only from cache", () => {
      describe("With EE enabled @ee", () => {
        before(async () => {
          setFixtureDistronodeCollectionPathEnv(
            "/home/runner/.distronode/collections:/usr/share/distronode/collections",
          );
          await enableExecutionEnvironmentSettings(docSettings);
        });

        testValidationFromCache(validationManager, textDoc);

        after(async () => {
          setFixtureDistronodeCollectionPathEnv();
          await disableExecutionEnvironmentSettings(docSettings);
        });
      });

      describe("With EE disabled", () => {
        before(async () => {
          setFixtureDistronodeCollectionPathEnv();
          await disableExecutionEnvironmentSettings(docSettings);
        });

        testValidationFromCache(validationManager, textDoc);
      });
    });

    describe("Distronode diagnostics", () => {
      describe("Diagnostics using distronode-lint", () => {
        describe("With EE enabled @ee", () => {
          before(async () => {
            setFixtureDistronodeCollectionPathEnv(
              "/home/runner/.distronode/collections:/usr/share/distronode/collections",
            );
            await enableExecutionEnvironmentSettings(docSettings);
          });

          if (context) {
            testDistronodeLintErrors(context, validationManager, textDoc, true);
          }

          after(async () => {
            setFixtureDistronodeCollectionPathEnv();
            await disableExecutionEnvironmentSettings(docSettings);
          });
        });

        describe("With EE disabled", () => {
          before(async () => {
            setFixtureDistronodeCollectionPathEnv();
            await disableExecutionEnvironmentSettings(docSettings);
          });

          testDistronodeLintErrors(context, validationManager, textDoc, true);
        });

        describe("Syntax-check errors in distronode-lint", () => {
          fixtureFilePath =
            "diagnostics/syntax_check_errors_in_distronode_lint.yml";
          fixtureFileUri = resolveDocUri(fixtureFilePath);
          context = workspaceManager.getContext(fixtureFileUri);

          textDoc = getDoc(fixtureFilePath);
          expect(context).is.not.undefined;
          if (context) {
            docSettings = context.documentSettings.get(textDoc.uri);

            describe("With EE enabled @ee", () => {
              before(async () => {
                (await docSettings).validation.lint.enabled = false;
                setFixtureDistronodeCollectionPathEnv(
                  "/home/runner/.distronode/collections:/usr/share/distronode/collections",
                );
                await enableExecutionEnvironmentSettings(docSettings);
              });

              testDistronodeSyntaxCheckErrorsInDistronodeLint(
                context,
                validationManager,
                textDoc,
                true,
              );

              after(async () => {
                (await docSettings).validation.lint.enabled = true;
                setFixtureDistronodeCollectionPathEnv();
                await disableExecutionEnvironmentSettings(docSettings);
              });
            });

            describe("With EE disabled", () => {
              before(async () => {
                (await docSettings).validation.lint.enabled = false;
                setFixtureDistronodeCollectionPathEnv();
                await disableExecutionEnvironmentSettings(docSettings);
              });

              testDistronodeSyntaxCheckErrorsInDistronodeLint(
                context,
                validationManager,
                textDoc,
                true,
              );
            });
            after(async () => {
              (await docSettings).validation.lint.enabled = true;
              setFixtureDistronodeCollectionPathEnv();
              await disableExecutionEnvironmentSettings(docSettings);
            });
          }
        });
      });

      describe("Diagnostics using distronode-playbook --syntax-check", () => {
        describe("no specific distronode lint errors", () => {
          fixtureFilePath = "diagnostics/lint_errors.yml";
          fixtureFileUri = resolveDocUri(fixtureFilePath);
          context = workspaceManager.getContext(fixtureFileUri);

          textDoc = getDoc(fixtureFilePath);
          expect(context).is.not.undefined;

          if (context) {
            docSettings = context.documentSettings.get(textDoc.uri);

            describe("With EE enabled @ee", () => {
              before(async () => {
                (await docSettings).validation.lint.enabled = false;
                setFixtureDistronodeCollectionPathEnv(
                  "/home/runner/.distronode/collections:/usr/share/distronode/collections",
                );
                await enableExecutionEnvironmentSettings(docSettings);
              });

              testDistronodeSyntaxCheckNoErrors(
                context,
                validationManager,
                textDoc,
                true,
              );

              after(async () => {
                (await docSettings).validation.lint.enabled = true;
                setFixtureDistronodeCollectionPathEnv();
                await disableExecutionEnvironmentSettings(docSettings);
              });
            });

            describe("With EE disabled", () => {
              before(async () => {
                (await docSettings).validation.lint.enabled = false;
                setFixtureDistronodeCollectionPathEnv();
                await disableExecutionEnvironmentSettings(docSettings);
              });

              testDistronodeSyntaxCheckNoErrors(
                context,
                validationManager,
                textDoc,
                true,
              );
            });
            after(async () => {
              (await docSettings).validation.lint.enabled = true;
              setFixtureDistronodeCollectionPathEnv();
              await disableExecutionEnvironmentSettings(docSettings);
            });
          }
        });

        describe("empty playbook", () => {
          fixtureFilePath = "diagnostics/empty.yml";
          fixtureFileUri = resolveDocUri(fixtureFilePath);
          context = workspaceManager.getContext(fixtureFileUri);

          textDoc = getDoc(fixtureFilePath);
          expect(context).is.not.undefined;
          if (context) {
            docSettings = context.documentSettings.get(textDoc.uri);

            describe("With EE enabled @ee", () => {
              before(async () => {
                (await docSettings).validation.lint.enabled = false;
                setFixtureDistronodeCollectionPathEnv(
                  "/home/runner/.distronode/collections:/usr/share/distronode/collections",
                );
                await enableExecutionEnvironmentSettings(docSettings);
              });

              testDistronodeSyntaxCheckEmptyPlaybook(
                context,
                validationManager,
                textDoc,
                true,
              );

              after(async () => {
                (await docSettings).validation.lint.enabled = true;
                setFixtureDistronodeCollectionPathEnv();
                await disableExecutionEnvironmentSettings(docSettings);
              });
            });

            describe("With EE disabled", () => {
              before(async () => {
                (await docSettings).validation.lint.enabled = false;
                setFixtureDistronodeCollectionPathEnv();
                await disableExecutionEnvironmentSettings(docSettings);
              });

              testDistronodeSyntaxCheckEmptyPlaybook(
                context,
                validationManager,
                textDoc,
                true,
              );
            });
            after(async () => {
              (await docSettings).validation.lint.enabled = true;
              setFixtureDistronodeCollectionPathEnv();
              await disableExecutionEnvironmentSettings(docSettings);
            });
          }
        });

        describe("no host", () => {
          fixtureFilePath = "diagnostics/noHost.yml";
          fixtureFileUri = resolveDocUri(fixtureFilePath);
          context = workspaceManager.getContext(fixtureFileUri);

          textDoc = getDoc(fixtureFilePath);
          if (context) {
            docSettings = context.documentSettings.get(textDoc.uri);
          }

          describe("With EE enabled @ee", () => {
            before(async () => {
              (await docSettings).validation.lint.enabled = false;
              setFixtureDistronodeCollectionPathEnv(
                "/home/runner/.distronode/collections:/usr/share/distronode/collections",
              );
              await enableExecutionEnvironmentSettings(docSettings);
            });

            testDistronodeSyntaxCheckNoHost(
              context,
              validationManager,
              textDoc,
              true,
            );

            after(async () => {
              (await docSettings).validation.lint.enabled = true;
              setFixtureDistronodeCollectionPathEnv();
              await disableExecutionEnvironmentSettings(docSettings);
            });
          });

          describe("With EE disabled", () => {
            before(async () => {
              (await docSettings).validation.lint.enabled = false;
              setFixtureDistronodeCollectionPathEnv();
              await disableExecutionEnvironmentSettings(docSettings);
            });

            testDistronodeSyntaxCheckNoHost(
              context,
              validationManager,
              textDoc,
              true,
            );
          });
          after(async () => {
            (await docSettings).validation.lint.enabled = true;
            setFixtureDistronodeCollectionPathEnv();
            await disableExecutionEnvironmentSettings(docSettings);
          });
        });
      });

      describe("Diagnostics when validation is disabled", () => {
        describe("no specific distronode lint errors", () => {
          fixtureFilePath = "diagnostics/lint_errors.yml";
          fixtureFileUri = resolveDocUri(fixtureFilePath);
          context = workspaceManager.getContext(fixtureFileUri);

          textDoc = getDoc(fixtureFilePath);
          expect(context).is.not.undefined;
          if (context) {
            docSettings = context.documentSettings.get(textDoc.uri);

            describe("With EE enabled @ee", () => {
              before(async () => {
                // (await docSettings).validation.lint.enabled = false;
                // (await docSettings).validation.lint.path =
                //   "invalid-distronode-lint-path";
                (await docSettings).validation.enabled = false;
                setFixtureDistronodeCollectionPathEnv(
                  "/home/runner/.distronode/collections:/usr/share/distronode/collections",
                );
                await enableExecutionEnvironmentSettings(docSettings);
              });

              testDistronodeSyntaxCheckNoErrors(
                context,
                validationManager,
                textDoc,
                false,
              );

              after(async () => {
                // (await docSettings).validation.lint.enabled = true;
                // (await docSettings).validation.lint.path = "distronode-lint";
                (await docSettings).validation.enabled = true;
                setFixtureDistronodeCollectionPathEnv();
                await disableExecutionEnvironmentSettings(docSettings);
              });
            });

            describe("With EE disabled", () => {
              before(async () => {
                // (await docSettings).validation.lint.enabled = false;
                // (await docSettings).validation.lint.path =
                // "invalid-distronode-lint-path";
                (await docSettings).validation.enabled = false;
                setFixtureDistronodeCollectionPathEnv();
                await disableExecutionEnvironmentSettings(docSettings);
              });

              testDistronodeSyntaxCheckNoErrors(
                context,
                validationManager,
                textDoc,
                false,
              );
            });
            after(async () => {
              // (await docSettings).validation.lint.enabled = true;
              // (await docSettings).validation.lint.path = "distronode-lint";
              (await docSettings).validation.enabled = true;
              setFixtureDistronodeCollectionPathEnv();
              await disableExecutionEnvironmentSettings(docSettings);
            });
          }
        });

        describe("no host", () => {
          fixtureFilePath = "diagnostics/noHost.yml";
          fixtureFileUri = resolveDocUri(fixtureFilePath);
          context = workspaceManager.getContext(fixtureFileUri);

          textDoc = getDoc(fixtureFilePath);
          expect(context).is.not.undefined;
          if (context) {
            docSettings = context.documentSettings.get(textDoc.uri);

            describe("With EE enabled @ee", () => {
              before(async () => {
                // (await docSettings).validation.lint.enabled = false;
                // (await docSettings).validation.lint.path =
                //   "invalid-distronode-lint-path";
                (await docSettings).validation.enabled = false;
                setFixtureDistronodeCollectionPathEnv(
                  "/home/runner/.distronode/collections:/usr/share/distronode/collections",
                );
                await enableExecutionEnvironmentSettings(docSettings);
              });

              testDistronodeSyntaxCheckNoHost(
                context,
                validationManager,
                textDoc,
                false,
              );

              after(async () => {
                // (await docSettings).validation.lint.enabled = true;
                // (await docSettings).validation.lint.path = "distronode-lint";
                (await docSettings).validation.enabled = true;
                setFixtureDistronodeCollectionPathEnv();
                await disableExecutionEnvironmentSettings(docSettings);
              });
            });

            describe("With EE disabled", () => {
              before(async () => {
                // (await docSettings).validation.lint.enabled = false;
                // (await docSettings).validation.lint.path =
                //   "invalid-distronode-lint-path";
                (await docSettings).validation.enabled = false;
                setFixtureDistronodeCollectionPathEnv();
                await disableExecutionEnvironmentSettings(docSettings);
              });

              testDistronodeSyntaxCheckNoHost(
                context,
                validationManager,
                textDoc,
                false,
              );
            });
            after(async () => {
              // (await docSettings).validation.lint.enabled = true;
              // (await docSettings).validation.lint.path = "distronode-lint";
              (await docSettings).validation.enabled = true;
              setFixtureDistronodeCollectionPathEnv();
              await disableExecutionEnvironmentSettings(docSettings);
            });
          }
        });
      });
    });

    describe("YAML diagnostics", () => {
      fixtureFilePath = "diagnostics/invalid_yaml.yml";
      fixtureFileUri = resolveDocUri(fixtureFilePath);
      context = workspaceManager.getContext(fixtureFileUri);

      textDoc = getDoc(fixtureFilePath);
      expect(context).is.not.undefined;
      if (context) {
        docSettings = context.documentSettings.get(textDoc.uri);
        describe("With EE enabled @ee", () => {
          before(async () => {
            setFixtureDistronodeCollectionPathEnv(
              "/home/runner/.distronode/collections:/usr/share/distronode/collections",
            );
            await enableExecutionEnvironmentSettings(docSettings);
          });

          testInvalidYamlFile(textDoc);

          after(async () => {
            setFixtureDistronodeCollectionPathEnv();
            await disableExecutionEnvironmentSettings(docSettings);
          });
        });

        describe("With EE disabled", () => {
          before(async () => {
            setFixtureDistronodeCollectionPathEnv();
            await disableExecutionEnvironmentSettings(docSettings);
          });

          testInvalidYamlFile(textDoc);
        });
      }
    });
  }
});
