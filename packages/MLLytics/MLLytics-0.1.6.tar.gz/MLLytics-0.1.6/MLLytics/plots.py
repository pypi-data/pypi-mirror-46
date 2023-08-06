import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import itertools
from sklearn.metrics import confusion_matrix



def plot_roc_auc(fpr,tpr,threshold,youden=None):
    import matplotlib.cm as cm
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    import seaborn as sns
    from sklearn.metrics import auc
    
  
    sns.set_style("whitegrid")
    plt.figure(figsize=(7,7))

    plt.plot(fpr,tpr,c='k', zorder=1, linestyle='-' )
    plt.plot([-0.2,1.2],[-0.2,1.2], zorder=1, linestyle='--', color='k')
    plt.xlim([-0.05,1.05])
    plt.ylim([-0.05,1.05])
    plt.scatter(fpr,tpr, c=threshold, cmap = cm.viridis, edgecolors='k', linewidth=1.5, marker='o',
                linestyle='-',zorder=2 )
    
    plt.xlabel("FPR", fontsize=16)
    plt.ylabel("TPR", fontsize=16)
    
    auc = auc(fpr,tpr)
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.9)
    
    if youden is not None:
        plt.text(0.6,0.25,'AUC = '+str(auc)+'\nyouden_J_statistic = '+str(youden[0])+'\nthresehold = '+str(youden[1]), fontsize=12, bbox=props)
    else:
        plt.text(0.6,0.25,'AUC = '+str(auc), fontsize=12, bbox=props)
        

    
    plt.gca().tick_params(axis='both', which='major', labelsize=15)
    plt.gca().tick_params(axis='both', which='minor', labelsize=15)

    cbaxes = inset_axes(plt.gca(), width="30%", height="3%", loc= 'lower right',bbox_to_anchor=(-0.02, 0.05, 1, 1),
                       bbox_transform=plt.gca().transAxes,
                       borderpad=0) 
    plt.colorbar(cax=cbaxes, orientation='horizontal')
    plt.text(0.33, 1.4, 'Threshold', fontsize=10)
    plt.show()

def plot_rp(recall,prec,threshold):
    import matplotlib.cm as cm
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    import seaborn as sns
    sns.set_style("whitegrid")
    plt.figure(figsize=(7,7))

    plt.plot(recall,prec,c='k', zorder=1, linestyle='-' )
    #plt.plot([-0.2,1.2],[-0.2,1.2], zorder=1, linestyle='--', color='k')
    plt.xlim([-0.05,1.05])
    plt.ylim([-0.05,1.05])
    plt.scatter(recall,prec, c=threshold, cmap = cm.viridis, edgecolors='k', linewidth=1.5, marker='o',
                linestyle='-',zorder=2 )
    #plt.plot(C,B, c='k',linewidth=1.5, marker='o', linestyle='-' )

    f_scores = np.linspace(0.2, 0.8, num=4)
    lines = []
    labels = []
    for f_score in f_scores:
        x = np.linspace(0.01, 1)
        y = f_score * x / (2 * x - f_score)
        l, = plt.plot(x[y >= 0], y[y >= 0], color='k', alpha=0.5, linestyle='-.', zorder=1)
        plt.annotate('f1={0:0.1f}'.format(f_score), xy=(0.85, y[45] - 0.05))

    plt.xlabel('Recall', fontsize=16)
    plt.ylabel('Precision', fontsize=16)
        
    plt.gca().tick_params(axis='both', which='major', labelsize=15)
    plt.gca().tick_params(axis='both', which='minor', labelsize=15)

    cbaxes = inset_axes(plt.gca(), width="30%", height="3%", loc= 'lower left',bbox_to_anchor=(0.05, 0.05, 1, 1),
                       bbox_transform=plt.gca().transAxes,
                       borderpad=0) 
    plt.colorbar(cax=cbaxes, orientation='horizontal')
    plt.text(0.33, 1.4, 'Threshold', fontsize=10)
    plt.show()



