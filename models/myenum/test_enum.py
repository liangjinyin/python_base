# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/1/7 15:37
# Description:  
# -------------------------------------------------------------------------------

from enum import Enum


class STSTUS(Enum):
    USER_NOT_FIND = '203 用户不存在！'


print(STSTUS.USER_NOT_FIND.value)