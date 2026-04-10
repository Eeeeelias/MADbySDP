In this folders, I store the model files to the different sklearn classifiers used to predict different bone grades.
The classifiers in this directory are all generated using one of two function calls:
```python
model = LogisticRegression(penalty='l1', solver='saga', l1_ratio=0.5, max_iter=1000, class_weight='balanced')
```
or 
```python
model = LogisticRegression(penalty='l1', solver='saga', l1_ratio=0.5, max_iter=1000)
```

Models that contain the keyword `balanced` are made using the first call since their weights are balanced according to
the sklearn method.

The first keyword in the model name can be either `tibia` or `radius` referencing the respective bone they were trained on.

The second keyword can be either `new` or `old` referencing the machine the model was trained on.
