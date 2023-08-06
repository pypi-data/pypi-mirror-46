# coding: utf-8
# 因素空间模块

import os
import numpy as np
import itertools
import tkinter.filedialog as fd
import tkinter as tk
import tkinter.ttk as ttk

#####################################

#样例数据
data=np.array([[1,1,3,2],[2,1,1,2],[3,2,2,3],[2,1,3,2],[1,3,2,3],[1,3,2,1],[3,2,4,3],[2,2,4,3],[2,1,1,1]])
label=np.array([2,1,1,1,2,1,2,2,1])
#####################################

#按钮界面
__rules=[]
__var=0
__choice=1
def __ui_train_btn_call():
    global __rules,__choice
    path=tk.filedialog.askopenfilename()
    data=load_data(path)
    tdata=data[:,0:-1]
    tlabel=data[:,-1]
    if __choice==1:
        __rules=factor_analy(tdata,tlabel)
    else:
        __rules=sub_rotate(tdata,tlabel)
    path=tk.filedialog.asksaveasfilename()
    saved=save_data(path,__rules)
    
def __ui_load_btn_call():
    global __rules
    path=tk.filedialog.askopenfilename()
    __rules=load_data(path)
 
def __ui_test_btn_call():
    global __rules
    results=[]
    path=tk.filedialog.askopenfilename()
    data=load_data(path)
    tdata=data[:,0:-1]
    tlabel=data[:,-1]
    for i in range(len(tdata)):
        results.append(predict(__rules,tdata[i]))
    results=np.array([results])
    data=np.append(data.T,results,axis=0)
    data=data.T
    path=tk.filedialog.asksaveasfilename()
    saved=save_data(path,data)

def __ui_radio_choice():
    global __var,__choice
    __choice=int(__var.get())
    
def app():
    global __rules,__var
    root=tk.Tk()
    root.title('因素空间模块')
    root.geometry("300x450")
    title=tk.Label(root,text='选择任务',font=('Arial', 16))
    title.pack()
    __var=tk.IntVar()
    fa_radio=tk.Radiobutton(root, text="因素分析", variable=__var, value=1,command=__ui_radio_choice)
    fa_radio.pack(side=tk.TOP)
    sr_radio=tk.Radiobutton(root, text="差转计算", variable=__var, value=2,command=__ui_radio_choice)
    sr_radio.pack(side=tk.TOP)
    train_btn=tk.Button(root,text='生成规则',font=('Arial', 12),width=20,height=5,command=__ui_train_btn_call)
    train_btn.pack(side=tk.TOP)
    space=tk.Label(root,text=' ')
    space.pack()
    load_btn=tk.Button(root,text='读取规则',font=('Arial', 12),width=20,height=5,command=__ui_load_btn_call)
    load_btn.pack()
    space=tk.Label(root,text=' ')
    space.pack()
    test_btn=tk.Button(root,text='测试规则',font=('Arial', 12),width=20,height=5,command=__ui_test_btn_call)
    test_btn.pack()
    root.mainloop()
    

#####################################

#因果排序
def causal_order(rules_set,none_value=-1):

    rules_set=np.array(rules_set)
    count=len(rules_set[0])-1
    weights=[0]*count
    
    for i in range(count):
        weights[i]=np.sum(rules_set[:,i]!=none_value)    
        
    #返回概念格
    weights=np.array(weights)
    weights=np.append(weights,-1)    
    zero_index=np.where(weights==0)
    weight_index=np.argsort(weights)
    zero_mask=np.in1d(weight_index,zero_index)
    filter_mask=np.where(zero_mask==True)
    rules_set=np.array(rules_set)
    rules_set=rules_set[:,weight_index]
    rules_set=rules_set[np.lexsort(rules_set.T)]
    weight_index=np.delete(weight_index,filter_mask)
    rules_set=np.delete(rules_set,filter_mask,axis=1)
    rules_set=rules_set[:,::-1]
    weight_index=weight_index[::-1]
    weight_index=np.delete(weight_index,-1)
    causality=rules_set.tolist()
    weight_index=weight_index.tolist()
    return causality,weight_index 



#####################################

#因素排序
def factor_order(rules_set,none_value=-1,reverse=False):

    rules_set=np.array(rules_set)
    order_index=[0]*len(rules_set)
                
    #生成排序索引
    for i in range(len(order_index)):
        order_index[i]=np.sum(rules_set[i]!=none_value)
                    
    #生成排序规则库
    if reverse==False:
        rules_set=rules_set[np.argsort(order_index)].tolist()
    else:
        rules_set=rules_set[np.argsort(order_index)[::-1]].tolist()
        
    return rules_set

    
#####################################

#阶乘函数
def func(n):

    #递归计算
    if n == 0 or n == 1:
        return 1
    else:
        return (n * func(n - 1))

#####################################

#读取CSV数据集
def load_csv(filename,start_index=2,none_value='0',label=True):

    #判断文件不存在
    if not os.path.exists(filename):  
        print("ERROR: file not exit: %s" % (filename))  
        return None  

    #判断不是文件
    if not os.path.isfile(filename):  
        print("ERROR: %s not a filename." % (filename))  
        return None  

    #定义变量  
    data = []
    labels = []
    file = open(filename)
    si=start_index-1

    #生成数据集
    for line in file:
        line = line.strip('\n')
        line = line.replace(',?',','+none_value)
        split_data = line.split(',')
        data_len=len(split_data)-start_index+1

        if label==False:
            data_len+=1

        data.append(list(map(float,split_data[si:data_len])))

        if label==True:
            labels.append(float(split_data[-1]))

    #返回数据集
    file.close()  
    data = np.array(data)
    labels = np.array(labels)

    if label==False:
        return data
    return data,labels
#####################################

#读取数据集
def load_data(filename,start_index=1,label=False):

    #判断文件不存在
    if not os.path.exists(filename):  
        print("ERROR: file not exit: %s" % (filename))  
        return None  

    #判断不是文件
    if not os.path.isfile(filename):  
        print("ERROR: %s not a filename." % (filename))  
        return None  

      
    data=np.loadtxt(filename,delimiter=',')

    if label==True:
        data_no_label=data[:,start_index-1:-1]
        label=data[:,-1]
        return data_no_label,label
    
    return data
           
#####################################

#保存数据集
def save_data(filename,data):

    data=np.array(data)  
    np.savetxt(filename,data,fmt='%f',delimiter=',') 
    return True  


#####################################

#精度
def accuracy(rules_set,test_data,test_label,none_value=-1,reverse=False,number=False):

    #定义变量
    correct=0
    total=0

    #遍历测试数据
    for i in range(len(test_data)):

        #进行规则推理
        if predict(rules_set,test_data[i],none_value=none_value,reverse=reverse)==test_label[i]:
            correct+=1
        total+=1
            
    #判断返回正确数量    
    if number==True:
        return correct

    #返回精度
    if total==0:
        return 0.
    return correct/total

    
