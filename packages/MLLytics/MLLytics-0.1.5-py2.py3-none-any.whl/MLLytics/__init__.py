import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import AffinityPropagation
from collections import OrderedDict


class ClassMetrics():

    def __init__(self, prob,label, thres_bins=110):
        
    
        self.threshold = np.empty(0)
        self.tpr = np.empty(0)
        self.fpr = np.empty(0)
        self.tnr = np.empty(0)
        self.prec = np.empty(0)
        self.recall = np.empty(0)
        self.acc = np.empty(0)
        
        self.tp = np.empty(0)
        self.tn = np.empty(0)
        self.fp = np.empty(0)
        self.fn = np.empty(0)
        
        for thres in range(0,100,1):
            th = np.zeros(len(label))
            th[(prob>(thres/100.))] = 1

            _tp = len(th[(label==1)&(th==1)])
            _tn = len(th[(label==0)&(th==0)])
            _fp = len(th[(label==0)&(th==1)])
            _fn = len(th[(label==1)&(th==0)])

            _tpr = _tp / (_tp + _fn)
            _fpr = _fp / (_fp + _tn)
            _tnr = _tn / (_tn + _fp)

            try:
                _precision = _tp / (_tp + _fp)
            except:
                _precision = 1
            _recall = _tp / (_tp + _fn)
            _acc = (_tp + _tn)/len(label)

            self.threshold = np.append(self.threshold, (thres/100.))
            
            self.tpr = np.append(self.tpr, _tpr)
            self.fpr = np.append(self.fpr, _fpr)
            self.tnr = np.append(self.tnr, _tnr)
            
            self.tp = np.append(self.tp, _tp)
            self.tn = np.append(self.tn, _tn)
            self.fp = np.append(self.fp, _fp)
            self.fn = np.append(self.fn, _fn)
            
            self.prec = np.append(self.prec, _precision)
            self.recall = np.append(self.recall, _recall)
            self.acc = np.append(self.acc, _acc)
        
    def calc_youden_J_statistic(self):
        _J = self.tpr + self.tnr - 1.
        _youden_J = _J.max()
        _youden_J_threshold = self.threshold[_J.argmax()] 
        
        return [_youden_J, _youden_J_threshold]
    
    def give_threshold(self, given_threshold=0.5):
        _arg = np.argwhere(self.threshold==0.5)
        
              
        _recall = np.asscalar(self.recall[_arg])
        _precision = np.asscalar(self.prec[_arg])
        _acc = np.asscalar(self.acc[_arg])
        _tp = np.asscalar(self.tp[_arg])
        _tn = np.asscalar(self.tn[_arg])
        _fp = np.asscalar(self.fp[_arg])
        _fn = np.asscalar(self.fn[_arg])
        _tpr = np.asscalar(self.tpr[_arg])
        _fpr = np.asscalar(self.fpr[_arg])
        _tnr = np.asscalar(self.tnr[_arg])
        
        return {'threshold':given_threshold,
                'recall':_recall ,
                'precision':_precision,
				'accuracy':_acc,
                'TP':_tp,
                'TN':_tn,
                'FP':_fp,
                'FN':_fn,
                'TPR':_tpr,
                'FPR':_fpr,
                'TNR':_tnr
        }
        
                

class MultiClassMetrics():

    def __init__(self, prob,pred,label):
        
        n_classes = len(prob.keys())
        n_labels = len(np.unique(label))
        n_pred = len(np.unique(pred))
        
        if n_classes == n_labels == n_pred:
            print('GOOD TO GO')
        
        multi = {}
        for i, j in enumerate(prob.keys()):

            _label = label.copy()
            _label[label==i] = 1
            _label[label!=i] = 0
            
            _pred = pred.copy()
            _pred[pred==i] = 1
            _pred[pred!=i] = 0
            
            multi[j] = ClassMetrics(prob[j], _label)
        
        self.multi = multi
        
        
        self.tp = len(pred[(label==1)&(pred==1)])
        self.tn = len(pred[(label==0)&(pred==0)])
        self.fp = len(pred[(label==0)&(pred==1)])
        self.fn = len(pred[(label==1)&(pred==0)])

        self.tpr = self.tp / (self.tp + self.fn)
        self.fpr = self.fp / (self.fp + self.tn)
        self.tnr = self.tn / (self.tn + self.fp)


        try:
            self.precision = self.tp / (self.tp + self.fp)
        except:
            self.precision = 1
        
        self.recall = self.tp / (self.tp + self.fn)
        self.acc = (self.tp + self.tn)/len(pred)
        
        
    def give_overview(self):
        _arg = np.argwhere(self.threshold==0.5)
        
        
        return {'recall':self.recall ,
                'precision':self.precision,
                'accuracy':self.acc,
                'TP':self.tp,
                'TN':self.tn,
                'FP':self.fp,
                'FN':self.fn,
                'TPR':self.tpr,
                'FPR':self.fpr,
                'TNR':self.tnr
        }
