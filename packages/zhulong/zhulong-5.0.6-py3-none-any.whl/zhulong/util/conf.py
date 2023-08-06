from lmf.dbv2 import db_command, db_write, db_query

from os.path import join, dirname


def get_conp(name, database=None):
    path1 = join(dirname(__file__), "cfg_db")
    if database is None:
        df = db_query("select * from cfg where schema='%s' " % name, dbtype='sqlite', conp=path1)
    else:
        df = db_query("select * from cfg where schema='%s' and database='%s' " % (name, database), dbtype='sqlite',
                      conp=path1)
    conp = df.values.tolist()[0]
    return conp


def get_conp1(name):
    path1 = join(dirname(__file__), "cfg_db")

    df = db_query("select * from cfg where database='%s' and schema='public' " % name, dbtype='sqlite', conp=path1)
    conp = df.values.tolist()[0]
    return conp


def command(sql):
    path1 = join(dirname(__file__), "cfg_db")
    db_command(sql, dbtype="sqlite", conp=path1)


def query(sql):
    path1 = join(dirname(__file__), "cfg_db")
    df = db_query(sql, dbtype='sqlite', conp=path1)
    return df


def update(user=None, password=None, host=None):
    if host is not None:
        sql = "update cfg set host='%s' " % host
        command(sql)
    if user is not None:
        sql = "update cfg set user='%s' " % user
        command(sql)
    if password is not None:
        sql = "update cfg set password='%s' " % password
        command(sql)


def add_conp(conp):
    sql = "insert into cfg values('%s','%s','%s','%s')" % (conp[0], conp[1], conp[2], conp[3])
    command(sql)