#####################################

#增强精度
def enhanced_accuracy(rules_set,rule_weights,test_data,test_label,none_value=-1,reverse=False,number=False,continuous=False):

    #定义变量
    correct=0
    total=0

    #判断不使用连续型数据规则推理
    if continuous==False:

        #遍历测试数据
        for i in range(len(test_data)):            

            #进行规则推理
            if discrete_predict(rules_set,rule_weights,test_data[i],none_value=none_value,reverse=reverse)==test_label[i]:
                correct+=1
            total+=1
            
    elif continuous==True:

        #遍历测试数据
        for i in range(len(test_data)):            

            #进行规则推理
            if continuous_predict(rules_set,rule_weights,test_data[i],none_value=none_value,reverse=reverse)==test_label[i]:
                correct+=1
            total+=1
        

    #判断返回正确数量    
    if number==True:
        return correct

    #返回精度
    if total==0:
        return 0.
    return correct/total

    

#####################################

#规则推理
def predict(rules_set,data,none_value=-1,reverse=False):

    #定义临时变量
    np_data=np.asarray(data)    
    count=len(rules_set)
    
    #判断反向规则集推理
    if reverse==False:

        #遍历规则集
        for i in range(count):
            rule=np.asarray(rules_set[i])
            rule=np.delete(rule,-1)

            #返回匹配结果
            if np.sum(np_data==rule)==np.sum(rule!=none_value):
                return rules_set[i][-1]
        return -1.
  
    else:

        reverse_count=count

        #遍历规则集
        for i in range(count):
            reverse_count-=1
            rule=np.asarray(rules_set[reverse_count])
            rule=np.delete(rule,-1)

            #返回匹配结果
            if np.sum(np_data==rule)==np.sum(rule!=none_value):
                return rules_set[reverse_count][-1]
        return -1.
    
#####################################

#离散型规则推理
def discrete_predict(rules_set,rule_weights,data,none_value=-1,reverse=False):

    #定义临时变量
    discrete_results=[0]*len(rules_set)
    rule_weights=np.array(rule_weights)
    np_data=np.asarray(data)    
    count=len(rules_set)    
    
    #判断反向规则集推理
    if reverse==False:

        #遍历规则集
        for i in range(count):
            rule=np.asarray(rules_set[i])
            rule=np.delete(rule,-1)

            #返回匹配结果
            discrete_results[i]=(np.sum(np_data==rule))*rule_weights[i]
            if np.sum(np_data==rule)==np.sum(rule!=none_value):
                return rules_set[i][-1]
        return rules_set[np.argmax(discrete_results)][-1]

    else:

        reverse_count=count

        #遍历规则集
        for i in range(count):
            reverse_count-=1
            rule=np.asarray(rules_set[reverse_count])
            rule=np.delete(rule,-1)

            #返回匹配结果
            discrete_results[reverse_count]=(np.sum(np_data==rule))*rule_weights[reverse_count]
            if np.sum(np_data==rule)==np.sum(rule!=none_value):
                return rules_set[reverse_count][-1]
        return rules_set[np.argmax(discrete_results)][-1]

    
#####################################

#连续型数据规则推理
def continuous_predict(rules_set,rule_weights,data,none_value=-1,reverse=False):

    #定义临时变量
    continuous_results=[0]*len(rules_set)
    rule_weights=np.array(rule_weights)
    np_data=np.asarray(data)    
    count=len(rules_set)    
    
    #判断反向规则集推理
    if reverse==False:

        #遍历规则集
        for i in range(count):
            rule=np.asarray(rules_set[i])
            rule=np.delete(rule,-1)

            #返回匹配结果            
            continuous_results[i]=(np.sqrt(np.sum((np_data[rule!=none_value]-rule[rule!=none_value])**2)))*(1/rule_weights[i])
            if np.sum(np_data==rule)==np.sum(rule!=none_value):
                return rules_set[i][-1]
        return rules_set[np.argmin(continuous_results)][-1]
        
    else:

        reverse_count=count

        #遍历规则集
        for i in range(count):
            reverse_count-=1
            rule=np.asarray(rules_set[reverse_count])
            rule=np.delete(rule,-1)

            #返回匹配结果
            continuous_results[reverse_count]=(np.sqrt(np.sum((np_data[rule!=none_value]-rule[rule!=none_value])**2)))*(1/rule_weights[reverse_count])
            if np.sum(np_data==rule)==np.sum(rule!=none_value):
                return rules_set[reverse_count][-1]
        return rules_set[np.argmin(continuous_results)][-1]
            

    
#####################################

#删除缺失值数集
def delete_none_value(train_data,train_label,none_value):

    train_data=np.array(train_data)
    train_label=np.array(train_label)
    delete_index=[]
    
    for i in range(len(train_data)):
        if np.sum(train_data[i]==none_value)>0:
            delete_index.append(i)

    train_data=np.delete(train_data,delete_index,axis=0)
    train_label=np.delete(train_label,delete_index,axis=0)

    return train_data,train_label
    
    
        
        
#####################################

#数据去重
def unique_data(train_data,train_label):

    #数据集去重
    train_data=np.array(train_data)
    train_label=np.array(train_label)
    train_data,indexes=np.unique(train_data,axis=0,return_index=True)
    train_label=train_label[indexes]

    return train_data,train_label
        
        

#####################################

#获取数据集
def get_data(train_data,train_label,data_num=-1):

    #返回数据集
    if data_num<=0:
        return train_data,train_label

    #随机返回部分数据集
    if data_num<=len(train_data):
        batch_mask = np.random.choice(len(train_data), data_num, replace=False)
        train_data = train_data[batch_mask]
        train_label = train_label[batch_mask]
        return train_data,train_label

    #随机返回重复数据集
    if data_num>len(train_data):
        batch_mask = np.random.choice(len(train_data), data_num, replace=True)
        train_data = train_data[batch_mask]
        train_label = train_label[batch_mask]
        return train_data,train_label
        
        
#####################################

#裁剪规则集
def slim_rules(rules_set,rule_weights,rule_time=[],slim=0.):
    
    if np.max(rule_weights)>1:
        weights=(np.array(rule_weights)/np.sum(rule_weights)).tolist()
        delete_index=np.where(np.array(weights)<=slim)

    else:
        #削减规则
        delete_index=np.where(np.array(rule_weights)<=slim)

    delete_rules_set=np.array(rules_set)[delete_index].tolist()
    rules_set=np.delete(rules_set,delete_index,axis=0).tolist()
    rule_weights=np.delete(rule_weights,delete_index).tolist()

    if len(rule_time)>0:
        rule_time=np.delete(rule_time,delete_index).tolist() 
        return rules_set,rule_weights,rule_time

    return rules_set,rule_weights
        
        
