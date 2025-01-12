import { MetadataManager } from "../features/distronodeMetaData";
import { LightSpeedManager } from "../features/lightspeed/base";
import { PythonInterpreterManager } from "../features/pythonMetadata";
import { SettingsManager } from "../settings";

export async function updateConfigurationChanges(
  metaData: MetadataManager,
  pythonInterpreter: PythonInterpreterManager,
  extSettings: SettingsManager,
  lightSpeedManager: LightSpeedManager,
): Promise<void> {
  await metaData.updateDistronodeInfoInStatusbar();
  await lightSpeedManager.reInitialize();
  await pythonInterpreter.updatePythonInfoInStatusbar();

  await extSettings.reinitialize();
}
