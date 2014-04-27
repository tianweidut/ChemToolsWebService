# coding: utf-8

__all__ = ["MOL_ORIGIN_CHOICES", "STATUS_CHOICES",
           "STATUS_UNDEFINED", "STATUS_FAILED", "STATUS_SUCCESS",
           "STATUS_WORKING", "ORIGIN_UNDEFINED",
           "FILE_CHOICES", "MODEL_CHOICES", "MODEL_ORIGIN_CHOICES",
           "STATUS_CHOICES", "ORIGIN_DRAW", "ORIGIN_OTHER", "ORIGIN_SMILE",
           "ORIGIN_UPLOAD"]

MODEL_KOA = "koa"
MODEL_KOF = "kof"
MODEL_KOH = "koh"
MODEL_KOH_T = "koh_T"
MODEL_KOC = "koc"
MODEL_PL = "pl"
MODEL_BCF = "bcf"
MODEL_PKD = "pkd"
MODEL_PPK = "ppk"
MODEL_DFS = "dfs"
MODEL_RP = "rp"

MODEL_CHOICES = (
    (MODEL_KOA, MODEL_KOA),
    (MODEL_KOF, MODEL_KOF),
    (MODEL_KOC, MODEL_KOC),
    (MODEL_RP, MODEL_RP),
    (MODEL_PL, MODEL_PL),
    (MODEL_PKD, MODEL_PKD),
    (MODEL_PPK, MODEL_PPK),
    (MODEL_DFS, MODEL_DFS),
    (MODEL_BCF, MODEL_BCF),
    (MODEL_KOH, MODEL_KOH),
    (MODEL_KOH_T, MODEL_KOH_T),
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

FILE_CSV = "csv"
FILE_PDF = "pdf"
FILE_TXT = "txt"

FILE_CHOICES = (
    (FILE_CSV, u"csv"),
    (FILE_PDF, u"pdf"),
    (FILE_TXT, u"txt"),
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