#####################################

#计算规则权重
def get_rule_weights(rules_set,data,label,number=False,none_value=-1):

    data_num=len(data)
    count=len(rules_set)
    rules_acc_number=[0]*count
    
    #构建权重集
    for i in range(len(data)):

        #定义临时变量
        np_data=np.asarray(data[i])    

        #遍历规则集
        for j in range(count):
            rule=np.asarray(rules_set[j])
            rule=np.delete(rule,-1)

            #返回匹配结果
            if np.sum(np_data==rule)==np.sum(rule!=none_value):
                if rules_set[j][-1]==label[i]:
                    rules_acc_number[j]+=1
                    break
    
    rule_weights=(np.array(rules_acc_number)/data_num).tolist()
    
    #返回规则权重集
    if number==False:
        return rule_weights
    
    return rules_acc_number
        
#####################################

#计算因素影响力
def factor_influence(rules_set,rule_weights,result_class=False,none_value=-1):

    #定义变量
    rules_set=np.array(rules_set)
    rule_weights=np.array(rule_weights)
    factor_num=rules_set.shape[1]-1
    result_values=np.unique(rules_set[:,-1])
    rules_set_part=[0]*len(result_values)
    rule_weights_part=[0]*len(result_values)
    factor_influences=[0]*len(result_values)

    #定义分结果空集
    for i in range(len(result_values)):
        rules_set_part[i]=[]
        rule_weights_part[i]=[]
        factor_influences[i]=[0.]*rules_set.shape[1]
        factor_influences[i][0]=result_values[i]

    #按结果拆分规则集
    for i in range(len(result_values)):
        index_part=np.where(rules_set[:,-1]==result_values[i])
        rules_set_part[i]=rules_set[index_part]
        rules_set_part[i]=rules_set_part[i][:,0:-1]
        rule_weights_part[i]=rule_weights[index_part]

    #numpy化数据集
    rules_set_part=np.array(rules_set_part)
    rule_weights_part=np.array(rule_weights_part)

    #遍历每种结果
    for i in range(len(result_values)):

        #遍历每个规则集
        for j in range(len(rules_set_part[i])):
            factor_weight=rule_weights_part[i][j]/np.sum(rules_set_part[i][j]!=none_value)

            #遍历每个因素
            for k in range(factor_num):

                #判断给出单规则影响值
                if rules_set_part[i][j][k]!=none_value:
                    factor_influences[i][k+1]+=factor_weight

    #返回影响集        
    if result_class==False:
        factor_influences=np.array(factor_influences)
        temp_values=[0.]*factor_num

        for i in range(factor_num):
            temp_values[i]=np.sum(factor_influences[:,i+1])

        factor_influences=temp_values
        
    return factor_influences       
#####################################

#构建因素边列表
def build_edge_list(rules_set,rule_weights,factor_index,none_value=-1):

    edge_list=[]
    factor_influences=factor_influence(rules_set,rule_weights,none_value=none_value)
    
    #转换边列表
    for i in range(len(factor_index)-1):
        edge=[]
        edge.append(factor_index[i])
        edge.append(factor_index[-1])
        edge.append(factor_influences[i])
        edge_list.append(edge)

    #返回边列表
    return edge_list

#####################################

#构建因素网络
def build_network(data,order=True,normalize=True,cut_zero_edge=True,none_value=-1):

    data=np.array(data)
    network=[]
    factor_index=list(range(data.shape[1]))

    #构建网路
    for i in range(data.shape[1]):
        factor_index_part=factor_index[:i]+factor_index[(i+1):]
        factor_index_part.append(i)
        data_part=np.c_[data[:,0:i],data[:,(i+1):]]
        label_part=data[:,i]
        rules_set=factor_analy(data_part,label_part,none_value=none_value)
        if len(rules_set)!=0:
            rule_weights=get_rule_weights(rules_set,data_part,label_part,number=True,none_value=none_value)
            network+=build_edge_list(rules_set,rule_weights,factor_index_part,none_value=none_value)

    #判断特殊处理
    if order or cut_zero_edge or normalize ==True:
        network=np.array(network)

        if order==True:
            network=network[:,::-1]
            network=network[np.lexsort(network.T)]
            network=network[:,::-1]
            
        if cut_zero_edge==True:
            network=network[np.where(network[:,-1]!=0)]
            
        if normalize==True:    
            total_value=np.sum(network[:,-1])
            network[:,-1]=network[:,-1]/total_value

        network=network.tolist()

    #返回因素网络    
    return network

#####################################

#获得网络输出
def get_network_out(network,order=True):

    network=np.array(network)
    factor_index=np.sort(np.unique(network[:,0]))
    network_out=[0]*len(factor_index)

    #构建输出集
    for i in range(len(factor_index)):
        network_out[i]=[]
        network_out[i].append(factor_index[i])
        network_out[i].append(np.sum(network[np.where(network[:,0]==factor_index[i])][:,2]))

    #判断排序
    if order==True:
        network_out=np.array(network_out)
        network_out=network_out[np.argsort(network_out[:,1])]
        network_out=network_out[::-1]
        network_out=network_out.tolist()

    #返回网络输出集
    return network_out
    
#####################################

#获得网络输入
def get_network_in(network,order=True):

    network=np.array(network)
    factor_index=np.sort(np.unique(network[:,1]))
    network_in=[0]*len(factor_index)

    #构建输入集
    for i in range(len(factor_index)):
        network_in[i]=[]
        network_in[i].append(factor_index[i])
        network_in[i].append(np.sum(network[np.where(network[:,1]==factor_index[i])][:,2]))

    #判断排序
    if order==True:
        network_in=np.array(network_in)

        network_in=network_in[np.argsort(network_in[:,1])]
        network_in=network_in[::-1]
        network_in=network_in.tolist()

    #返回网络输入集    
    return network_in

#####################################

#获得网络净输出集
def get_network_netout(network,order=True):

    outflows=get_network_out(network,order=False)
    inflows=get_network_in(network,order=False)
    outflows=np.array(outflows)
    inflows=np.array(inflows)
    factors=np.append(outflows[:,0],inflows[:,0])
    factors=np.sort(np.unique(factors))
    netout=[0]*len(factors)

    #构建净输出集
    for i in range(len(factors)):
        netout[i]=[]
        netout[i].append(factors[i])
        value=0.
        if factors[i] in outflows[:,0] and factors[i] in inflows[:,0]:
            value=outflows[np.where(outflows[:,0]==factors[i])][0][1]-inflows[np.where(inflows[:,0]==factors[i])][0][1]
        
        elif factors[i] in outflows[:,0]:
            value=outflows[np.where(outflows[:,0]==factors[i])][0][1]

        elif factors[i] in inflows[:,0]:
            value=-infows[np.where(inflows[:,0]==factors[i])][0][1]

        netout[i].append(value)

    #判断排序
    if order==True:
        netout=np.array(netout)
        netout=netout[np.argsort(netout[:,1])]
        netout=netout[::-1]
        netout=netout.tolist()

    #返回网络净输出集    
    return netout