def reliability_curve(y_true, y_score, bins=10, normalize=False):
    """Compute reliability curve

    Reliability curves allow checking if the predicted probabilities of a
    binary classifier are well calibrated. This function returns two arrays
    which encode a mapping from predicted probability to empirical probability.
    For this, the predicted probabilities are partitioned into equally sized
    bins and the mean predicted probability and the mean empirical probabilties
    in the bins are computed. For perfectly calibrated predictions, both
    quantities whould be approximately equal (for sufficiently many test
    samples).

    Note: this implementation is restricted to binary classification.

    Parameters
    ----------

    y_true : array, shape = [n_samples]
        True binary labels (0 or 1).

    y_score : array, shape = [n_samples]
        Target scores, can either be probability estimates of the positive
        class or confidence values. If normalize is False, y_score must be in
        the interval [0, 1]

    bins : int, optional, default=10
        The number of bins into which the y_scores are partitioned.
        Note: n_samples should be considerably larger than bins such that
              there is sufficient data in each bin to get a reliable estimate
              of the reliability

    normalize : bool, optional, default=False
        Whether y_score needs to be normalized into the bin [0, 1]. If True,
        the smallest value in y_score is mapped onto 0 and the largest one
        onto 1.


    Returns
    -------
    y_score_bin_mean : array, shape = [bins]
        The mean predicted y_score in the respective bins.

    empirical_prob_pos : array, shape = [bins]
        The empirical probability (frequency) of the positive class (+1) in the
        respective bins.


    References
    ----------
    .. [1] `Predicting Good Probabilities with Supervised Learning
            <http://machinelearning.wustl.edu/mlpapers/paper_files/icml2005_Niculescu-MizilC05.pdf>`_

    """
    if normalize:  # Normalize scores into bin [0, 1]
        y_score = (y_score - y_score.min()) / (y_score.max() - y_score.min())

    bin_width = 1.0 / bins
    bin_centers = np.linspace(0, 1.0 - bin_width, bins) + bin_width / 2

    y_score_bin_mean = np.empty(bins)
    empirical_prob_pos = np.empty(bins)
    for i, threshold in enumerate(bin_centers):
        # determine all samples where y_score falls into the i-th bin
        bin_idx = np.logical_and(threshold - bin_width / 2 < y_score,
                                 y_score <= threshold + bin_width / 2)
        # Store mean y_score and mean empirical probability of positive class
        y_score_bin_mean[i] = y_score[bin_idx].mean()
        empirical_prob_pos[i] = y_true[bin_idx].mean()
    return y_score_bin_mean, empirical_prob_pos

def plot_rely(y_score_bin_mean, empirical_prob_pos):
    plt.figure(0, figsize=(8, 8))
    plt.subplot2grid((3, 1), (0, 0), rowspan=2)
    plt.plot([0.0, 1.0], [0.0, 1.0], 'k', linestyle='--' , label="Perfect")
    plt.plot(y_score_bin_mean, empirical_prob_pos, label='method')

    #for method, (y_score_bin_mean, empirical_prob_pos) in reliability_scores.items():
    #    scores_not_nan = np.logical_not(np.isnan(empirical_prob_pos))
    #    plt.plot(y_score_bin_mean[scores_not_nan],
    #             empirical_prob_pos[scores_not_nan], label=method)
    plt.ylabel("Empirical probability")
    plt.legend(loc=0)

    plt.subplot2grid((3, 1), (2, 0))
    plt.hist(empirical_prob_pos, range=(0, 1), bins=5, label='method',histtype="step", lw=2)
    #for method, y_score_ in y_score.items():
    #    y_score_ = (y_score_ - y_score_.min()) / (y_score_.max() - y_score_.min())
    #    plt.hist(y_score_, range=(0, 1), bins=bins, label=method,
    #             histtype="step", lw=2)
    plt.xlabel("Predicted Probability")
    plt.ylabel("Count")
    #plt.legend(loc='upper center', ncol=2)
    plt.show()
    
def plot_confusion_matrix(label, pred, label_names,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    
    cm = confusion_matrix(label,pred)#,labels = [0,1,2])
    
    
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)
    sns.set_style("white")
    
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(label_names))
    plt.xticks(tick_marks, label_names, rotation=45)
    plt.yticks(tick_marks, label_names)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.show()