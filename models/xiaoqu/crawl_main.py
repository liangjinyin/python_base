# -*- coding: utf-8 -*-#

# ------------------------------------------------------------------------------- 
# Author:       liangjinyin
# Date:         2019/4/1 15:35
# Description:  小区爬取主类
# -------------------------------------------------------------------------------

from models.xiaoqu.crawl_community import CrawlCommunity
from models.xiaoqu.analysis_excel import Analysis_Excel
import threading
import time


def main():
    # 解析输入源
    excel_list = Analysis_Excel.read_excel()
    start_time = time.time()
    # t = threading.Thread(target=CrawlCommunity.data_trans, args=(excel_list, ))
    # t.start()
    result = CrawlCommunity.data_trans(excel_list)
    print(str(time.time()-start_time))
    # 导出excel
    Analysis_Excel.export_excel(result)


if __name__ == '__main__':
    main()
