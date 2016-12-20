#coding=utf-8

import os
import sys
import pickle
import random
import json


#----- case define -----
class CCase:
    def __init__(self):
        self.name = 'case'
        self.comment = 'I am comment'
        self.showtype='line'
        self.x = [0,1,2]
        self.y = [5,3,4]
        self.x_label = 'time'
        self.y_label = 'value'

    def set_values(self, name, comment, x, y, x_label, y_label):
        if name is not None :
            self.name = name
        if comment is not None:
            self.comment = comment
        if x is not None and len(x) > 0:
            self.x = []
            for a in x:
                self.x.append(a)
        if y is not None and len(y) >0:
            self.y = []
            for a in y:
                self.y.append(a)
        if x_label is not None:
            self.x_label = x_label
        if y_label is not None:
            self.y_label = y_label
        return

    def pt(self):
        print "------"
        print "name", self.name
        print "comment", self.comment
        print "showtype", self.showtype
        print "x", self.x
        print "y", self.y
        print "x_label", self.x_label
        print "y_label", self.y_label
        return

    def toDic(self):
        dic = {}
        dic['name'] = self.name
        dic['comment'] = self.comment
        dic['showtype'] = self.showtype
        dic['x'] = self.x
        dic['y'] = self.y
        dic['x_label'] = self.x_label
        dic['y_label'] = self.y_label
        return dic


class CSummary(CCase):
    def __init__(self):
        CCase.__init__(self)
        self.name = 'summary'
        self.showtype='poly'

class CMhInfo(CCase):
    def __init__(self):
        CCase.__init__(self)
        self.name = 'mhInfo'
        self.showtype = 'table'


#---- suite define ----
class CSuite:
    def __init__(self):
        self.name = "suitename"
        self.summary = None
        self.mh_info = None
        self.case_dic = {}

    def add_summary(self, summary):
        self.summary = summary

    def add_mhinfo(self, mhinfo):
        self.mh_info = mhinfo
    
    def add_case(self, onecase):
        if onecase is not None:
            self.case_dic[onecase.name] = onecase

    def pt(self):
        print "-"*5
        print "name", self.name
        if self.summary is not None:
            self.summary.pt()
        if self.mh_info is not None:
            self.mh_info.pt()
        print "--- cases ---"
        for _, c in self.case_dic.items():
            c.pt()
        print "-"*5


    def toDic(self):
        dic = {}
        dic['name'] = self.name
        if self.summary is not None:
            dic['summary'] = self.summary.toDic()
        else:
            dic['summary'] = {}
        if self.mh_info is not None:
            dic['mh_info'] = self.mh_info.toDic()
        else:
            dic['mh_info'] = {}
        dic['case_dic'] = {}
        for k, v in self.case_dic.items():
            dic['case_dic'][k]=v.toDic()
        return dic


#---- total data define ----
class CDatas:
    def __init__(self, base_dir = './datas'):
        self.suite_dic = {}
        self.base_dir = os.path.abspath(base_dir)
    
    def get_dumpfile_name(self, name = None):
        filename = 'cdata.dump'
        if name is not None:
            filename = name
        return os.path.join(self.base_dir, filename)

            
    def save(self, name = None):
        filename = self.get_dumpfile_name(name)
        with open(filename, 'wb') as f:
            pickle.dump(self.suite_dic, f)
        return

    def load(self, name = None):
        filename = self.get_dumpfile_name(name)
        if not os.path.exists(filename):
            self.suite_dic = {}
            return False
        else:
            with open(filename, 'rb') as f:
                self.suite_dic = pickle.load(f)
            return True

    def pt(self):
        print "-"*10, "CDATA", "-"*10
        print "base_dir :", self.base_dir
        idx = 0
        for _, s in self.suite_dic.items():
            print "-"*3, "suite ", idx, "-"*3
            s.pt()
        return
    
    def toDic(self):
        dic = {}
        dic['base_dir'] = self.base_dir
        dic['suite_dic'] = {}
        for k, v in self.suite_dic.items():
            dic['suite_dic'][k] = v.toDic()
        return dic

    def get_suite_names(self):
        return self.suite_dic.keys()

    def get_one_suite(self, suite_name):
        if suite_name not in self.suite_dic:
            return None
        return self.suite_dic[suite_name]

    def add_suite(self,suite):
        if suite is not None:
            self.suite_dic[suite.name] = suite

    def get_case_names(self, suitename = None):
        if suitename is None:
            case_names = []
            for _, s in self.suite_dic.items():
                case_names = s.case_dic.keys()
                return case_names
        else:
            if suitename not in self.suite_dic:
                return []
            else:
                return self.suite_dic[suitename].case_dic.keys()
    
    def get_one_case(self, suitename, casename):
        if suitename not in self.suite_dic:
            return None
        if casename not in self.suite_dic[suitename].case_dic:
            return None
        return self.suite_dic[suitename].case_dic[casename]

    def get_suite_summary(self, suitename):
        if suitename not in self.suite_dic:
            return None
        return self.suite_dic[suitename].summary

    def get_suite_mhinfo(self, suitename):
        if suitename not in self.suite_dic:
            return None
        return self.suite_dic[suitename].mh_info

#----- generate data func ----
def gen_case(idx):
    onecase = CCase()
    onecase.name = "case"+str(idx)
    onecase.comment = "Comment"+str(idx)+'\n'
    for i in range(50):
        onecase.x.append(i)
        onecase.y.append(random.randint(1,100))
    onecase.x_label = onecase.name
    onecase.y_label = 'v_'+str(idx)
    return onecase

def gen_summary(idx):
    onecase = CSummary()
    onecase.name = "summary"+str(idx)
    onecase.comment = "Comment"+str(idx)+'\n'
    for i in range(10):
        onecase.x.append('s_'+str(i))
        onecase.y.append(random.randint(1,100))
    onecase.x_label = onecase.name
    onecase.y_label = 'v_'+str(idx)
    return onecase

def gen_mhinfo(idx):
    onecase = CMhInfo()
    onecase.name = "mhinfo"+str(idx)
    onecase.comment = "Comment"+str(idx)+'\n'
    for i in range(10):
        onecase.x.append('m_'+str(i))
        onecase.y.append('MM_'+str(random.randint(1,10)))
    onecase.x_label = onecase.name
    onecase.y_label = 'v_'+str(idx)
    return onecase



def gen_data():
    base_dir = '../../datas'
    cdata = CDatas(base_dir)
    for i in range(10):
        suite = CSuite()
        suite.name = 'suite_'+str(i)
        for x in range(20):
            suite.add_case(gen_case(x))
        suite.add_summary(gen_summary(i))
        suite.add_mhinfo(gen_mhinfo(i))
        cdata.add_suite(suite)
    cdata.save()
    cdata.pt()


def get_data():
    base_dir = '../../datas'
    cdata = CDatas(base_dir)
    cdata.load()
    cdata.pt()




if __name__ == "__main__":
    #gen_data()
    get_data()