#####################################

#最大规则算法
def max_rules(train_data,train_label,none_value=-1,train_times=10000,used_factors=False,full_rules=False,simple=False,strict=False,expand=False,similar_first=False):

    #初始化变量
    data=np.array(train_data)
    label=np.array(train_label)
    factor_num=data.shape[1]
    factor_classes=[]
    trained_factors=np.array([])
    used_factor_set=np.array([])
    delete_list=[]
    rule=[none_value]*(factor_num+1)
    rules_set=[]
    rules_set_part=[]
    decide_data=np.full(data.shape,none_value)
    decide_label=np.full(label.shape,none_value)

    #判断不启用全规则算法
    if full_rules==False:
        comb_num=1
        
        #一次数据收敛
        for i in range(train_times):
            delete_list=[]
            rules_set_part=[]
            trained_factors=np.array([])
            last_data_num=len(data)
            decide_data=np.full(data.shape,none_value)
            decide_label=np.full(label.shape,none_value)
            final_count=len(used_factor_set)
            rules=[]

            ###
            factor_index=list(range(factor_num))
            combinations=list(itertools.combinations(factor_index,comb_num))
                        
            #生成因素分类构建决定表    
            for j in range(len(combinations)):
                factor_classes=[]

                ###
                factor_count=len(combinations[j])
                factor_value=[0.]*len(data)
                factor_value=np.array(factor_value)
                rule=[none_value]*(factor_num+1)

                #确定分类值
                for k in range(factor_count):
                    factor_value+=data[:,combinations[j][k]]**(1/(k+1))
                    
                #按照一个因素分类
                for k in np.unique(factor_value):
                    factor_classes.append(np.where(factor_value==k))

                #遍历一个因素的每个类
                for k in range(len(factor_classes)):

                    #判断一个类是决定类
                    if len(np.unique(label[factor_classes[k]]))==1:

                        #生成推理规则
                        for l in range(factor_count):
                            rule[combinations[j][l]]=data[factor_classes[k][0][0]][combinations[j][l]]
                            rule[-1]=label[factor_classes[k][0][0]]
                            trained_factors=np.append(trained_factors,combinations[j][l])
                            trained_factors=np.unique(trained_factors)

                        #构建推理规则集
                        rules.append(rule.copy())
                
                        #构建收敛表和决定表
                        for l in range(factor_count): 

                            for m in range(len(factor_classes[k][0])):
                                delete_list.append(factor_classes[k][0][m])
                                decide_data[factor_classes[k][0][m]][combinations[j][l]]=data[factor_classes[k][0][m]][combinations[j][l]]
                                decide_label[factor_classes[k][0][m]]=label[factor_classes[k][0][m]]

            
            #遍历全部因素组合数量
            if comb_num==1 and simple==False:
                for j in range(2,factor_num+1):
                
                    #遍历决定表
                    for k in range(len(decide_data)):
                        data_factor_use=np.where(decide_data[k]!=none_value)[0]
                        decide_num=len(data_factor_use)

                        #判断无生成规则
                        if decide_num==0:
                            continue

                        #构建当前数据所有组合                    
                        combinations=list(itertools.combinations(data_factor_use,j))
                    
                        #遍历所有组合
                        for l in combinations:
                            factor_count=len(l)
                            rule=[none_value]*(factor_num+1)

                            #判断严格规则集
                            if strict==False:
                        
                                #生成当前因素规则
                                for m in range(factor_count):
                                    rule[l[m]]=decide_data[k][l[m]]
                                    rule[-1]=decide_label[k]
                                    trained_factors=np.append(trained_factors,l[m])
                                    trained_factors=np.unique(trained_factors)

                                #加入生成规则
                                rules.append(rule.copy())

                            else:

                                #停止扩大规则集
                                expand=False
                            
                                #生成之前因素规则
                                for m in range(final_count):
                                    rule[int(used_factor_set[m])] = data[k][int(used_factor_set[m])]

                                #生成当前因素规则
                                for m in range(factor_count):
                                    rule[l[m]]=decide_data[k][l[m]]
                                    rule[-1]=decide_label[k]
                                    trained_factors=np.append(trained_factors,l[m])
                                    trained_factors=np.unique(trained_factors)

                                #加入生成规则    
                                rules.append(rule.copy())
                            

                            #判断扩大规则集
                            if expand==True:

                                #生成之前因素规则
                                for m in range(final_count):
                                    rule[int(used_factor_set[m])] = data[k][int(used_factor_set[m])]

                                #生成当前因素规则
                                for m in range(factor_count):
                                    rule[l[m]]=decide_data[k][l[m]]
                                    rule[-1]=decide_label[k]

                                #加入生成规则    
                                rules.append(rule.copy())

            if comb_num>1 and simple==False:

                #遍历决定表
                for k in range(len(decide_data)):
                    data_factor_use=np.where(decide_data[k]!=none_value)[0]
                    decide_num=len(data_factor_use)

                    #判断无生成规则
                    if decide_num==0:
                        continue

                    #构建当前数据所有组合                    
                    combinations=list(itertools.combinations(data_factor_use,decide_num))

                    #遍历所有组合
                    for l in combinations:
                        factor_count=len(l)
                        rule=[none_value]*(factor_num+1)

                        #判断严格规则集
                        if strict==False:
                        
                            #生成当前因素规则
                            for m in range(factor_count):
                                rule[l[m]]=decide_data[k][l[m]]
                                rule[-1]=decide_label[k]
                                trained_factors=np.append(trained_factors,l[m])
                                trained_factors=np.unique(trained_factors)

                            #加入生成规则
                            rules.append(rule.copy())

                        else:

                            #停止扩大规则集
                            expand=False
                            
                            #生成之前因素规则
                            for m in range(final_count):
                                rule[int(used_factor_set[m])] = data[k][int(used_factor_set[m])]

                            #生成当前因素规则
                            for m in range(factor_count):
                                rule[l[m]]=decide_data[k][l[m]]
                                rule[-1]=decide_label[k]
                                trained_factors=np.append(trained_factors,l[m])
                                trained_factors=np.unique(trained_factors)

                            #加入生成规则    
                            rules.append(rule.copy())

                        #判断扩大规则集
                        if expand==True:

                            #生成之前因素规则
                            for m in range(final_count):
                                rule[int(used_factor_set[m])] = data[k][int(used_factor_set[m])]

                            #生成当前因素规则
                            for m in range(factor_count):
                                rule[l[m]]=decide_data[k][l[m]]
                                rule[-1]=decide_label[k]

                            #加入生成规则    
                            rules.append(rule.copy())

            #构建规则集
            rules_set_part+=rules
                
            #构建约简因素集和收敛数据    
            used_factor_set=np.append(used_factor_set,trained_factors)
            used_factor_set=np.unique(used_factor_set)
            data=np.delete(data,delete_list,axis=0)
            label=np.delete(label,delete_list,axis=0)
            #print('remain data:',len(data))

            if comb_num>1:
                comb_num=1

            #判断规则库排序
            if similar_first==True and len(rules_set_part)!=0:
                rules_set_part=np.array(rules_set_part)
                order_index=[0]*len(rules_set_part)
                
                #生成排序索引
                for i in range(len(order_index)):
                    order_index[i]=np.sum(rules_set_part[i]!=none_value)
                    
                #生成排序规则库
                rules_set_part=rules_set_part[np.argsort(order_index)[::-1]].tolist()

            #合并规则集
            rules_set+=rules_set_part

            #判断收敛完成
            if len(data)==0:
                break

            #判断无法收敛改用多因素组合
            if len(data)==last_data_num:
                #print('use more f')
                comb_num+=1

                   

        

    #判断使用全规则算法
    if full_rules==True:
        
        #遍历每一个因素
        for i in range(factor_num):
            factor_index=list(range(factor_num))
            combinations=list(itertools.combinations(factor_index,i+1))

            #构建每一种因素组合
            for j in combinations:
                factor_classes=[]
                factor_count=len(j)
                factor_value=[0.]*len(data)
                factor_value=np.array(factor_value)
                rule=[none_value]*(factor_num+1)

                #确定分类值
                for k in range(factor_count):
                    factor_value+=data[:,j[k]]**(1/(k+1))

                #构建分类表
                for k in np.unique(factor_value):
                    factor_classes.append(np.where(factor_value==k))

                #遍历分类表
                for k in range(len(factor_classes)):

                    #判断决定类
                    if len(np.unique(label[factor_classes[k]]))==1:

                        #生成推理规则
                        for l in range(factor_count):
                            rule[j[l]]=data[factor_classes[k][0][0]][j[l]]
                            rule[-1]=label[factor_classes[k][0][0]]

                        #构建推理规则集    
                        rules_set.append(rule.copy())

                        #构建收敛表
                        for l in range(len(factor_classes[k][0])):
                            delete_list.append(factor_classes[k][0][l])

        #生成约简因素集
        used_factor_set=factor_index

    #转换成整数因素集
    used_factor_set=list(map(int,used_factor_set))

    #判断返回约简因素集
    if used_factors==True:
        return rules_set,used_factor_set
   
    #返回规则集
    return rules_set

