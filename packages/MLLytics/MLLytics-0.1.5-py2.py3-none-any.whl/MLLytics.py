class ClassMetrics():

    def __init__(self, prob,label, thres_bins=110):
        
    
        self.threshold = np.empty(0)
        self.tpr = np.empty(0)
        self.fpr = np.empty(0)
        self.tnr = np.empty(0)
        self.prec = np.empty(0)
        self.recall = np.empty(0)
        
        for thres in range(0,110,1):
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

            self.threshold = np.append(self.threshold, (thres/100.))
            
            self.tpr = np.append(self.tpr, _tpr)
            self.fpr = np.append(self.fpr, _fpr)
            self.tnr = np.append(self.tnr, _tnr)
            
            self.prec = np.append(self.prec, _precision)
            self.recall = np.append(self.recall, _recall)
        
    def calc_youden_J_statistic(self):
        _J = self.tpr + self.tnr - 1.
        _youden_J = _J.max()
        _youden_J_threshold = self.threshold[_J.argmax()] 
        
        return [_youden_J, _youden_J_threshold]
        
        