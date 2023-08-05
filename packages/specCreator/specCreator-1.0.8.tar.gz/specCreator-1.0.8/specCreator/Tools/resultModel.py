#!/usr/bin/env python
# -*- coding=utf-8 -*-

from formatter import Formatter
from arguments import Arguments
from mdFormatter import MDFormatter
from shellCommand import Shell
from fileHandle import FileHandle
import json
import os


class ResultModel(object):
    __instance = None

    def __init__(self):
        self.formatter = Formatter.instance()
        self.mdFormatter = MDFormatter.instance()
        self.arguments = Arguments.instance()
        self.resultDict = {}
        self.versionHistory = ""


    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = ResultModel()
        return cls.__instance

    def recordResultDict(self):
        arguments = Arguments.instance()
        self.resultDict = arguments.argumentDict()

    def recordVersionHistory(self):
        self.versionHistory += self.mdFormatter.title(self.arguments.podName + " " + self.arguments.version, 2)
        disorderList = ["podName: " + self.arguments.podName, "version: " + self.arguments.version]
        if self.arguments.branch:
            disorderList.append("branch: " + self.arguments.branch)
        if self.arguments.commitId:
            disorderList.append("version: " + str(self.arguments.version))
        disorderList.append("subPackage: " + str(self.arguments.subPackage))
        disorderList.append("打的静态库包有:")

        if self.resultDict.has_key("dependency"):
            disorderList.append("dependency", str(self.resultDict["dependency"]))
        self.versionHistory += self.mdFormatter.disorderListString(disorderList)
        headerList = [" \\ ", " DebugPackage ", " ReleasePackage "]
        tableList = [" Framework "]
        if self.arguments.framework:
            if self.arguments.debugPackage:
                tableList.append(" ✔️ ")
            else:
                tableList.append("  ")
            if self.arguments.releasePackage:
                tableList.append(" ✔️ ")
            else:
                tableList.append("  ")
        else:
            tableList.append("  ")
            tableList.append("  ")
        self.versionHistory += self.mdFormatter.table([tableList], headerList)
        self.versionHistory += "\n\n"

    def saveResultPath(self):
        resultPath = self.arguments.resultPath
        if resultPath:
            if not FileHandle.instance().file_exist(resultPath):
                parentDir = os.path.dirname(resultPath)
                self.formatter.format_info("文件不存在，正在创建输出文件")
                Shell.instance().excommand_until_done("mkdir -p " + parentDir)
                Shell.instance().excommand_until_done("touch " + resultPath)
            FileHandle.instance().writeToFile(json.dumps(self.resultDict), resultPath)
            self.formatter.format_info("结果JSON写入成功"+ resultPath)
            self.formatter.format_info(str(self.resultDict))

    def saveVersionHistory(self):
        self.formatter.format_info("将打包信息写入VersionHistory文件")
        self.formatter.format_info(self.versionHistory)
        versionHistoryPath = os.path.join(self.arguments.projectPath, "VersionHistory.md")
        FileHandle.instance().appendToFile(self.versionHistory, versionHistoryPath)
