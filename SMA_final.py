import os
import glob
import string
import matplotlib.pyplot as plt
import networkx as nx

Temp= []#暫存list
file_novel = glob.glob(r'/Users/xiaozout/Documents/Final_SMA/TXT/*.txt')

#全人物列表
f_cha = open('charactor.txt', 'r')
A = f_cha.read()
A = A.replace("\n", " ")
A = A.split(" ")

#處理所有文章內容
for i in range(len(file_novel)):
	file_n = open(file_novel[i],'r')
	A_n = file_n.read()
	A_n = A_n.replace("全本小說網 http://big5.quanben-xiaoshuo.com", "")
	A_n = A_n.replace("。”","")
	A_n = A_n.replace("”","")
	A_n = A_n.replace("“","")
	A_n = A_n.replace("\n","")
	A_n = A_n.replace("。","\n")
	A_n = A_n.split()

#存在人物列表中的人物有出現在句子中就加入setence list
sentence = []
for i in range(len(A_n)):
	for j in range(len(A)):
		result = A[j] in A_n[i]
		if result == True:
			Temp.append(A[j])
	sentence.append(Temp)
	Temp=[]
while [] in sentence:
    sentence.remove([])

print(sentence)
print(len(sentence))
print('######################################################################################################################################')

#將句子中只有出現過一次的人名delete掉放入relation list(代表實際確實有關係)
relation = []
for i in range(len(sentence)):
	if (len(sentence[i])>1):
		relation.append(sentence[i])
for i in range(len(relation)-1):
	if(len(relation[i])>len(relation[i+1])):
		a = len(relation[i])

print(relation)
print(len(relation))
print('######################################################################################################################################')

#將relation list 整理成只有兩個人的關係，因為最多一個句子會出現6個人所以我很白癡的直接用if-else去倆倆組合
reduce_relation = []
for i in range(len(relation)):
	if len(relation[i]) == 2:
		reduce_relation.append((relation[i][0],relation[i][1]))
	elif len(relation[i]) == 3:
		reduce_relation.append((relation[i][0],relation[i][1]))
		reduce_relation.append((relation[i][0],relation[i][2]))
		reduce_relation.append((relation[i][1],relation[i][2]))
	elif len(relation[i]) == 4:
		reduce_relation.append((relation[i][0],relation[i][1]))
		reduce_relation.append((relation[i][0],relation[i][2]))
		reduce_relation.append((relation[i][0],relation[i][3]))
		reduce_relation.append((relation[i][1],relation[i][2]))
		reduce_relation.append((relation[i][1],relation[i][3]))
		reduce_relation.append((relation[i][2],relation[i][3]))
	elif len(relation[i]) == 5:
		reduce_relation.append((relation[i][0],relation[i][1]))
		reduce_relation.append((relation[i][0],relation[i][2]))
		reduce_relation.append((relation[i][0],relation[i][3]))
		reduce_relation.append((relation[i][0],relation[i][4]))
		reduce_relation.append((relation[i][1],relation[i][2]))
		reduce_relation.append((relation[i][1],relation[i][3]))
		reduce_relation.append((relation[i][1],relation[i][4]))
		reduce_relation.append((relation[i][2],relation[i][3]))
		reduce_relation.append((relation[i][2],relation[i][4]))
		reduce_relation.append((relation[i][3],relation[i][4]))
	else : 
		reduce_relation.append((relation[i][0],relation[i][1]))
		reduce_relation.append((relation[i][0],relation[i][2]))
		reduce_relation.append((relation[i][0],relation[i][3]))
		reduce_relation.append((relation[i][0],relation[i][4]))
		reduce_relation.append((relation[i][0],relation[i][5]))
		reduce_relation.append((relation[i][1],relation[i][2]))
		reduce_relation.append((relation[i][1],relation[i][3]))
		reduce_relation.append((relation[i][1],relation[i][4]))
		reduce_relation.append((relation[i][1],relation[i][5]))
		reduce_relation.append((relation[i][2],relation[i][3]))
		reduce_relation.append((relation[i][2],relation[i][4]))     
		reduce_relation.append((relation[i][2],relation[i][5]))
		reduce_relation.append((relation[i][3],relation[i][4]))
		reduce_relation.append((relation[i][3],relation[i][5]))
		reduce_relation.append((relation[i][4],relation[i][5]))

print(reduce_relation)
print(len(reduce_relation))
print(reduce_relation[0])
print(type(reduce_relation))
print('######################################################################################################################################')

#key_value是將兩人的關係整理成唯一並計算兩人之間出現關係的次數（關係權重）
key_value = []
reduce_relation_set = list(set([tuple(t) for t in reduce_relation]))
for item in reduce_relation_set:
  key_value.append((item, reduce_relation.count(item)))

#因為key_vale內容是（（人名，人名），關係權重）所以轉成turple重切再另存成一個list
key_value = tuple(key_value)
relation_key=[]
for i in range(len(key_value)):
	relation_key.append(key_value[i][0])

print(reduce_relation_set)
print(len(reduce_relation_set))
print(key_value)
print(len(key_value))
print(key_value[0])
print(key_value[0][1])
print(key_value[0][0])
print(relation_key)
print(relation_key[0][0])
print('######################################################################################################################################')

#最後畫圖
G = nx.Graph()
for i in range(len(relation_key)):
	G.add_edge(relation_key[i][0], relation_key[i][1], weight=key_value[i][1])


elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 12]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 12]

pos = nx.spring_layout(G)

# nodes
nx.draw_networkx_nodes(G, pos, node_size=350)

# edges
nx.draw_networkx_edges(G, pos, edgelist=elarge,width=6)
nx.draw_networkx_edges(G, pos, edgelist=esmall,width=3, alpha=0.5, edge_color='b')

# labels
# 結點字會出現亂碼或方塊是因為內建沒有中文字只要去網路上下載中文字體ttf檔然後將檔名存成DejaVuSans放在matplotlib中的mpl-data\fonts\ttf的資料夾下
nx.draw_networkx_labels(G, pos, font_size=5, font_family='DejaVu Sans')

plt.axis('off')
plt.show()



