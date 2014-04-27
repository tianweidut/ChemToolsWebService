#coding: utf-8

__all__ = ["LEVEL2_CHOICES", "LEVEL3_CHOICES", "LEVEL_CHOICES",
           "LEVEL_1"]

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