#####################################

#差转算法
def sub_rotate(train_data,train_label,none_value=-1,train_times=10000,used_factors=False,fast=False,rule_weight=False):

    #初始化变量
    data_num=len(train_data)
    data=np.array(train_data)
    label=np.array(train_label)
    factor_num=data.shape[1]    
    rule_delete=[]
    rule_weights=[]
    factor_classes=[]
    trained_factors=np.array([])
    used_factor_set=np.array([])
    delete_list=[]
    rule=[none_value]*(factor_num+1)
    rules_set=[]

    #判断不使用快速收敛
    if fast==False:
        comb_num=1
        #comb_total=func(factor_num)/(func(factor_num-comb_num)*func(comb_num))
        #decide_num=[0]*com_total

        #一次数据收敛
        for i in range(train_times):
            delete_list=[]
            trained_factors=np.array([])
            last_data_num=len(data)
            final_count=len(used_factor_set)            
            factor_index=list(range(factor_num))
            combinations=list(itertools.combinations(factor_index,comb_num))
            decide_num=[0]*len(combinations)

            #构建因素组合
            for j in range(len(combinations)):
                delete_list=[]
                factor_classes=[]
                factor_count=len(combinations[j])
                factor_value=[0.]*len(data)
                factor_value=np.array(factor_value)
                rule=[none_value]*(factor_num+1)

                #确定分类值
                for k in range(factor_count):
                    factor_value+=data[:,combinations[j][k]]**(1/(k+1))

                #构建分类表
                for k in np.unique(factor_value):
                    factor_classes.append(np.where(factor_value==k))

                #遍历分类表
                for k in range(len(factor_classes)):

                    #判断决定类
                    if len(np.unique(label[factor_classes[k]]))==1:
                        decide_num[j]+=len(label[factor_classes[k]])

            #定位核因素
            argmax=np.argmax(decide_num)

            #启动多因素组合分类
            if decide_num[argmax]==0:
                comb_num+=1
                #print('use more factors')
                continue

            #生成一条规则    
            delete_list=[]
            factor_classes=[]
            factor_count=len(combinations[argmax])
            factor_value=[0.]*len(data)
            factor_value=np.array(factor_value)
            rule=[none_value]*(factor_num+1)
            
            #确定分类值
            for k in range(factor_count):
                factor_value+=data[:,combinations[argmax][k]]**(1/(k+1))

            #构建分类表
            for k in np.unique(factor_value):
                factor_classes.append(np.where(factor_value==k))

            #遍历分类表
            for k in range(len(factor_classes)):

                #判断决定类
                if len(np.unique(label[factor_classes[k]]))==1:

                    #生成推理规则
                    for l in range(factor_count):
                        rule[combinations[argmax][l]]=data[factor_classes[k][0][0]][combinations[argmax][l]]
                        rule[-1]=label[factor_classes[k][0][0]]
                        trained_factors=np.append(trained_factors,combinations[argmax][l])
                        trained_factors=np.unique(trained_factors)

                    #构建推理规则集    
                    rules_set.append(rule.copy())

                    #构建收敛集
                    for l in range(len(factor_classes[k][0])):
                        delete_list.append(factor_classes[k][0][l])
                        rule_delete.append(factor_classes[k][0][l])

                    rule_delete=np.unique(rule_delete).tolist()
                    rule_weights.append((len(rule_delete)/data_num))
                    rule_delete=[]

            #收敛数据
            if len(delete_list)!=0:
                used_factor_set=np.append(used_factor_set,trained_factors)
                used_factor_set=np.unique(used_factor_set)
                data=np.delete(data,delete_list,axis=0)
                label=np.delete(label,delete_list,axis=0)
                #print('remain data:',len(data))

                if comb_num>1:
                    comb_num=1

            #判断收敛完成        
            if len(data)==0:
                break

    #判断使用快速收敛
    if fast==True:
        comb_num=1
        
        #一次数据收敛
        for i in range(train_times):
            delete_list=[]
            trained_factors=np.array([])
            last_data_num=len(data)
            final_count=len(used_factor_set)            
            factor_index=list(range(factor_num))
            combinations=list(itertools.combinations(factor_index,comb_num))

            #构建因素组合
            for j in combinations:
                delete_list=[]
                factor_classes=[]
                factor_count=len(j)
                factor_value=[0.]*len(data)
                factor_value=np.array(factor_value)
                rule=[none_value]*(factor_num+1)

                #确定分类值
                for k in range(factor_count):
                    factor_value+=data[:,j[k]]**(1/(k+1))

                #构建分类表
                for k in np.unique(factor_value):
                    factor_classes.append(np.where(factor_value==k))

                #遍历分类表
                for k in range(len(factor_classes)):

                    #判断决定类
                    if len(np.unique(label[factor_classes[k]]))==1:

                        #生成推理规则
                        for l in range(factor_count):
                            rule[j[l]]=data[factor_classes[k][0][0]][j[l]]
                            rule[-1]=label[factor_classes[k][0][0]]
                            trained_factors=np.append(trained_factors,j[l])
                            trained_factors=np.unique(trained_factors)

                        #构建推理规则集    
                        rules_set.append(rule.copy())

                        #构建收敛表
                        for l in range(len(factor_classes[k][0])):
                            delete_list.append(factor_classes[k][0][l])
                            rule_delete.append(factor_classes[k][0][l])

                        rule_delete=np.unique(rule_delete).tolist()
                        rule_weights.append((len(rule_delete)/data_num))
                        rule_delete=[]

                #收敛数据
                if len(delete_list)!=0:
                    used_factor_set=np.append(used_factor_set,trained_factors)
                    used_factor_set=np.unique(used_factor_set)
                    data=np.delete(data,delete_list,axis=0)
                    label=np.delete(label,delete_list,axis=0)
                    #print('remain data:',len(data))

                    if comb_num>1:
                        comb_num=1
                        break

            #启动多因素组合分类
            if last_data_num==len(data):
                comb_num+=1
                #print('use more factors')

            #判断收敛完成   
            if len(data)==0:
                break

    #转换成整数因素集
    used_factor_set=list(map(int,used_factor_set))
    
    #判断同时返回约简因素集和因素权重
    if used_factors==True and rule_weight==True:
        return rules_set,used_factor_set,rule_weights
   
    #判断返回约简因素集
    if used_factors==True:
        return rules_set,used_factor_set

    #判断返回规则权重
    if rule_weight==True:
        return rules_set,rule_weights

    #返回规则集
    return rules_set
                


