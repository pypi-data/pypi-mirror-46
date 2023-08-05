# -*- coding: utf-8 -*-
# Author: guoyang14
# Date: 28 Apr 2019
# 单变量ks

import pandas as pd
from sklearn.metrics import roc_curve

def Univariate_KS(
         ks_datain
        ,ks_y = ''
        ,ks_list = []
        ,pos_label = 1
        ):
    
    # ks_list
    if ks_list == []:
        datatp = ks_datain.dtypes
        ks_list = set(list(datatp[datatp != 'object'].index)) - set([ks_y])
    
    def calc_ks(ks_x):
        sub_set = ks_datain[[ks_y, ks_x]].dropna()
        fpr, tpr, thresholds = roc_curve(sub_set[ks_y], sub_set[ks_x], pos_label = pos_label)
        w = tpr - fpr
        
        w_max = round(w.max(), 4)
        w_min = round(w.min(), 4)
        
        return ks_x, max(abs(w_max), abs(w_min)), (w_max, w_min),'positive' if abs(w.max()) > abs(w.min()) else 'negative'
        
    ks_df = pd.DataFrame(list(map(calc_ks, ks_list)), columns=['var','ks_value_abs','ks_value(positive, negative)','direction']).\
            sort_values('ks_value_abs', ascending = False).reset_index(drop = True)            

    return ks_df

# test
if __name__ == '__main__':
    
    datain_test = pd.read_csv('http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt')
    Univariate_KS(datain_test, ks_y = 'survived')
