# coding: utf-8

__all__ = ["MOL_ORIGIN_CHOICES", "STATUS_CHOICES",
           "STATUS_UNDEFINED", "STATUS_FAILED", "STATUS_SUCCESS",
           "STATUS_WORKING", "ORIGIN_UNDEFINED",
           "MODEL_CHOICES", "MODEL_ORIGIN_CHOICES",
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
MODEL_BDG = 'bdg'

MODEL_CHOICES = (
    (MODEL_KOA, "正辛醇/空气分配系数"),
    (MODEL_KOF, MODEL_KOF),
    (MODEL_KOC, "土壤/沉积物吸附系数"),
    (MODEL_RP, "甲状腺素干扰效应"),
    (MODEL_PL, "过冷液体蒸气压"),
    (MODEL_PKD, MODEL_PKD),
    (MODEL_PPK, MODEL_PPK),
    (MODEL_DFS, MODEL_DFS),
    (MODEL_BCF, "生物富集因子"),
    (MODEL_KOH, "气相羟基自由基反应速率常数"),
    (MODEL_KOH_T, "气相羟基自由基反应速率常数"),
    (MODEL_BDG, "生物降解性"),
)

MODEL_EN_PHY = "en_physiochemical"
MODEL_EN_TRANS = "en_transform"
MODEL_EN_TOXICOLOGY = "en_toxicology"
MODEL_HEALTH_TO = "health_toxicology"

MODEL_ORIGIN_CHOICES = (
    (MODEL_EN_PHY, u"理化属性"),
    (MODEL_EN_TRANS, u"迁移转化"),
    (MODEL_EN_TOXICOLOGY, u"生态毒性"),
    (MODEL_HEALTH_TO, u"健康毒性"),
)

STATUS_SUCCESS = "success"
STATUS_FAILED = "failed"
STATUS_WORKING = "calculating"
STATUS_UNDEFINED = "undefined"

STATUS_CHOICES = (
    (STATUS_SUCCESS, u"计算成功"),
    (STATUS_FAILED, u"计算失败"),
    (STATUS_WORKING, u"正在计算"),
    (STATUS_UNDEFINED, u"未定义"),
)

ORIGIN_UPLOAD = "upload"
ORIGIN_SMILE = "smiles"
ORIGIN_DRAW = "drawing"
ORIGIN_OTHER = "other"
ORIGIN_UNDEFINED = "undefined"

MOL_ORIGIN_CHOICES = (
    (ORIGIN_UPLOAD, "文件上传"),
    (ORIGIN_SMILE, "综合搜索"),
    (ORIGIN_OTHER, "其他"),
    (ORIGIN_DRAW, "分子式绘制"),
    (ORIGIN_UNDEFINED, "未定义"),
)

MODEL_SPLITS = ";"

TASK_SUITE = "suitetask"
TASK_SINGLE = "singletask"
