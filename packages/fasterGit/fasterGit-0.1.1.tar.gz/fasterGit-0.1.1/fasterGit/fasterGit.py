#!/usr/bin/env python
# -*- coding=utf-8 -*-


import os
import subprocess
import yaml


__author__ = "handa"
__version__ = "0.1.1"


def file_exist(filePath):
    """
    判断文件是否存在
    :param filePath: 文件目录
    :return:
    """
    if os.path.exists(filePath):
        return True
    else:
        return False


def readFile(filePath):
    """
    读取文件内容
    :param filePath: 文件路径
    :return:
    """
    with open(filePath, "r+") as fileReader:
        return fileReader.read()


def excommand_until_done(cmd):
    """
    子线程执行脚本，直到结束，并输出
    Arguments:
        cmd {str} -- cmd命令
    Returns:
        Pipe -- 管道
    """
    p = subprocess.Popen(args="export LANG=en_US.UTF-8;"+cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, close_fds=False)
    outPut = ""
    for line in iter(p.stdout.readline, ''):
        # if "close failed in file object destructor:" in line or "IOError: [Errno 9] Bad file descriptor" in line:
        #     continue
        outPut += line
        print line.rstrip()
    p.wait()
    return (p.returncode, outPut)


def readLines(filePath):
    """[按行读取文件的全部内容，返回数组]

    Arguments:
        filePath {string} -- 文件名

    Returns:
        List -- 每一行的数组
    """
    with open(filePath, "r") as file:
        return file.readlines()


def writeToFile(string, filePath):
    """
    把内容写进文件
    Arguments:
        string {string} -- 文件内容
        filePath {string} -- 文件路径
    """
    with open(filePath, "w+") as fileWriter:
        fileWriter.write(string)
        fileWriter.flush()


def returnError(message=""):
    print str(message)
    print "请确认您用了sudo命令。"
    exit(1)

def gitIp(host):
    # nslookup github.com
    cmd = "nslookup " + str(host)
    print cmd
    returnCode, content = excommand_until_done(cmd)
    if returnCode > 0:
        returnError("执行" + cmd + "失败：\n" + content)
    content = content.replace("\t", " ")
    contentDict = yaml.load(content)
    if contentDict.has_key("Address"):
        return contentDict["Address"]
    else:
        return ""

def changHost():
    hostPath = '/etc/hosts'
    if not file_exist(hostPath):
        print "host 文件不存在"
        exit(1)
    hostBackUp = os.path.join("/etc", "hosts.bp")
    if not file_exist(hostBackUp):
        # 备份host
        print "正在备份host到" + hostBackUp
        cmd = "cp -R -p " + hostPath + " " + hostBackUp
        returnCode, content = excommand_until_done(cmd)
        if returnCode > 0:
            returnError("Error:\n" + content)
    print "源host备份文件在" + hostBackUp

    print "获取 github.global.ssl.fastly.Net 的IP地址"
    githubGlobleHost = "github.global.ssl.fastly.net"
    githubGlobleIP = gitIp(githubGlobleHost)
    githubGlobleIPString = " ".join([githubGlobleIP, githubGlobleHost])

    print "获取 github.com 的IP地址"
    githubHost = "github.com"
    githubIP = gitIp(githubHost)
    githubIPString = " ".join([githubIP, githubHost])

    hostContentLines = readLines(hostPath)
    hostLines = []
    # 去掉旧的地址。
    print "清空旧host里关于github的信息"
    for line in hostContentLines:
        if githubGlobleHost in line or githubHost in line:
            continue
        hostLines.append(line)
    # 添加新的地址
    if "\n" not in hostLines[-1]:
        hostLines.append(" \n")
    newGitHost = githubGlobleIPString + "\n" + githubIPString
    hostLines.append(newGitHost)
    print "开始把新地址写入host\n" + newGitHost
    hostString = "".join(hostLines)
    writeToFile(hostString, hostPath)

    # 刷新
    cmd = "sudo killall -HUP mDNSResponder"
    print "刷新host：\n" + cmd
    returnCode, content = excommand_until_done(cmd)
    if returnCode > 0:
        returnError("请用sudo执行命令。")

def main():
    print "当前版本：" + __version__
    changHost()

if __name__ == "__main__":
    changHost()