#####################################

#因素分析法
def factor_analy(train_data,train_label,last_rules_set=[],none_value=-1,train_times=10000,used_factors=False,zero_decide_random=False,rule_weight=False,strict=False):

    #初始化变量
    data_num=len(train_data)
    data=np.array(train_data)
    label=np.array(train_label)
    factor_num=data.shape[1]
    factor_classes=[]
    used_factor_set=np.array([])
    delete_list=[]
    rule_delete=[]
    rule_weights=[]
    #factor_weights=[0]*factor_num
    last_factor=-1
    rule=[none_value]*(factor_num+1)
    rules_set=[]
    class_num=1

    #一次数据收敛
    for i in range(train_times):
        delete_list=[]
        final_count=len(used_factor_set)            
        decide_num=[0]*factor_num

        #判断第一次收敛
        if last_factor==-1:

            #构建因素组合
            for j in range(factor_num):
                delete_list=[]
                factor_classes=[]
                rule=[none_value]*(factor_num+1)

                #构建分类表
                for k in np.unique(data[:,j]):
                    factor_classes.append(np.where(data[:,j]==k))

                #遍历分类表
                for k in range(len(factor_classes)):

                    #判断决定类
                    if len(np.unique(label[factor_classes[k]]))==1:
                        decide_num[j]+=len(label[factor_classes[k]])

            #定位核因素
            argmax=np.argmax(decide_num)

            #判断零决定度开启随机索引
            if zero_decide_random==True and decide_num[argmax]==0:
                argmax=np.random.randint(factor_num)

            #生成规则        
            delete_list=[]
            factor_classes=[]
            rule=[none_value]*(factor_num+1)

            #构建分类表
            for k in np.unique(data[:,argmax]):
                factor_classes.append(np.where(data[:,argmax]==k))

            #遍历分类表
            for k in range(len(factor_classes)):

                #判断决定类
                if len(np.unique(label[factor_classes[k]]))==1:
                    rule[argmax]=data[factor_classes[k][0][0]][argmax]
                    rule[-1]=label[factor_classes[k][0][0]]
                    
                    #构建推理规则集
                    rules_set.append(rule.copy())

                    #构建收敛表
                    for l in range(len(factor_classes[k][0])):
                        delete_list.append(factor_classes[k][0][l])
                        rule_delete.append(factor_classes[k][0][l])

                    rule_delete=np.unique(rule_delete).tolist()
                    rule_weights.append((len(rule_delete)/data_num))
                    rule_delete=[]

            #收敛数据
            if len(delete_list)!=0:                
                data=np.delete(data,delete_list,axis=0)
                label=np.delete(label,delete_list,axis=0)
                delete_list=np.unique(delete_list).tolist()
                #factor_weights[argmax]+=len(delete_list)/data_num
                #print('remain data:',len(data))

            #生成约简因素集
            last_factor=argmax
            used_factor_set=np.append(used_factor_set,last_factor)
            used_factor_set=np.unique(used_factor_set)
                              
            #判断收敛完成
            if len(data)==0:
                break

        else:

            #定义上一次核因素分类变量
            last_classes=[]
            
            #构建上一次核因素分类
            for j in np.unique(data[:, last_factor]):
                last_classes.append(np.where(data[:,int(last_factor)]==j))

            #定义部分数据集
            class_num=len(last_classes)
            data_part=[0]*class_num
            label_part=[0]*class_num
            
            #创建部分数据集
            for j in range(class_num):
                data_part[j]=data[last_classes[j]]
                label_part[j]=label[last_classes[j]]

            #遍历每一部分数据集
            for j in range(class_num):

                #构建因素组合
                for k in range(factor_num):
                    delete_list=[]
                    factor_classes=[]
                    rule=[none_value]*(factor_num+1)
                    
                    #构建分类表
                    for l in np.unique(data_part[j][:,k]):
                        factor_classes.append(np.where(data_part[j][:,k]==l))
                        
                    #遍历分类表
                    for l in range(len(factor_classes)):

                        #判断决定类
                        if len(np.unique(label_part[j][factor_classes[l]]))==1:
                            decide_num[k]+=len(label_part[j][factor_classes[l]])

            #定位核因素
            argmax=np.argmax(decide_num)

            #判断零决定度顺延索引
            if decide_num[argmax]==0:
                if strict==False:
                    argmax=last_factor+1

                    #索引到结尾重置
                    if argmax>=factor_num:
                        argmax=0
                else:
                    for i in range(factor_num):
                        argmax=last_factor+1
                        if np.sum(np.in1d(argmax,used_factor_set))>0:
                            argmax+=1

                        #索引到结尾重置
                        if argmax==factor_num:
                            argmax=0
                    

            #判断开启随机索引
            if zero_decide_random==True and decide_num[argmax]==0:
                
                #选择与上一因素不重复索引
                for i in range(factor_num):
                    argmax=np.random.randint(factor_num)
                    if strict==False:
                        #不重复退出选择
                        if argmax!=last_factor:
                            break
                    else:
                        #不重复退出选择
                        if np.sum(np.in1d(argmax,used_factor_set))==0:
                            break

            #遍历每一部分数据集
            for j in range(class_num):
                delete_list=[]
                factor_classes=[]
                rule=[none_value]*(factor_num+1)

                #构建分类表
                for k in np.unique(data_part[j][:,argmax]):
                    factor_classes.append(np.where(data_part[j][:,argmax]==k))
                    
                #遍历分类表
                for k in range(len(factor_classes)):

                    #判断决定类
                    if len(np.unique(label_part[j][factor_classes[k]]))==1:
                        
                        #生成之前因素规则
                        for l in range(final_count):
                            rule[int(used_factor_set[l])] = data_part[j][factor_classes[k][0][0]][int(used_factor_set[l])]

                        #生成当前因素规则
                        rule[argmax]=data_part[j][factor_classes[k][0][0]][argmax]
                        rule[-1]=label_part[j][factor_classes[k][0][0]]
                        
                        #构建推理规则集
                        rules_set.append(rule.copy())

                        #构建收敛表
                        for l in range(len(factor_classes[k][0])):
                            delete_list.append(factor_classes[k][0][l])
                            rule_delete.append(factor_classes[k][0][l])

                        rule_delete=np.unique(rule_delete).tolist()
                        rule_weights.append((len(rule_delete)/data_num))
                        rule_delete=[]
                        
                #收敛数据
                if len(delete_list)!=0:                    
                    data_part[j]=np.delete(data_part[j],delete_list,axis=0)
                    label_part[j]=np.delete(label_part[j],delete_list,axis=0)
                    delete_list=np.unique(delete_list).tolist()
                    #factor_weights[argmax]+=len(delete_list)/data_num
                
            #定义初始完整数据
            data=data_part[0]
            label=label_part[0]

            #组合完整数据
            for j in range(1,class_num):
                data=np.append(data,data_part[j],axis=0)
                label=np.append(label,label_part[j],axis=0)

            #print('remain data:',len(data))
            
            #生成约简因素集
            last_factor=argmax
            used_factor_set=np.append(used_factor_set,last_factor)
            used_factor_set=np.unique(used_factor_set)            
                    
            #判断收敛完成
            if len(data)==0:
                break       

    #转换成整数因素集
    used_factor_set=list(map(int,used_factor_set))
    result_set=last_rules_set+rules_set

    #判断同时返回约简因素集和规则权重
    if used_factors==True and rule_weight==True:
        return rules_set,used_factor_set,rule_weights

    #判断返回约简因素集
    if used_factors==True:
        return rules_set,used_factor_set

    #判断返回规则权重
    if rule_weight==True:
        return rules_set,rule_weights

    #返回规则集
    return rules_set
