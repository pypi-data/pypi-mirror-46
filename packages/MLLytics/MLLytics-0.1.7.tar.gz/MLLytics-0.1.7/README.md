# MLLytics

## Installation instructions 
```pip install MLLytics```
or
```python setup.py install```

## Update pypi instructions (for me)
Creates the package
```python setup.py sdist bdist_wheel```
Upload package
```twine upload --repository pypi *version_files*```

## Future
### Improvements and cleanup
* Allow figure size and font sizes to be passed into plotting functions
* Comment all functions and classes
* Add type hinting to all functions and classes (https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html)
* Example guides for each function in jupyter notebooks

### Cosmetic
* Fix size of confusion matrix 
* Check works with matplotlib 3
* Tidy up legends and annotation text on plots
* Joy plots
* Brier score for calibration plot

### Big push
* Cross Validation and plots (also repeated cross-validation)
* Scoring functions
* MultiClassMetrics class to inherit from ClassMetrics and share common functions
* More output stats in overviews
* Update reliability plot https://machinelearningmastery.com/calibrated-classification-model-in-scikit-learn/
* Tests
* Switch from my metrics to sklearn metrics where it makes sense? aka 
```fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])```
and more general macro/micro average metrics from: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html#sklearn.metrics.recall_score

## Contributing Authors
* Scott Clay
* David Sullivan