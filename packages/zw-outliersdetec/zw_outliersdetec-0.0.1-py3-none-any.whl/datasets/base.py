#导入自带的数据集
"""
Base IO code for all datasets
"""
import pandas as pd
import numpy as np
from os.path import *

#__module_path = dirname(__file__)

def load_hbk():
    """Load and return the hbk dataset (classification).
    =================   ==============
    Samples total                75
    Dimensionality               4
    Features                     real
    =================   ==============
    Returns
    -------
    data : pd.readcsv
    """
    #filename = join(__module_path,'data','hbk.csv')
    #data_train = pd.read_csv(filename, sep=',')
    data_train = pd.read_csv('hbk.csv', sep=',')
    return data_train


def load_isolet(return_Label=False):
    """Load and return the isolet dataset (classification).
    =================   ==============
    Samples total                190
    Dimensionality               617
    Features                     real
    =================   ==============
    parameters
    return_Label:if return_Label=False,Labels will not return
    ---------
    Returns
    data :pd.readcsv
    """
    #filename = join(__module_path,'data', 'isolet.csv')
    data= pd.read_csv('isolet.csv', sep=',')
    label = data.iloc[:, -1]
    data_train=data.drop('Label',axis=1)
    if return_Label==False:
        return data_train
    else:
        return data_train,label


def load_shuttle(return_Label=False):
    """Load and return the shuttle dataset (classification).
    =================   ==============
    Samples total                14500
    Dimensionality               9
    Features                     real
    =================   ==============
    parameters
    return_Label:if return_Label=False,Labels will not return
    ---------
    Returns
    data :pd.readcsv
    """
    #filename=join(__module_path, 'data','shuttle.csv')
    data= pd.read_csv('shuttle.csv', sep=',')
    label = data.iloc[:, -1]
    data_train=data.drop('Label',axis=1)
    if return_Label==False:
        return data_train
    else:
        return data_train,label

def load_TS_chfdb_1():
    """Load and return the ECG dataset (classification).
    =================   ==============
    Samples total                3750
    Dimensionality               1
    Features                     real
    =================   ==============
    Returns
    data :array
    --------
    note:the length of sequence is 250
    """
    #filename = join(__module_path,'data', 'TS_chfdb_1.csv')
    data = np.genfromtxt('TS_chfdb_1.csv', delimiter=',')
    return data

def load_TS_ECG108_1():
    """Load and return the ECG dataset (classification).
    =================   ==============
    Samples total                3600
    Dimensionality               1
    Features                     real
    =================   ==============
    Returns
    data :array
    --------
    note:the length of sequence is 400
    """
    #filename = join(__module_path,'data', 'TS_ECG108_1.csv')
    data = np.genfromtxt('TS_ECG108_1.csv', delimiter=',')
    return data


def load_TS_ECG108_2():
    """Load and return the ECG dataset (classification).
    =================   ==============
    Samples total                3600
    Dimensionality               1
    Features                     real
    =================   ==============
    Returns
    data :array
    --------
    note:the length of sequence is 400
    """
    #filename = join(__module_path,'data', 'TS_ECG108_2.csv')
    data = np.genfromtxt('TS_ECG108_2.csv', delimiter=',')
    return data

def load_TS_ECG0606_1():
    """Load and return the ECG dataset (classification).
    =================   ==============
    Samples total                2299
    Dimensionality               1
    Features                     real
    =================   ==============
    Returns
    data :array
    --------
    note:the length of sequence is 100,win-size=100
    """
    #filename = join(__module_path,'data', 'TS_ECG0606_1.csv')
    data = np.genfromtxt('TS_ECG0606_1.csv', delimiter=',')
    return data