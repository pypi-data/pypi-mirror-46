# MLLytics

python setup.py sdist bdist_wheel

Creates the package

python setup.py install

Installs the package from source

twine upload --repository pypi *0.1.4*

Upload package


To do:

* Fix size of confusion matrix
* Update reliability plot https://machinelearningmastery.com/calibrated-classification-model-in-scikit-learn/
* Repeated cross-validation (and x-val in general)
* Extra output metrics
* Brier score for calibration plot
* joy plots
* switch to sklearn micro average metrics? https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html#sklearn.metrics.recall_score