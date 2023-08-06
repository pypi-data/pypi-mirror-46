from lmf.dbv2 import db_command

from zhulong.shanxi1 import shanxi


from os.path import join, dirname


import time

from zhulong.util.conf import get_conp,get_conp1


# 1
def task_shanxi(**args):
    conp = get_conp(shanxi._name_)
    shanxi.work(conp,cdc_total=1, **args)




def task_all():
    bg = time.time()
    try:
        task_shanxi()


    except:
        print("part1 error!")



    ed = time.time()

    cos = int((ed - bg) / 60)

    print("共耗时%d min" % cos)


# write_profile('postgres,since2015,127.0.0.1,shandong')


def create_schemas():
    conp = get_conp1('shanxi1')
    arr = ['shanxi']
    for diqu in arr:
        sql = "create schema if not exists %s" % diqu
        db_command(sql, dbtype="postgresql", conp=conp)