def get_df():
    data1 = {
        "anhui": ["anqing", "bengbu", "bozhou", "chaohu", "chizhou", "chuzhou", "fuyang",
                  "huaibei", "huainan", "huangshan", "luan", "maanshan"
            , "suzhou", "tongling", "wuhu", 'xuancheng', 'hefei'
                  ],
        "fujian": ["fujian", "fuqing", "fuzhou", "jianou", "longyan",
                   "nanan", "nanping", "ningde", "putian", "quanzhou",
                   "sanming", "shaowu", "wuyishan", "xiamen", "yongan",
                   "zhangzhou"],
        "guangdong": ["heyuan", "huizhou", "jiangmen", "jieyang", "meizhou", "yunfu"
            , "zhanjiang", "zhaoqing", "zhongshan", "zhuhai"
                      ],
        "guangxi": [
            "baise", "beihai", "chongzuo", "fangchenggang", "guangxi",
            "guigang", "guilin", "hechi", "hezhou", "laibin",
            "liuzhou", "nanning", "qinzhou", "wuzhou",
        ],
        "hainan": ["danzhou", "dongfang", "haikou", "hainan", "qionghai",
                   "sansha", "sanya"],
        "heilongjiang": ["daqing", "hegang", "heilongjiang", 'qiqihaer', 'yichun'],

        "henan": ["anyang", "dengfeng", "gongyi", "hebi", "jiaozhuo",
                  "jiyuan", "jiyuan1", "kaifeng", "linzhou", "luohe",
                  "luoyang", "mengzhou", "nanyang", "pingdingshan", "puyang",
                  "qinyang", "ruzhou", "sanmenxia", "shangqiu", "weihui",
                  "wugang", "xinmi", "xinyang", "xinxiang", "xinzheng",
                  "xuchang", "yanshi", "yongcheng", "zhengzhou", "zhoukou",
                  "zhumadian"],

        "hubei": ["enshi", "huanggang", "huangshi", "jingmen", "shiyan", "suizhou"
            , "xiangyang", "yichang"
                  ],

        "hunan": ["changde", "chenzhou", "hengyang", "huaihua", "loudi", "shaoyang"
            , "xiangtan", "yiyang", "yongzhou", "yueyang", "zhangjiajie", "zhuzhou"
                  ],

        "jiangsu": ["changshu", "changzhou", "danyang", "dongtai", "huaian"
            , "jiangyin", "kunshan", "lianyungang", "nanjing", "nantong"
            , "shenghui", "suqian", "suzhou", "taizhou", "wuxi"
            , "xinyi", "xuzhou", "yancheng", "yangzhou", "yizheng"
            , "zhangjiagang", "zhenjiang"
                    ],

        'jiangxi': ["dexing", "fengcheng", 'fuzhou', 'ganzhou', 'gaoan', 'jian', 'jiangxi', 'jingdezhen',
                    'jianggangshan', 'lushan', 'nanchang', 'ruichang', 'ruijin', 'shangrao',
                    'xinyu', 'yichun', 'yingtan', 'zhangshu'],

        "jilin": ['baicheng', 'baishan', 'changchun', 'jilin', 'jinlinshi', 'liaoyuan', 'siping', 'songyuan',
                  'tonghua'],

        "liaoning": [
            "anshan", "beizhen", "benxi", "chaoyang", "dalian",
            "dandong", "donggang", "fushun", "fuxin", "haicheng",
            "huludao", "jinzhou", "liaoning", "liaoyang", "panjin",
            "shenyang", "tieling", "yingkou",
        ],

        "neimenggu": [
            "baotou", "baoyannaoer", "chifeng", "eeduosi", "huhehaote",
            "hulunbeier", "manzhouli", "xinganmeng", "tongliao", "wuhai",
            "wulanchubu", "xilinguolemeng", "xinganmeng",
        ],

        "ningxia": ['guyuan', 'ningxia', 'yinchuan'],

        "qinghai": ['qinghai', 'xining'],

        "shandong": ["anqiu", "binzhou", "dongying", "feicheng", "jiaozhou",
                     "dezhou", "jinan", "laiwu", "leling", "linqing",
                     "pingdu", "qingdao", "rizhao", "rongcheng", "rushan",
                     "shenghui", "taian", "tengzhou", "weifang", "weihai",
                     "xintai", "yantai", "zaozhuang", "zibo", "linyi"
                     ],

        "shanxi1": ['shanxi'],

        "sichuan": ["bazhong", "chengdu", "chongzhou", "dazhou", "deyang",
                    "dujiangyan", "guangan", "guanghan", "guangyuan", "jiangyou",
                    "jianyang", "leshan", "longchang", "luzhou", "meishan",
                    "mianyang", "nanchong", "neijiang", "panzhihua", "pengzhou",
                    "qionglai", "shifang", "sichuan", "suining", "wanyuan",
                    "yaan", "yibin", "sichuan2",
                    ],
        "xizang": ['xizang', 'lasa', 'rikaze'],

        "yunnan": ['baoshan', 'chuxiong', 'dali', 'lijiang', 'lincang', 'puer', 'tengchong', 'wenshan', 'yunnan',
                   'yuxi', 'zhaotong', 'kunming'],

        "zhejiang": ["cixi", "dongyang", "hangzhou", "huzhou", "jiaxing",
                     "jinhua", "linhai", "lishui", "longquan", "ningbo",
                     "pinghu", "quzhou", "ruian", "shaoxing", "shengzhou",
                     "taizhou", "tongxiang", "wenling", "wenzhou", "yiwu",
                     "yueqing", "yuhuan", "zhejiang", "zhoushan", "zhuji"
                     ],

        "shanxi": ['chenzhou', 'shanxi', 'weinan', 'xian', 'xianyang', 'yanan'
                   ],
        "xinjiang": ['beitun', 'kezhou', 'wulumuqi', 'xinjiang'],

    }

    data = []

    for w in data1.keys():
        tmp1 = data1[w]
        for w1 in tmp1:
            tmp = ["postgres", "since2015", "127.0.0.1", w, w1]
            data.append(tmp)

    df = pd.DataFrame(data=data, columns=["user", 'password', "host", "database", "schema"])
    return df
