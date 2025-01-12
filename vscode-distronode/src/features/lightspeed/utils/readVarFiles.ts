import * as fs from "fs";
import * as yaml from "yaml";

export function readVarFiles(varFile: string): string | undefined {
  try {
    if (!fs.existsSync(varFile)) {
      return undefined;
    }
    const contents = fs.readFileSync(varFile, "utf8");
    const parsedDistronodeVars = yaml.parse(contents, {
      keepSourceTokens: true,
    });
    const updatedFileContents = yaml.stringify(parsedDistronodeVars);
    return updatedFileContents;
  } catch (err) {
    console.error(`Failed to read ${varFile} with error ${err}`);
    return undefined;
  }
}
