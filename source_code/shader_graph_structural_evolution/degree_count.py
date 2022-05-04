"""
degree distribution for each frame for FS
"""

import os 
import csv 
import pandas as pd
import networkx as nx

path1 = './fireStrick/combine_all/'
frame_start=510
frame_end=3121
for idx in range(frame_start, frame_end, 10):
    fnum = '_f'+ str(idx)+'_'
    shadertypes = [m for m in os.listdir(path1) if m.startswith('distinct')]
    degreeDistribution_output= path1  + 'degree_distribution/' + fnum +"FS_degreeDistribution.csv"
    in_out_degree_output = path1 + 'degree_distribution/' + fnum +'FS_in_out_degree.csv'    
    
    with open(degreeDistribution_output, 'a', newline='') as file, open(in_out_degree_output, 'w', newline='') as file1:
                writer = csv.writer(file)
                writer.writerow(["fnum","shadertype","x", "node", "Digraph", "Graph"])
                writer1 = csv.writer(file1)
                writer1.writerow(["idx", "node", "digraph_in", "digraph_out"])
    
    
    for shadertype in shadertypes:
        print(shadertype)
        edgelists = [i for i in os.listdir(path1 + shadertype +'/edgelist/') if i.find(fnum)!=-1]  
        
        for edge in edgelists:
            print(edge)
            edge_list = pd.read_csv(path1  + shadertype + '/edgelist/' + edge, header = None)
            node_list = pd.read_csv(path1 + shadertype + '/hash/' + edge.split('_edgelist')[0]+'_nodelist', header = None)
            diG = nx.DiGraph()
            for i, elrow in edge_list.iterrows():
                diG.add_edge(elrow[0], elrow[1])
            for i, nodrow  in node_list.iterrows():
                diG.nodes[i]['value'] =nodrow 
                
            #print(diG.degree())
            with open(degreeDistribution_output, 'a', newline='') as file, open(in_out_degree_output, 'a', newline='') as file1:
                writer = csv.writer(file)
                writer1 = csv.writer(file1)
                for i, nodrow  in node_list.iterrows():
                    # number of degree
                    x = diG.degree(nodrow[0])
                    gindegree = diG.in_degree(nodrow[0])
                    goutdegree = diG.out_degree(nodrow[0])
                    
                    writer.writerow([fnum.split('_')[1].split('f')[1], shadertype.split('_')[1], nodrow[0],nodrow[1], x ])
                    writer1.writerow([fnum.split('_')[1].split('f')[1], shadertype.split('_')[1], nodrow[0],nodrow[1], gindegree , goutdegree])
