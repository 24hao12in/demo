"""
Kmeans with 3D plot 
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.metrics import  silhouette_score

src1 = './inter_games/allshader_gspan_output/25percent_result/WL/maxInCol/maxInCol_trainingdataset.csv'
data = pd.read_csv(src1, header = 'infer', index_col = 0)
X= data.T
  

labelsize = 25

#-------select number of components ----------------
pca = PCA()
pca.fit(X)
variance = pca.explained_variance_ratio_
var = np.cumsum(np.round(variance, 3))
print(var)

# plot for explained variance
fig, ax = plt.subplots(figsize=(8,4))
ax.grid()
plt.ylabel('cumulative explained variance', fontsize=labelsize-3)
plt.xlabel('# of features', fontsize=labelsize)

x = [i+1 for i in range(len(var))]
plt.xticks(np.arange(1, 28, step=2))  
plt.yticks(np.arange(0, 1.1, step=0.20))  
plt.ylim(0,1.1)
plt.tick_params(labelsize=labelsize)
plt.plot(x,var,marker='o')

pca = PCA(n_components=3)
pca_scale = pca.fit_transform(X)
pca_df_scale = pd.DataFrame(pca_scale, columns=['PCA0','PCA1','PCA2'])

#-------select k value------------------------------
sse = []
max_k=28
k_list = range(1, max_k)
for k in k_list:
    km = KMeans(n_clusters=k)
    km.fit(pca_df_scale)
    sse.append([k, km.inertia_])
    
pca_results_scale = pd.DataFrame({'Cluster': range(1,28), 'SSE': sse})
fig, ax2 = plt.subplots(figsize=(8,4))
ax2.grid()
plt.plot(pd.DataFrame(sse)[0], pd.DataFrame(sse)[1], marker='o')
plt.title('Number of Clusters vs Inertia', fontsize=labelsize)
plt.xlabel('# clusters', fontsize=labelsize)
plt.ylabel('Inertia', fontsize=labelsize)
#plt.xticks([1,4,7,10,13,16,19,22,25,28])
plt.xticks(np.arange(0, 28, step=3))  
plt.tick_params(labelsize=labelsize)

#-------------------------------------------------------


n_cluster =4
kmeans_pca_scale = KMeans(n_clusters=n_cluster, n_init=100, max_iter=300, init='k-means++', random_state=2).fit(pca_df_scale)
print('KMeans PCA Scaled Silhouette Score: {}'.format(silhouette_score(pca_df_scale, kmeans_pca_scale.labels_, metric='euclidean')))
labels_pca_scale = kmeans_pca_scale.labels_
centers= kmeans_pca_scale.cluster_centers_
clusters_pca_scale = pd.concat([pca_df_scale, pd.DataFrame({'pca_clusters':labels_pca_scale})], axis=1)
result = pca_df_scale

#--------------------------------------------------------------------
# Plot initialisation
my_color=clusters_pca_scale['pca_clusters'].astype('category').cat.codes
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(result['PCA0'], result['PCA1'], result['PCA2'], c=my_color, cmap='viridis', s=200)
#plt.colorbar()
ax.scatter(centers[:, 0], centers[:, 1],centers[:, 2], marker="x",c='black', s=400, alpha=1);  
# make simple, bare axis lines through space:
xAxisLine = ((min(result['PCA0']), max(result['PCA0'])), (0, 0), (0,0))
ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r')
yAxisLine = ((0, 0), (min(result['PCA1']), max(result['PCA1'])), (0,0))
ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r')
zAxisLine = ((0, 0), (0,0), (min(result['PCA2']), max(result['PCA2'])))
ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r')
ax.tick_params(labelsize=30)
ax.tick_params(size=30)
# label the axes
ax.set_xlabel("PC1",fontsize=20)
ax.set_ylabel("PC2",fontsize=20)
ax.set_zlabel("PC3",fontsize=20)
ax.set_title("KMEANS result on 3 principle components")
plt.show()