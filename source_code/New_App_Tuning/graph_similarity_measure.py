
"""
WL kernel to compare fsm from each game 
step1: read all distinct fsm from each game 
step2: call the library to compute kernel matrix from one game to the rest of games 
step3: find the max kernel value of each fsm in targeted game to all the other games

"""
from __future__ import print_function
print(__doc__)


from grakel.kernels import WeisfeilerLehman, VertexHistogram

import os 
import pandas as pd

src1 = './inter_games/allshader_gspan_output/25percent_result/'
dst = src1 + 'WL/'  
if(os.path.isdir(dst)==False):
        os.mkdir(dst)
        
game_folders = [i for i in os.listdir(src1) if i.startswith('f') ]
df_f = pd.DataFrame(game_folders)
df_f.to_csv(dst + 'folder_info.csv', index = True)

actual_game =[]
graph_all = []
for idx, game_folder in enumerate(game_folders):
    print(game_folder)
    src_game = src1 + game_folder +'/' 
    # Use distinct edgelist and nodelist of gSpan result
    shader_folder = 'sub_iso_result'   # for shader_folder in shader_folders:
    src_unfold = src1 + game_folder +'/' + shader_folder + '/' 
    
    if(os.path.isdir(src_unfold)):   
        graph_single = []
        graph_len = []
        actual_game.append(game_folder)
        edgefiles = [i for i in os.listdir(src_unfold+'edgelist/') if i.endswith('.csv')]
        nodefiles = [i for i in os.listdir(src_unfold+'hash/') if i.endswith('.csv')]
    
        for idx in range(len(edgefiles)):
            graph_edge=set()
            # node graph 
            ngc = dict()
            # edge line 
            elc = dict()
            # dictionary of labels for nodes
            node_labels = dict()
            # dictionary of labels for edges
            edge_labels = dict()
            edges_path = src_unfold + 'edgelist/' + edgefiles[idx]
            with open(edges_path, "r") as f:
                for (i, line) in enumerate(f, 1):
                    edge = line[:-1].replace(' ', '').split(",")
                    elc[i] = (int(edge[0]), int(edge[1]))
                    graph_edge.add(elc[i])

            

            node_labels_path= src_unfold + 'hash/' + edgefiles[idx].split("edgelist")[0]
            with open(node_labels_path, "r") as f:
                for (i, line) in enumerate(f, 1):
                    node_labels[int(line.split(',')[0])] = line.split(',')[1]
            
            for each in graph_edge:
                edge_labels[each] = 0
            
            graph_single.append([graph_edge, node_labels, edge_labels])
        graph_len.append(len(edgefiles))  
        graph_all.append(graph_single)
        

#-------------------------------------------------------------------------------------------
AVERAGE = []
filename =[]


df_graph = pd.DataFrame(list(zip(graph_all, actual_game)))     
df_graph.columns = ['graph', 'name']

for count1, row1 in df_graph.iterrows():
    target_graph = row1['graph']
    compare_graph = df_graph[df_graph.name!=row1['name']]
    for count2, row2 in compare_graph.iterrows():
        graph_measure = target_graph + row2['graph']
        gk = WeisfeilerLehman(n_iter=4, base_graph_kernel=VertexHistogram, normalize=True)
        K_train = gk.fit_transform(graph_measure)

        #-------calculate average of 2 consecutive game--------
        df = pd.DataFrame(K_train)
        real_ave_df = df.loc[len(target_graph):,:len(target_graph)-1]
        ave=real_ave_df.mean().mean()
        ave_col = real_ave_df.mean()
        max_in_column = real_ave_df.max()
        AVERAGE.append(ave)
        df_max=pd.DataFrame(max_in_column,columns=['max'])
        df_max.to_csv(dst + row1['name'].split('_lip')[0] +'_to_'+ row2['name'].split('_lip')[0] +'_WL_kernel_maxInCol.csv')
        df.to_csv(dst+ row1['name'].split('_lip')[0] +'_to_'+ row2['name'].split('_lip')[0] +'_' +'WL_kernel_normalize.csv')
        filename.append(row1['name'].split('_lip')[0] +','+ row2['name'].split('_lip')[0])

