# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 09:31:45 2019

@author: DrEdC
"""

import pandas as pd
import numpy as np
import scipy.stats as st

def VR_test(data,test_what="price",sub_size=2,return_p=False):
    """
    This method take a array-like data as input and perform variance ratio test according to Lo and MacKinlay's algorithem.
    The test detects deviation from log-normal distribution in asset returns by comparing estimated variances from different holding periods
    This method allows array-like inputs for the choise of long-period variance and it returns the Z statistics or the p-values corresponding to each input
    """
    if isinstance(data,(pd.Series,np.ndarray,list)):
        P = pd.Series(data).astype(float)
        if not isinstance(P.index,(pd.DatetimeIndex)):
            P.index = pd.DatetimeIndex(P.index)
        P = P.sort_index()
    else:
        raise ValueError ("only support data type of pd.Series, np.array, or list")
    if np.isscalar(sub_size):
        sub_size = [sub_size]
    N = len(P)
    n = N-1
    result = []
    for ss in sub_size:
        m = N//ss-1
        mu = (np.log(P[-1]) - np.log(P[0]))/n
        va = (((np.log(P) - np.log(P).shift(1) - mu)**2).sum())/n
        sub_s = pd.Series([P.iat[ss*i] for i in range(0,N//ss)])
        vb = (((np.log(sub_s) - np.log(sub_s).shift(1) - ss*mu)**2).sum())/(ss*m)
        jb = vb/va-1
        z = np.sqrt(m*ss)*(jb/np.sqrt(2*(ss-1)))
        result.append(z)
    if len(sub_size) == 1:
        if return_p:
            return 2*(1-st.norm.cdf(abs(result[0])))
        else:
            return result[0]
    else:
        if return_p:
            return_s = pd.Series(2*(1-st.norm.cdf(np.abs(result))),index=sub_size,name="p-values")
        else:
            return_s = pd.Series(result,index=sub_size,name="Z-stat")
        return_s.index.name = "lvar_size"
        return return_s

def check_float(string):
    try:
        float(string)
        return True
    except:
        return False
    
def str2list(str_input,number=False,separator_list=[",",";"]):
    if str_input is None or str_input=="":
        return []
    if str_input[-1] not in separator_list:
        str_input += separator_list[0]
    return_list=[]
    temp_str=""
    for ch in str_input:
        if ch in separator_list:
            if temp_str.strip().isnumeric():
                return_list.append(int(temp_str.strip()))
            elif check_float(temp_str.strip()):
                return_list.append(float(temp_str.strip()))
            else:
                return_list.append(temp_str.strip())
            temp_str =""
        else:
            temp_str+=ch
    return return_list