#####################################

#随机因素分析法
def factor_analy_random(train_data,train_label,last_rules_set=[],none_value=-1,train_times=10000,used_factors=False,rule_weight=False):

    #初始化变量
    data_num=len(train_data)
    data=np.array(train_data)
    label=np.array(train_label)
    factor_num=data.shape[1]
    factor_classes=[]
    used_factor_set=np.array([])
    delete_list=[]
    rule_delete=[]
    rule_weights=[]
    #factor_weights=[0]*factor_num
    last_factor=-1
    rule=[none_value]*(factor_num+1)
    rules_set=[]
    class_num=1

    #一次数据收敛
    for i in range(train_times):
        delete_list=[]
        final_count=len(used_factor_set)

        #判断第一次收敛
        if last_factor==-1:

            
            #定位核因素
            argmax=np.random.randint(factor_num)

            #生成规则        
            delete_list=[]
            factor_classes=[]
            rule=[none_value]*(factor_num+1)

            #构建分类表
            for k in np.unique(data[:,argmax]):
                factor_classes.append(np.where(data[:,argmax]==k))

            #遍历分类表
            for k in range(len(factor_classes)):

                #判断决定类
                if len(np.unique(label[factor_classes[k]]))==1:
                    rule[argmax]=data[factor_classes[k][0][0]][argmax]
                    rule[-1]=label[factor_classes[k][0][0]]
                    
                    #构建推理规则集
                    rules_set.append(rule.copy())

                    #构建收敛表
                    for l in range(len(factor_classes[k][0])):
                        delete_list.append(factor_classes[k][0][l])
                        rule_delete.append(factor_classes[k][0][l])

                    rule_delete=np.unique(rule_delete).tolist()
                    rule_weights.append((len(rule_delete)/data_num))
                    rule_delete=[]

            #收敛数据
            if len(delete_list)!=0:                
                data=np.delete(data,delete_list,axis=0)
                label=np.delete(label,delete_list,axis=0)
                delete_list=np.unique(delete_list).tolist()
                #factor_weights[argmax]+=len(delete_list)/data_num
                #print('remain data:',len(data))

            #生成约简因素集
            last_factor=argmax
            used_factor_set=np.append(used_factor_set,last_factor)
            used_factor_set=np.unique(used_factor_set)
                              
            #判断收敛完成
            if len(data)==0:
                break

        else:

            #定义上一次核因素分类变量
            last_classes=[]
            
            #构建上一次核因素分类
            for j in np.unique(data[:, last_factor]):
                last_classes.append(np.where(data[:,int(last_factor)]==j))

            #定义部分数据集
            class_num=len(last_classes)
            data_part=[0]*class_num
            label_part=[0]*class_num
            
            #创建部分数据集
            for j in range(class_num):
                data_part[j]=data[last_classes[j]]
                label_part[j]=label[last_classes[j]]

            
            #选择与上一因素不重复索引
            for i in range(factor_num):
                argmax=np.random.randint(factor_num)
                #if np.sum(np.in1d(argmax,used_factor_set))==0:
                if argmax!=last_factor:
                    break
                

            #遍历每一部分数据集
            for j in range(class_num):
                delete_list=[]
                factor_classes=[]
                rule=[none_value]*(factor_num+1)

                #构建分类表
                for k in np.unique(data_part[j][:,argmax]):
                    factor_classes.append(np.where(data_part[j][:,argmax]==k))
                    
                #遍历分类表
                for k in range(len(factor_classes)):

                    #判断决定类
                    if len(np.unique(label_part[j][factor_classes[k]]))==1:
                        
                        #生成之前因素规则
                        for l in range(final_count):
                            rule[int(used_factor_set[l])] = data_part[j][factor_classes[k][0][0]][int(used_factor_set[l])]

                        #生成当前因素规则
                        rule[argmax]=data_part[j][factor_classes[k][0][0]][argmax]
                        rule[-1]=label_part[j][factor_classes[k][0][0]]
                        
                        #构建推理规则集
                        rules_set.append(rule.copy())

                        #构建收敛表
                        for l in range(len(factor_classes[k][0])):
                            delete_list.append(factor_classes[k][0][l])
                            rule_delete.append(factor_classes[k][0][l])

                        rule_delete=np.unique(rule_delete).tolist()
                        rule_weights.append((len(rule_delete)/data_num))
                        rule_delete=[]
                        
                #收敛数据
                if len(delete_list)!=0:                    
                    data_part[j]=np.delete(data_part[j],delete_list,axis=0)
                    label_part[j]=np.delete(label_part[j],delete_list,axis=0)
                    delete_list=np.unique(delete_list).tolist()
                    #factor_weights[argmax]+=len(delete_list)/data_num
                
            #定义初始完整数据
            data=data_part[0]
            label=label_part[0]

            #组合完整数据
            for j in range(1,class_num):
                data=np.append(data,data_part[j],axis=0)
                label=np.append(label,label_part[j],axis=0)

            #print('remain data:',len(data))
            
            #生成约简因素集
            last_factor=argmax
            used_factor_set=np.append(used_factor_set,last_factor)
            used_factor_set=np.unique(used_factor_set)            
                    
            #判断收敛完成
            if len(data)==0:
                break       

    #转换成整数因素集
    used_factor_set=list(map(int,used_factor_set))
    rules_set=last_rules_set+rules_set
    

    #判断同时返回约简因素集和规则权重
    if used_factors==True and rule_weight==True:
        return rules_set,used_factor_set,rule_weights

    #判断返回约简因素集
    if used_factors==True:
        return rules_set,used_factor_set

    #判断返回规则权重
    if rule_weight==True:
        return rules_set,rule_weights

    #返回规则集
    return rules_set


