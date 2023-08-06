from zhulong2.shanxi1 import shenghui
from zhulong2.shanxi1 import yuncheng





from lmf.dbv2 import db_command


from os.path import join ,dirname 

import time 

from zhulong2.util.conf import get_conp,get_conp1

#6
#8
def task_shenghui(**args):
    conp=get_conp(shenghui._name_)
    shenghui.work(conp,**args)
#10
def task_yuncheng(**args):
    conp=get_conp(yuncheng._name_)
    yuncheng.work(conp,**args)



def task_all():
    bg = time.time()
    try:

        task_shenghui()
        task_yuncheng()
    except:
        print("part shanxi1 error!")

    ed = time.time()

    cos = int((ed - bg) / 60)

    print("共耗时%d min" % cos)

def create_schemas():
    conp = get_conp1('zfcg')
    arr = [
        'shanxi1_shenghui',
        'shanxi1_yuncheng',
    ]
    for diqu in arr:
        sql = "create schema if not exists %s" % diqu
        db_command(sql, dbtype="postgresql", conp=conp)
    
