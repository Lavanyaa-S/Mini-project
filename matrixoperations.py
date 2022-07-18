import numpy as np
import eccoperations as ec
def transpose(X):
    result = [[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]
    return result
def matrix_multiplication(A,B):
    result = [[0], [0], [0], [0]]
    for i in range(len(A)):

        # iterating by column by B
        for j in range(len(B[0])):

            # iterating by rows of B
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]

    #for r in result:
        #print(r)
    return result
def inverse_key_formation(initial_key_Ki,a,b,p,G):
    #initiating the required lists
    invertMat=[]
    K=[]
    K22=[[0,0],[0,0]]
    Identity_mat=np.array([[1,0],[0,1]])

    #formation of the K11 big matrix which consistes of k11,k12,k21,k22 #K11=x.G k12=y.G
    K1 = list(ec.double_and_add(initial_key_Ki[0], G, p, a))
    K2 = list(ec.double_and_add(initial_key_Ki[1], G, p, a))
    K.append(K1)
    K.append(K2)

    #formation of big K12 Matrix which consists of k13 k14 k23 k24 #K12=I-K11
    K11=np.array(K)
    K12=np.subtract(Identity_mat,K11)
    for i in range(0,2):
        for j in range(0,2):
            if K12[i][j]<0 :
                K12[i][j] = K12[i][j] % 256
    temp1 = K12[0].tolist()
    temp2 = K12[1].tolist()
    for k in temp1:
        K1.append(k)
    for l in temp2:
        K2.append(l)

    invertMat.append(K1)
    invertMat.append(K2)

    #formation of big K21 MAtrix which contains of k31 k32 k41 k42 #K21= I+K11

    K21 = np.add(Identity_mat,K11)

    #formation of big K22 matrix which contains k33 k34 k43 k44  #K22=-K1

    for i in range(0,2):
        for j in range(0,2):
            K22[i][j] = 256 - K11[i][j]

    temp3 = K21[0].tolist()
    temp4 = K21[1].tolist()
    for m in K22[0]:
        temp3.append(m)
    for n in K22[1]:
        temp4.append(n)

    invertMat.append(temp3)
    invertMat.append(temp4)
    return invertMat