#####################################

#自适应规则简单删除算法
def simple_batch(rules_set,never_set,data_batch,label_batch,none_value=-1):

    rules_set=np.array(rules_set)
    never_set=np.array(never_set)
    data_num=len(data_batch)
    count=len(rules_set)
    rules_acc_number=[0]*count
    rules_set_index=[]
    never_set_index=[]

    #构建单因素删除集
    for i in range(len(data_batch)):

        #定义临时变量
        np_data=np.asarray(data_batch[i])        

        #遍历规则集
        for j in range(count):
            rule=np.asarray(rules_set[j])
            rule=np.delete(rule,-1)

            #返回匹配结果
            if np.sum(np_data==rule)==np.sum(rule!=none_value):
                if rules_set[j] in delete_set:
                    never_set=np.delete(never_set,np.where(never_set==rules_set[j])[0][0],axis=0)
                    
                if rules_set[j][-1]!=label_batch[i]:
                    rules_set_index.append(j)
                else:
                    rules_acc_number[j]+=1
                    
    #删除规则集规则
    never_set_index=np.where(np.array(rules_acc_number)==0)
    never_set=never_set.tolist()
    never_set+=np.array(rules_set)[never_set_index].tolist()
    rules_set=np.delete(rules_set,rules_set_index,axis=0)
    
    #规则集去重
    if len(rules_set)!=0:
        rules_set=np.unique(rules_set,axis=0).tolist()
    if len(never_set)!=0:
        never_set=np.unique(never_set,axis=0).tolist()

    #返回规则集
    return rules_set,never_set

#####################################

#自适应规则权重算法
def batch_rule_weights(rules_set,rule_weights,rule_time,batch_rules,data_batch,label_batch,return_all_set=False,time_decay=False,study_decay=False,none_value=-1):

    batch_rules=delete_rules(batch_rules,rules_set)
    batch_num=len(batch_rules)
    batch_weights=[0]*batch_num
    batch_time=[0]*batch_num
    rules_set+=batch_rules
    rule_weights+=batch_weights
    rule_time+=batch_time
    data_num=len(data_batch)
    count=len(rules_set)
    rule_time=(np.array(rule_time)+1).tolist()
        
    #构建单因素删除集
    for i in range(data_num):

        #定义临时变量
        np_data=np.asarray(data_batch[i])        

        #遍历规则集
        for j in range(count):
            rule=np.asarray(rules_set[j])
            rule=np.delete(rule,-1)
            time_rate=1.
            study_rate=1.
            memory_rate=1.
            if time_decay==True:
                time_rate=1./rule_time[j]
            if study_decay==True:
                study_rate=1./(batch_num+1)

            memory_rate=time_rate*study_rate

            #返回匹配结果
            if np.sum(np_data==rule)==np.sum(rule!=none_value):
                    
                if rules_set[j][-1]==label_batch[i]:
                    rule_weights[j]+=memory_rate
                else:
                    rule_weights[j]-=memory_rate

    #返回规则集
    if return_all_set==False:      
        return rules_set,rule_weights,rule_time

    right_set_index=np.where(np.array(rule_weights)>0)
    right_set=np.array(rules_set)[right_set_index].tolist()
    never_set_index=np.where(np.array(rule_weights)==0)
    never_set=np.array(rules_set)[never_set_index].tolist()
    wrong_set_index=np.where(np.array(rule_weights)<0)
    wrong_set=np.array(rules_set)[wrong_set_index].tolist()

    return rules_set,rule_weights,rule_time,right_set,never_set,wrong_set
    
    
#####################################

#规则集对比删除
def delete_rules(rules_set,compare_set):

    delete_index=[]

    for i in range(len(rules_set)):

        if rules_set[i] in compare_set:
            delete_index.append(i)

    rules_set=np.delete(rules_set,delete_index,axis=0).tolist()
    
    #返回规则集
    return rules_set



###############################################################################
