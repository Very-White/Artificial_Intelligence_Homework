from Search import a_star_search, iterative_deepening_a_star_search, trace_back
from graph import all_task

import time
import datetime

# 记录程序开始的时间
for task_num in range(0, 6):
    start_time = time.time()

    cost, come_from = iterative_deepening_a_star_search(all_task[task_num])
    path = trace_back(come_from)
    print(f'路径长度:{len(path)}')
    # for line in path:
    #     print(line)
    #     print()

    end_time = time.time()

    # 计算程序运行所花费的时间（秒）
    elapsed_time = end_time - start_time

    # 将秒转换为更易读的格式（分钟、秒、毫秒）
    formatted_time = str(datetime.timedelta(seconds=elapsed_time))

    # 显示程序运行时间
    print(f"程序运行完成，所花费的时间为：{formatted_time}")
    print("\n_______________分割线___________________\n")
