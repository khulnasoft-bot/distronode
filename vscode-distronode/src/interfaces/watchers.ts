import * as vscode from "vscode";

export type IDistronodeType = "vars_files";

export interface IWatchersType {
  watcher: vscode.FileSystemWatcher;
  type: IDistronodeType;
}

export interface IFileSystemWatchers {
  [key: string]: IWatchersType;
}
