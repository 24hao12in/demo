"""
union all graphs within a frame into a disjoint one graph (raw shaders)
"""
import os 
import pandas as pd
import networkx as nx

#list of paths (graphs to be merged)
path1  ='./GrandAuto/edgelist_hash_cs/'
path2 = './GrandAuto/edgelist_hash_ls/'
path3 = './GrandAuto/edgelist_hash_hs/'

output = './prepare_GCN_inputdata/'

frame_start=10
frame_end = 635
if(os.listdir(output)==False):
    os.mkdir(output)


for i in range(frame_start, frame_end, 2):
    graph_pre = []
    fnum = 'f'+str(i)
    for pathname in [path1,path2,path3]:
        edgefiles =  [i for i in os.listdir(pathname+'edgelist/') if i.find('_'+fnum+'_')!=-1 and i.endswith('_edgelist')]  
        if(len(edgefiles) !=0):
            for edge in edgefiles:
                edge_list = pd.read_csv(pathname + 'edgelist/' + edge, header = None)
                node_list = pd.read_csv(pathname + 'hash/' + edge.replace('edgelist', 'nodelist'), header = None)
                diG = nx.DiGraph()
                for i, elrow in edge_list.iterrows():
                    diG.add_edge(elrow[0], elrow[1])
                for i, nodrow  in node_list.iterrows():
                    diG.nodes[i]['value'] =nodrow 
                graph_pre.append(diG)
                  
        all = nx.disjoint_union_all(graph_pre)
        nx.write_edgelist(all, output +'/'+ fnum+'_rawshader.edgelist', data = False, delimiter =',')
        
        xx = nx.get_node_attributes(all, 'value')
        xx_items = xx.items()
        xx_list = list(xx_items)
        xx_final = []
        for i in range(len(xx_list)):
            xx_final.append(xx_list[i][1][1])
            
        df=pd.DataFrame(xx_final)
        df.to_csv(output+ '/'+ fnum+'_rawshader_NodeLabel.csv', header=False)    