def ftr_importance(cols, imps):
    d={}
    for i in range(0, len(cols)):
        d[cols[i]] = imps[i]*100.
    
    d_values = sorted(d.values()) 
    d_keys = sorted(d, key=d.get)
    d_keys.reverse()
    d_values.reverse()
    
    return d_keys, d_values

def plot_ftr_importance(cols, imps, n=None):
    
    d_keys, d_values = ftr_importance(cols, imps)
    
    if n is not None:
        d_keys = d_keys[:n]
        d_values = d_values[:n]
        
    sns.set(style="whitegrid")

    plt.figure(figsize=(9,6))
    ax = sns.barplot(y=d_keys, x=d_values, orient = 'h',palette=("viridis"))

    ax.set_title('Top 10 Features',fontsize=20)
    ax.set_xlabel('Importance (%)', fontsize=18)

    ax.tick_params(axis='both', which='major', labelsize=14)
    #fig = plt.gcf()
    #plt.xticks(rotation=90)



def cluster_corr(corr):
    
    _corr = corr.abs()
    
    
    _clustering = AffinityPropagation().fit(_corr)

    _corr['cluster'] = _clustering.labels_
    

    _cols = list(_corr.columns)
    _clus = list(_clustering.labels_)
    

    
    order = {}
    for i in range(0,len(_clus)): 
        order[_cols[i]] = _clus[i]
        

    x = OrderedDict(sorted(order.items(), key=lambda x: x[1]))
    clus_corr = _corr.reindex(x.keys())[list(x.keys())]
    
    return x, clus_corr

def plot_cluster_corr(x, clus_corr):
    sns.set(style="white")
    
    corr = clus_corr
    
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    f, ax = plt.subplots(figsize=(9, 7))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    sns.heatmap(corr, cmap=cmap, square=True, cbar_kws={"shrink": .75}, vmin=0., vmax=1.)
    ax.set_title('Clustered Correlation Matrix', fontsize=14)

    j = 0
    k = 0
    for i in range(0,len(set(x.values()))):
        z = sum(value == i for value in x.values())
        k+=z
        l=k-z
     
        if i == 0:
            lt_a = lt_c = 3
            lt_b = lt_d = 2
        elif i == (len(set(x.values())) - 1):
            lt_a = lt_c = 2
            lt_b = lt_d = 5        
        else:
            lt_a = lt_b = lt_c = lt_d = 2
       
        ax.hlines(l,l,k, color='yellow', linewidth=lt_a)
        ax.hlines(k,l,k, color='yellow', linewidth=lt_b)
        ax.vlines(l,l,k, color='yellow', linewidth=lt_c)
        ax.vlines(k,l,k, color='yellow', linewidth=lt_d)    



def corr_matrix_triangle(_corr):
    
    ## corr matrix triangle
    sns.set(style="white")
    
    # Generate a mask for the upper triangle
    mask = np.zeros_like(_corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(9, 7)) 
    
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    
    sns.heatmap(_corr, mask=mask, cmap=cmap, square=True, cbar_kws={"shrink": .75}, vmin=-1., vmax=1.)
    ax.set_title('Correlation Matrix', fontsize=14)            
        
def corr_with_label(df, label):
    _df = df.select_dtypes(include=[np.number])
    _x = {}
    for col in _df.columns:
        print(col, _df[col].corr(_df[label]))
        _x[col] = (_df[col].corr(_df[label]))
    
    return _x

def plot_corr_hist(corr):
    plt.hist(np.array(list(a.values())), bins=10)
    plt.xlim([-1,1])
        
        		
 