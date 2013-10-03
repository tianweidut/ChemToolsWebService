# coding: UTF-8
'''
Created on 2013-03-27

@author: tianwei

Desc: const defination
'''

__all__ = ["MOL_ORIGIN_CHOICES", "STATUS_CHOICES",
           "STATUS_UNDEFINED", "STATUS_FAILED", "STATUS_SUCCESS",
           "STATUS_WORKING", "ORIGIN_UNDEFINED",
           "FILE_CHOICES", "MODEL_CHOICES", "MODEL_ORIGIN_CHOICES",
           "STATUS_CHOICES", "LEVEL2_CHOICES", "LEVEL3_CHOICES",
           "LEVEL_CHOICES", "ORIGIN_DRAW", "ORIGIN_OTHER", "ORIGIN_SMILE",
           "ORIGIN_UPLOAD"]

FILE_CSV = "csv"
FILE_PDF = "pdf"
FILE_TXT = "txt"

FILE_CHOICES = (
    (FILE_CSV, u"csv"),
    (FILE_PDF, u"pdf"),
    (FILE_TXT, u"txt"),
)

MODEL_KOA = "koa"
MODEL_KOF = "kof"
MODEL_KOH = "koh"
MODEL_KOH_T="koh_T"
MODEL_KOC = "koc"
MODEL_PL  = "pl"
MODEL_BCF = "bcf"
MODEL_PKD = "pkd"
MODEL_PPK = "ppk"
MODEL_DFS = "dfs"
MODEL_RP  = "rp"

MODEL_CHOICES = (
    (MODEL_KOA, MODEL_KOA),
    (MODEL_KOF, MODEL_KOF),
    (MODEL_KOC, MODEL_KOC),
    (MODEL_RP , MODEL_RP ),
    (MODEL_PL,  MODEL_PL ),
    (MODEL_PKD, MODEL_PKD),
    (MODEL_PPK, MODEL_PPK),
    (MODEL_DFS, MODEL_DFS),
    (MODEL_BCF, MODEL_BCF),
    (MODEL_KOH, MODEL_KOH),
    (MODEL_KOH_T,MODEL_KOH_T),
)

MODEL_EN_BEHAVIOR = "en_behavior"
MODEL_EN_TOXICOLOGY = "en_toxicology"
MODEL_HEALTH_TO = "health_toxicology"

MODEL_ORIGIN_CHOICES = (
    (MODEL_EN_BEHAVIOR, u"Environment Behavior"),
    (MODEL_EN_TOXICOLOGY, u"Environment toxicology"),
    (MODEL_HEALTH_TO, u"Health Toicology"),
)


STATUS_SUCCESS = "success"
STATUS_FAILED = "failed"
STATUS_WORKING = "calculating"
STATUS_UNDEFINED = "undefined"

STATUS_CHOICES = (
    (STATUS_SUCCESS, u"Calculate Successfully!"),
    (STATUS_FAILED, u"Calculate Failed!"),
    (STATUS_WORKING, u"Still calculating"),
    (STATUS_UNDEFINED, u"undefined"),
)

LEVEL_1 = "1"
LEVEL_2 = "2"
LEVEL_3 = "3"
LEVEL_4 = "4"
LEVEL_5 = "5"

LEVEL_CHOICES = (
    (LEVEL_1, "Free"),
    (LEVEL_2, "Micro"),
    (LEVEL_3, "Normal"),
    (LEVEL_4, "VIP"),
    (LEVEL_5, "Ultimate"),
)

LEVEL2_CHOICES = (
    (LEVEL_1, "Level 1"),
    (LEVEL_2, "Level 2"),
    (LEVEL_3, "Level 3"),
    (LEVEL_4, "Level 4"),
    (LEVEL_5, "Level 5"),
)

LEVEL3_CHOICES = (
    (LEVEL_1, "Free"),
    (LEVEL_2, "Personal"),
    (LEVEL_3, "Education"),
    (LEVEL_4, "Micro Enterprise"),
    (LEVEL_5, "Enterprise"),
)

ORIGIN_UPLOAD = "upload"
ORIGIN_SMILE = "smiles"
ORIGIN_DRAW = "drawing"
ORIGIN_OTHER = "other"
ORIGIN_UNDEFINED = "undefined"

MOL_ORIGIN_CHOICES = (
    (ORIGIN_UPLOAD, "mol upload driectly"),
    (ORIGIN_SMILE, "smiles search"),
    (ORIGIN_OTHER, "other"),
    (ORIGIN_DRAW, "draw"),
    (ORIGIN_UNDEFINED, "undefined"),
)

MODEL_SPLITS = ";"

TASK_SUITE = "suitetask"
TASK_SINGLE = "singletask"
