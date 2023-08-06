
# coding: utf-8

# In[222]:

import numpy as np
import pandas as pd 

import sklearn
from sklearn import svm


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#get_ipython().magic(u'matplotlib inline')
from mpl_toolkits.mplot3d import Axes3D
import tempfile

#pd.set_option('display.mpl_style', 'default')
# Always display all the columns
pd.set_option('display.width', 5000) 
pd.set_option('display.max_columns', 60) 

def readdata(filename):
    A=pd.read_excel(filename)
    B = pd.DataFrame()
    B['x'] = A.iloc[:,1]
    return B


# In[223]:

def genData(filename='A2.xlsx'):
    n = 200
    x1 = [np.random.chisquare(1) for i in range(n)]
    x2 = [np.random.chisquare(1) for i in range(n)]
    x3 = [np.random.chisquare(1) for i in range(n)]
    A = pd.DataFrame()
    A['x1']=x1
    A['x2']=x2
    A['x3']=x3
    A.to_excel(filename)
    #genData("A2.xlsx")
    plt.scatter(x1,x2)
    fig = plt.figure(1)
    ax = Axes3D(fig, elev=-150, azim=110)
    ax.scatter(A.iloc[:,0],A.iloc[:,1],A.iloc[:,2], cmap=plt.cm.Paired)
    


# # PCA

# In[224]:

def PCA(A):
    #A = pd.read_excel('A2.xlsx')
    from sklearn.decomposition import PCA
    X_reduced = PCA(n_components=2).fit_transform(A)
    X_r = pd.DataFrame(X_reduced)
    X_r.plot(kind='scatter',x=0,y=1)


# # SVDD

# In[226]:

def SVDD(A):
    clf = sklearn.svm.OneClassSVM(nu=0.261, gamma=0.05)
    clf.fit(A.iloc[:,0:2])
    xx1, yy1 = np.meshgrid(np.linspace(A.iloc[:, 0].min()-1, A.iloc[:, 0].max()+1, len(A.iloc[:, 0])),                              np.linspace(A.iloc[:, 1].min()-1, A.iloc[:, 1].max()+1, len(A.iloc[:, 1])))
    Z0 = clf.decision_function(np.c_[xx1.ravel(), yy1.ravel()])
    Z1 = Z0.reshape(xx1.shape)
    
    plt.title("svdd")
    legend1 = {}
    legend1['svdd'] = plt.contour(
            xx1, yy1, Z1, levels=[0], linewidths=2, colors='b')
    legend1_values_list = list(legend1.values())
    legend1_keys_list = list(legend1.keys())
    plt.scatter(A.iloc[:, 0], A.iloc[:, 1], color='black')
    bbox_args = dict(boxstyle="round", fc="0.8")
    arrow_args = dict(arrowstyle="->")
    plt.annotate("several confounded points", xy=(24, 19),
                 xycoords="data", textcoords="data",
                 xytext=(13, 10), bbox=bbox_args, arrowprops=arrow_args)
    plt.xlim((xx1.min(), xx1.max()))
    plt.ylim((yy1.min(), yy1.max()))
    plt.ylabel(A.columns.values[1])
    plt.xlabel(A.columns.values[0])
    legend1 = plt.contour(
            xx1, yy1, Z1, levels=[0], linewidths=2, colors='b')

    plt.legend([legend1.collections[0]],['svdd'],loc="upper right", prop=matplotlib.font_manager.FontProperties(size=12))
    return Z0
   


# # KMeans

# In[227]:

def KMeans(A):
    from sklearn.cluster import KMeans
    est = KMeans(n_clusters=3, n_init=1,init='random')
    est.fit(A)
    labels = est.labels_
    fig = plt.figure(1)
    ax = Axes3D(fig, elev=-150, azim=110)
    ax.scatter(A.iloc[:,0],A.iloc[:,1],A.iloc[:,2], c=labels.astype(np.float))#,cmap=plt.cm.Paired)
    return labels


# # test

# In[228]:

if __name__ == '__main__':
    #genData("A2.xlsx")
    A = pd.read_excel('A2.xlsx')
    Z0=SVDD(A)
    #plt.plot(Z0)
    #plt.savefig
    labels = KMeans(A)
    #plt.savefig
    


# In[ ]:




# In[ ]:



