import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import AffinityPropagation
from collections import OrderedDict
from matplotlib import cm

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
        
        for thres in range(0,101,1):
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
        _arg = np.argwhere(self.threshold==given_threshold)
        
              
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
        
        self.n_classes = len(prob.keys())
        self.n_labels = len(np.unique(label))
        self.n_pred = len(np.unique(pred))
        self.n_obs = len(pred)
        self.accuracy = len(pred[pred==label])/len(pred)
        
        
        count_uniques = np.bincount(pred)
        ii = np.nonzero(count_uniques)[0]
        self.class_counts = {}
        for i in range(0,len(count_uniques)):
            self.class_counts[str(ii[i])] = count_uniques[ii][i]
        
        
        if self.n_classes == self.n_labels == self.n_pred:
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
        self.micro_macro()
        
    def micro_macro(self):

        self.precision = {'macroA':np.empty(0),
                          'macroB':np.empty(0),
                          'micro':np.empty(0)
                         }
        
        self.recall    = {'macroA':np.empty(0),
                          'macroB':np.empty(0),
                          'micro':np.empty(0)
                         }
        
        self.tpr = {'macroA':np.empty(0),
                    'macroB':np.empty(0),
                    'micro':np.empty(0)
                    }
        
        self.fpr = {'macroA':np.empty(0),
                    'macroB':np.empty(0),
                    'micro':np.empty(0)
                    }
        
        self.threshold = np.empty(0)
        

        for j in range(0,len(self.multi[list(self.multi.keys())[0]].threshold)):
            
            _prec_macroA = 0
            _prec_macroB = 0
            _recall_macroA = 0
            _recall_macroB = 0
            _tpr_macroA = 0
            _tpr_macroB = 0
            _fpr_macroA = 0
            _fpr_macroB = 0
            
            _tp = 0
            _fp = 0
            _fn = 0
            _tn = 0
            
            for i in self.multi.keys():
                _prec_macroA += (self.multi[i].prec[j]/self.n_classes)
                _recall_macroA += (self.multi[i].recall[j]/self.n_classes)
                _tpr_macroA += (self.multi[i].tpr[j]/self.n_classes)
                _fpr_macroA += (self.multi[i].fpr[j]/self.n_classes)                
                
                _prec_macroB += (self.multi[i].prec[j]*(self.class_counts[i]/self.n_obs))
                _recall_macroB += (self.multi[i].recall[j]*(self.class_counts[i]/self.n_obs))          				
                _tpr_macroB += (self.multi[i].tpr[j]*(self.class_counts[i]/self.n_obs))   
                _fpr_macroB += (self.multi[i].fpr[j]*(self.class_counts[i]/self.n_obs))                   
                
                _tp += (self.multi[i].tp[j])
                _fp += (self.multi[i].fp[j])     
                _fn += (self.multi[i].fn[j])
                _tn += (self.multi[i].tn[j])
            
            self.threshold = np.append(self.threshold, self.multi['0'].threshold[j])
            
            self.precision['macroA'] = np.append(self.precision['macroA'], _prec_macroA)
            self.recall['macroA'] = np.append(self.recall['macroA'], _recall_macroA)    
            self.tpr['macroA'] = np.append(self.tpr['macroA'], _tpr_macroA)   
            self.fpr['macroA'] = np.append(self.fpr['macroA'], _fpr_macroA)               
            
            self.precision['macroB'] = np.append(self.precision['macroB'], _prec_macroB)
            self.recall['macroB'] = np.append(self.recall['macroB'], _recall_macroB)    
            self.tpr['macroB'] = np.append(self.tpr['macroB'], _tpr_macroB)   
            self.fpr['macroB'] = np.append(self.fpr['macroB'], _fpr_macroB)                   

            
            if (_tp != 0) and (_fp != 0):
                self.precision['micro']  = np.append(self.precision['micro'], _tp /(_tp + _fp))
            else:
                self.precision['micro'] = np.append(self.precision['micro'], 1.0)
            
            self.recall['micro']  = np.append(self.recall['micro'], _tp /(_tp + _fn))  
            self.fpr['micro'] = np.append(self.fpr['micro'], _fp/ (_fp + _tn))
            self.tpr['micro'] = np.append(self.tpr['micro'], _tp /(_tp + _fn))       

    
    def give_threshold(self, given_threshold=0.5, method='micro'):
        _arg = np.argwhere(self.threshold==given_threshold)
        
        
        _recall = np.asscalar(self.recall[method][_arg])
        _precision = np.asscalar(self.precision[method][_arg])
        _tpr = np.asscalar(self.tpr[method][_arg])
        _fpr = np.asscalar(self.fpr[method][_arg])
        
        
        _acc = self.accuracy
        
        return {'threshold':given_threshold,
                'recall':_recall ,
                'precision':_precision,
                'accuracy':_acc,
                'TPR':_tpr,
                'FPR':_fpr
        }
		
    def calc_youden_J_statistic(self, method='micro'):
        _J = self.tpr[method] + self.tnr[method] - 1.
        _youden_J = _J.max()
        _youden_J_threshold = self.threshold[_J.argmax()] 
        
        return [_youden_J, _youden_J_threshold]


   


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
    #cmap = sns.diverging_palette(20, 10, as_cmap=True)
    cmap = cm.BuPu
    
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
       
        ax.hlines(l,l,k, color='k', linewidth=lt_a)
        ax.hlines(k,l,k, color='k', linewidth=lt_b)
        ax.vlines(l,l,k, color='k', linewidth=lt_c)
        ax.vlines(k,l,k, color='k', linewidth=lt_d)    



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
        
        		
 