import os
import json
import time
import argparse
from itertools import chain
from datetime import datetime

import pandas as pd
from sklearn.externals import joblib
from IPython.display import display
from time import strftime, gmtime

#==============================================================================
# 时间相关
#==============================================================================
def log_start_time(fname):
    global st_time
    st_time = time()
    print("""
#=================================================================================
# START !!! {}    PID: {}    Time: {}
#=================================================================================
""".format(fname.split("/")[-1], os.getpid(), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    #    send_line(f'START {fname}  time: {elapsed_minute():.2f}min')

    return

def log_end_time(fname):
    print("""
#=================================================================================
# SUCCESS !!! {}  Total Time: {} [s]
#=================================================================================
""".format(fname.split("/")[-1], _elapsed_minute()))
    return

def _elapsed_minute():
    return int(time() - st_time)

def now():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())
#==============================================================================
# 文件相关
#==============================================================================
def csv_2_pickle(paths: list):
    """Convert csv files into pickle format files.

     Parameters
     ----------
     paths: list
     	Csv file paths.

     Examples
     --------
     PATH = Path("data/raw/")
     CSV = [str(i) for i in list(PATH.glob("*.csv"))]
     csv_2_pickle(CSV)
     """
    for path in paths:
        data = pd.read_csv(path)
        joblib.dump(data, path.split('csv')[0] + "p")

def loadConfig(path):
    parser  = argparse.ArgumentParser()
    parser.add_argument('--config', default=path)
    options = parser.parse_args()
    config  = json.load(open(options.config))
    return config

def mkdir(path: str):
    """Create directory.

     Create directory if it is not exist, else do nothing.

     Parameters
     ----------
     path: str
     	Path of your directory.

     Examples
     --------
     mkdir("data/raw/train")
     """

    try:
        os.stat(path)
    except:
        os.mkdir(path)

def remove_temporary_files(folder_path: str):
    """Remove files begin with ".~".

     Parameters
     ----------
     folder_path: str
        Folder path which you want to clean.

     Examples
     --------
     remove_temporary_files("data/raw/")
     """
    '''
        Parameter
        remove files begin with ".~"
        ---------
        folder_path: str
    '''
    num_of_removed_file = 0
    for fname in os.listdir(folder_path):
        if fname.startswith("~") or fname.startswith("."):
            num_of_removed_file += 1
            os.remove(folder_path + '/'+ fname)
    print("{0} file have been removed".format(num_of_removed_file))
#==============================================================================
# 展示相关
#==============================================================================
def display_pro(data: pd.DataFrame, n=5):
    """Pro version of display function.

     Display [memory usage], [data shape] and [first n rows] of a pandas dataframe.

     Parameters
     ----------
     data: pandas dataframe
        Pandas dataframe to be displayed.
     n: int
        First n rows to be displayed.

     Example
     -------
     import pandas as pd
     from sklearn.datasets import load_boston
     data = load_boston()
     data = pd.DataFrame(data.data)
     display_pro(data)
     """

    '''
        Parameters
        ----------
        data: pandas dataframe


        Returns
        -------
            None
    '''
    memory = memory_usage(data, 0)
    print("Data shape   : {}".format(data.shape))
    display(data[:n])

def memory_usage(data: pd.DataFrame, detail=1):
    """Show memory usage.

     Parameters
     ----------
     data: pandas dataframe
     detail: int, optinal (default = 1)
        0: show memory of each column
        1: show total memory

     Examples
     --------
     import pandas as pd
     from sklearn.datasets import load_boston
     data = load_boston()
     data = pd.DataFrame(data.data)
     memory = memory_usage(data)
     """
    if detail:
        display(data.memory_usage())
    memory = data.memory_usage().sum() / (1024*1024)
    print("\nMemory usage : {0:.2f}MB".format(memory))
    return memory


#==============================================================================
# 功能相关
#==============================================================================
def find_a_not_in_b(a : list, b : list):
    '''找到a中存在b中不存在的元素

        Parameter
        ---------

        Return
        ------
        list
    '''
    # isinstance(a, float)是为了防止[空值]的情况
    if  isinstance(a, float) or isinstance(b, float):
        return a
    return [i1 for i1 in a if i1 not in b]

def find_a_in_b(a : list, b : list):
    '''找到a中存在b中也存在的元素

        Parameter
        ---------

        Return
        ------
        list
    '''
    # isinstance(a, float)是为了防止[空值]的情况
    if  isinstance(a, float) or isinstance(b, float):
        return []
    return [i1 for i1 in a if i1 in b]

def sum_list_in_list(list_in_list):
    '''将 list in list 变为 list
        Parameter
        ---------
        list_in_list: list

        Return
        ------
        list

        Example
        -------
        sum_list([['1','2'], ['2']]) -> ['1', '2', '2']
    '''
    return list(chain.from_iterable(list_in_list))

def unique_list_in_list(list_in_list):
    '''将 list in list 变为 list
        Parameter
        ---------
        list_in_list: list

        Return
        ------
        list

        Example
        -------
        unique_list_in_list([['1','2'], ['2']]) -> ['1', '2']
    '''
    li = sum_list_in_list(list_in_list)
    return list(set(li))

def is_primary_key(data, column_list):
    '''Verify if columns in column list can be treat as primary key

        Parameter
        ---------
        data: pandas dataframe

        column_list: list_like
                     column names in a list

        Return
        ------
        boolean: if true, these columns are unique in combination and can be used as a key
                 if false, these columns are not unique in combination and can not be used as a key
    '''

    return data.shape[0] == data.groupby(column_list).size().reset_index().shape[0]

def is_identical(col_1, col_2):
    '''判断数据集的两列是否一致

        Parameters
        ----------
        data: dataframe
        col_1: string
        col_2: string

        Return
        ------
        True、False
    '''
    if sum(col_1 == col_2) / len(col_1) == 1:
        return True
    return False

def reverse_dict(x : dict):
    '''翻转一个dict

        Parameters
        ----------
        x: dict

        Return
        ------
        dict
    '''
    return {v:k for k, v in x.items()}

def min_max(x):
    return min(x), max(x)
