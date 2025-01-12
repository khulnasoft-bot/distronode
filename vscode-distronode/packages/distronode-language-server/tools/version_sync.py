# utility to sync distronode-language-server version with vscode-distronode devel
# pylint: disable=unused-import
import json


def sync_als_version_in_vscode_distronode_devel():
    with open("package.json") as als_fp:
        package_json_als = json.load(als_fp)
    version_als = package_json_als["version"]

    with open("../vscode-distronode/package.json") as fp:
        package_json_vscode_distronode = json.load(fp)

    package_json_vscode_distronode["dependencies"]["@distronode/distronode-language-server"] = version_als
    with open("../vscode-distronode/package.json", "w") as fp:
        json.dump(package_json_vscode_distronode, fp, indent=4)


if __name__ == "__main__":
    sync_als_version_in_vscode_distronode_devel()
