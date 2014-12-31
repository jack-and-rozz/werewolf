
# coding:utf-8

from village import Village
from log_learning_engine import LogLearningEngine
from role_inference_engine import RoleInferenceEngine
from log_parser import LogParser

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
        log_parser = LogParser()
        if (argc <= 1):
            log_srcfilename = FilePath.ROOTPATH + FilePath.SOURCE_LOG
            log_parser.getLog(log_srcfilename)
            parsed_logfilename = FilePath.ROOTPATH + FilePath.PARSED_LOG
        elif (argc == 2):
            print "error : 出力ファイル名を指定してください\n"
            exit()
        elif (argc >= 3):
            srcfile = FilePath.ROOTPATH + FilePath.LOGFILES + params[2]
            log_parser.getLog(srcfile)
            parsed_logfilename = FilePath.ROOTPATH + FilePath.LOGFILES + params[3]

        log_parser.saveParsedLog(parsed_logfilename,"w+")
    elif mode == "-learn":
        
        log_parser = LogParser()
        log_parser.loadParsedLog(FilePath.ROOTPATH + FilePath.PARSED_LOG)
        learning_engine = RoleInferenceEngine(log_parser)
        learning_engine.learnFromLog()
        learning_engine.checkEvaluations()
        learning_engine.saveParameters()

    elif mode == "-infer":
        role = params[2]
        role_inference_engine = RoleInferenceEngine()
        role_inference_engine.loadLearnedParameters()
        role_inference_engine.roleInferenceTest(role)
        #log_parser = LogParser()
        #log_parser.loadParsedLog(FilePath.ROOTPATH + FilePath.PARSED_LOG)
        #learning_engine =LogLearningEngine(log_parser)
        #learning_engine.learnFromLog()
        #learning_engine.roleInferenceTest(role)
    elif mode == "-game":
        village = Village(13)
        village.start()
    else:
        print "Invalid options"


