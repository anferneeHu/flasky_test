#coding=utf-8

import os
from flask import jsonify, request, g, url_for, current_app
from . import api

from app.proc.suites import *

base_dir = os.path.abspath('./datas')
cdata = None





@api.route('/datas/suite_list')
def get_suite_list():
    init_data()
    lst = cdata.get_suite_names()
    print lst
    rsp = {'suite':lst}
    return jsonify(rsp)


@api.route('/datas/case_list')
def get_case_list():
    init_data()
    lst = cdata.get_case_names()
    print lst
    rsp = {'case':lst}
    return jsonify(rsp)

@api.route('/datas/<suite>/case_list')
def get_case_list_by_suite(suite):
    init_data()
    lst = cdata.get_case_names(suite)
    print lst
    rsp = {'case':lst}
    return jsonify(rsp)

@api.route('/datas/<suite>/<case>')
def get_case(suite, case):
    init_data()
    case = cdata.get_one_case(suite, case)
    if case is None:
        return jsonify({})
    else:
        return jsonify(case.toDic())

@api.route('/datas/<suite>/summary')
def get_summary(suite):
    init_data()
    summary = cdata.get_suite_summary(suite)
    if summary is None:
        return jsonify({})
    else:
        return jsonify(summary.toDic())

@api.route('/datas/<suite>/mhinfo')
def get_mhinfo(suite):
    init_data()
    mhinfo = cdata.get_suite_mhinfo(suite)
    if mhinfo is None:
        return jsonify({})
    else:
        return jsonify(mhinfo.toDic())

def init_data():
    global cdata
    if cdata is None:
        cdata = CDatas(base_dir)
        cdata.load()
    return
