# coding:utf-8

from village import Village
from log_manager import RoleInferenceEngine
from log_manager import LogManager

import sys,os
import codecs

sys.path.append(os.pardir)
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/" + os.pardir)

from utils import Const
from utils import FilePath


#########実行ファイル時#############

if __name__ == "__main__":
    params = sys.argv
    argc = len(params)
    logmanager = LogManager()
    if argc <= 1 : 
        print "********************************************"
        print "Invalid options"
        print "-game"
        print "-parse output input"
        print "-learn"
        print "-infer rolename"
        print "********************************************"
        exit()

    mode = params[1]
    if mode == "-parse" :
        if (argc <= 1):
            log_srcfilename = FilePath.ROOTPATH + FilePath.SOURCE_LOG
            logmanager.getLog(log_srcfilename)
            parsed_logfilename = FilePath.ROOTPATH + FilePath.PARSED_LOG
        elif (argc == 2):
            print "error : 出力ファイル名を指定してください\n"
            exit()
        elif (argc >= 3):
            srcfile = FilePath.ROOTPATH + FilePath.LOGFILES + params[2]
            logmanager.getLog(srcfile)
            parsed_logfilename = FilePath.ROOTPATH + FilePath.LOGFILES + params[3]

        logmanager.saveParsedLog(parsed_logfilename,"w+")
    elif mode == "-learn":
        logmanager.loadParsedLog(FilePath.ROOTPATH + FilePath.PARSED_LOG)
        inferencer = RoleInferenceEngine(logmanager)
        inferencer.learn()
        inferencer.checkEvaluations()
        inferencer.saveParameters()

    elif mode == "-infer":
        role = params[2]
        #保存したパラメータをまだ使用していない
        logmanager.loadParsedLog(FilePath.ROOTPATH + FilePath.PARSED_LOG)
        inferencer = RoleInferenceEngine(logmanager)
        inferencer.learn()
        inferencer.roleInferenceTest(role)
    elif mode == "-game":
        village = Village(13)
        village.start()
    else:
        print "Invalid options"


