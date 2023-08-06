import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import StringIO

# Metaphlan 2.2.0 & 12.50h & (1.66GB) & 2.13h & (1.44GB)\\
# FOCUS CAMI & 13.45h & (4.99GB) & 2.34h & (4.99GB)\\
# Quikr & 16.32h & (26.12GB) & 2.12h & (24.12GB)\\
# mOTU 1.1 & 19.83h & (1.19GB) & 3.82h & (1.19GB)\\
# CommonKmers & 76.82h & (26.03GB) & 11.28h & (24.16GB)\\
# MetaPhyler 1.25 & 119.51h & (2.56GB) & 31.16h & (6.85GB)\\
# TIPP 2.0.0 & 151.01h & (67.51GB) & 32.01h & (81.53GB)\\

# s = StringIO("""     time     memory
# Metaphlan    12.50   1.66
# FOCUS        13.45   4.99
# Quikr        16.32  26.12
# mOTU         19.83   1.19
# CommonKmers  76.82  26.03
# MetaPhyler  119.51   2.56
# TIPP        151.01   67.5""")

s = StringIO("""     time     memory
Metaphlan   2.13     1.44
FOCUS       2.34     4.99
Quikr       2.12    24.12
mOTU        3.82     1.19
CommonKmers 11.28   24.16
MetaPhyler  31.16    6.85
TIPP        32.01   81.53""")


def plot_time_memory(time, memory, tool):
    # print(dict(zip(range(len(tool)), tool)))
    # exit()
    # xx = map(tool, range(len(tool)))
    # print(dict(xx))
    # exit()


    time_label = 'Time (hours)'
    memory_label = 'Memory (GB)'
    df = pd.DataFrame({'tool': tool, time_label: time, memory_label: memory}, columns=[time_label, memory_label], index=tool).sort_values(by=[time_label])
    # df.set_index('tool', inplace=True)
    # df.sort_values(by=[time_label], inplace=True)
    # df = pd.read_csv(s, index_col=0, delimiter=' ', skipinitialspace=True)
    # df.set_index(["a", "b", "c", "d", "e", "f", "g"], inplace=True)
    print(df.index.tolist())
    print(df.columns)
    print(df)
    exit()
    df.columns = ['Time (hours)', 'Memory (GB)']

    ax = df.plot(kind='bar', secondary_y='Memory (GB)', mark_right=False, zorder=20)
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='lightgrey', zorder=0)
    ax.set_ylabel('Time (hours)')
    plt.setp(ax.get_xticklabels(), fontsize=9, rotation=15)

    ax2 = ax.twinx()
    ax2.set_ylabel('Memory (GB)', labelpad=23)
    ax2.yaxis.set_ticks([])

    plt.savefig('test.pdf', dpi=100, format='pdf', bbox_inches='tight')


plot_time_memory([11.28, 2.13, 32.01], [24.16, 1.44, 81.53], ['a', 'b', 'c'])
