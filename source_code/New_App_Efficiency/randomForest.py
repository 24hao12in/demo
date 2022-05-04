"""
RF with cross validation

"""
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import auc
from sklearn.metrics import RocCurveDisplay
from sklearn.model_selection import StratifiedKFold
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import average_precision_score, precision_recall_curve
from sklearn.metrics import auc, plot_precision_recall_curve

path = './new_label_game/shader_project_more_games_lip/'
src = path + 'map_back/training/dataset_breakAll1.csv'

src = path + 'map_back/training/dataset_detail_smallpattern_2ndlabeling.csv'
data = pd.read_csv(src, index_col =0 )
X = data.iloc[:, :43]
X = X.reindex(sorted(X.columns), axis=1)
y = data['class']

##-------------------random downsampling-------------------
#df_class_0_under = df_class_0.sample(count_class_1)
#df_test_under = pd.concat([df_class_0_under, df_class_1], axis=0)
#
#print('Random under-sampling:')
#print(df_test_under.target.value_counts())
##-----------------------------------


X = X.to_numpy()
y = y.to_numpy()

cv = StratifiedKFold(n_splits=4,shuffle = True,random_state=6)
tprs = []
aucs = []
mean_fpr = np.linspace(0, 1, 100)
fig, ax = plt.subplots( figsize = (8,6))

classifier=RandomForestClassifier(n_estimators=200,max_depth=15,max_leaf_nodes=20,min_samples_leaf=1)#

for i, (train, test) in enumerate(cv.split(X, y)):
    classifier.fit(X[train], y[train])
    viz = RocCurveDisplay.from_estimator(
        classifier,
        X[test],
        y[test],
        name="ROC fold {}".format(i),
        alpha=0.6,
        lw=4,
        ax=ax
        )
    y_pred=classifier.predict(X[test])
    print("Accuracy:", metrics.accuracy_score(y[test], y_pred))

#    print("average_precision_score:",average_precision_score(y[test], y_pred))
#    print("roc_auc_score:", roc_auc_score(y[test], y_pred))

    #fpr false positive rate, tpr: true positive rate 
    interp_tpr = np.interp(mean_fpr, viz.fpr, viz.tpr)
    interp_tpr[0] = 0.0
    tprs.append(interp_tpr)
    aucs.append(viz.roc_auc)
    
    precision, recall, thresholds = precision_recall_curve(y[test], y_pred)
    auc_precision_recall = auc(recall, precision)
    print("pr_auc:",auc_precision_recall)
    fpr, tpr, thresholds = roc_curve(y[test], y_pred)
    roc_auc_value = auc(fpr, tpr)
    print(roc_auc_value)
    
ax.plot([0, 1], [0, 1], linestyle="--", lw=4, color="r", label="Chance", alpha=0.8)


mean_tpr = np.mean(tprs, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs)
ax.plot(
    mean_fpr,
    mean_tpr,
    color="b",
    label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc),
    lw=6,
    alpha=0.8,
)

std_tpr = np.std(tprs, axis=0)
tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
ax.fill_between(
    mean_fpr,
    tprs_lower,
    tprs_upper,
    color="grey",
    alpha=0.5,
    label=r"$\pm$ 1 std. dev.",
)

ax.set(
    xlim=[-0.05, 1.05],
    ylim=[-0.05, 1.05],   
)
plt.title("Receiver operating characteristic", fontsize=20)
plt.xlabel('False Positive Rate (positive label: 1)', fontsize=18)
plt.ylabel("True Positive Rate (positive label: 1)", fontsize=18)
plt.tick_params(labelsize=18)    
plt.legend(loc="lower right", fontsize=10) 
plt.show()    

    