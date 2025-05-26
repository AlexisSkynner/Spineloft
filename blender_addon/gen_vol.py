import copy
import math
import numpy as np
import bpy


#Forme à copier
class Shape():
    def __init__(self, vertices, edges, faces):
        self.vertices = vertices
        self.edges = edges
        self.faces = faces

def angle_between_vectors(u, v):
    dot_product = sum(i*j for i, j in zip(u, v))
    norm_u = math.sqrt(sum(i**2 for i in u))
    norm_v = math.sqrt(sum(i**2 for i in v))
    cos_theta = dot_product / (norm_u * norm_v)
    angle_rad = math.acos(cos_theta)
    return angle_rad

def norm(u):
    return(math.sqrt(sum(i**2 for i in u)))

def rot(shape:Shape,theta:float):
    c=np.cos(theta)
    s=np.sin(theta)

    mat=np.array([[c,-s,0],[s,c,0],[0,0,1]])


    shape2=copy.deepcopy(shape)
    vertices=shape2.vertices
    

    for i in range(len(vertices)):
        col=np.array(vertices[i]).T
        res=np.dot(mat,col).T
        vertices[i]=tuple(res)

 
    return(shape2)

def homo(shape:Shape,h:float):
    shape2=copy.deepcopy(shape)
    vertices=shape2.vertices


    for i in range(len(vertices)):
        vertices[i]=tuple(h*np.array( vertices[i] ))
    return(shape2)

def transl(shape:Shape,vect:tuple):
    shape2=copy.deepcopy(shape)
    vertices=shape2.vertices
    
    for i in range(len(vertices)):
        vertices[i]=tuple(np.array(vertices[i]) + np.array(vect))
    return(shape2)

def middle(p1:tuple,p2:tuple):
    return ( ( (p1[0]+p2[0])/2 , (p1[1]+p2[1])/2 , (p1[2]+p2[2])/2))

def printVertices(shape:Shape):
    X=[]
    Y=[]
    Z=[]

    for u in shape.vertices:
        X.append(u[0])
        Y.append(u[1])
        Z.append(u[2])

    ax = plt.axes(projection='3d')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.plot3D(X,Y,Z, 'o:r',linestyle='None')
    plt.show()

def printEdges(shape:Shape):
    ax = plt.axes(projection='3d')

    for edge in shape.edges:
    
        X=[]
        Y=[]
        Z=[]

        j1,j2=edge[0],edge[1]
        vertices=shape.vertices

        for j in [j1,j2]:
            X.append(vertices[j][0])
            Y.append(vertices[j][1])
            Z.append(vertices[j][2])

        ax.plot3D(X,Y,Z, 'b')

    ax.set_xlim(0,4)
    ax.set_ylim(0,4)
    ax.set_zlim(-2,2)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    plt.show()    




                 




#########################################################################################################################
#Données à entrer

# Figure à répéter
#Heart
A=[(0,0,0),(-2,0,2),(-2,0,3),(-1,0,4),(0,0,3),(1,0,4),(2,0,3),(2,0,2)] #Il faut une figure qui fait face vers les y (y=0 pour tout point), dont le centre est en 0,0,0, de largeur 1
B=[(0,7)]+[(i,i+1) for i in range(7)]
C=[]

shapeHeart=copy.deepcopy(homo(Shape(A,B,C),0.25))


#Square
A=[(-0.5,0,-0.5),(0.5,0,-0.5),(0.5,0,0.5),(-0.5,0,0.5)]
B=[(0,3)]+[(i,i+1) for i in range (3)]
C=[]

shapeSquare=copy.deepcopy(Shape(A,B,C))

#Circle
n=20
X=np.arange(0,n)
A=[(0.5*np.cos(2*np.pi*x/n) , 0, 0.5*np.sin(2*np.pi*x/n)) for x in X]
B=[(0,n-1)]+[(i,i+1) for i in range (n-1)]
C=[]

shapeCircle=copy.deepcopy(Shape(A,B,C))



shapeStart = shapeCircle


def addVertices(startShape:Shape,listPts:list):
    l=len(listPts)
    
    #Calcul des milieux + norme de segments, et des angles avec (1,0,0)
    listMid=[]
    listAngl=[]
    listDist=[]
    for i in range(l):
        listMid.append(middle(listPts[i][0],listPts[i][1]))
        listAngl.append(angle_between_vectors(np.array(listPts[i][0])-np.array(listPts[i][1]) , (1,0,0) ))
        listDist.append(norm(np.array(listPts[i][0])-np.array(listPts[i][1])))

    #On trace la forme finale
    finalShape=Shape([],[],[])
    for i in range(l):
        newShape=transl(homo(rot(startShape, listAngl[i]),listDist[i]),listMid[i])
        finalShape.vertices.extend(newShape.vertices)

    return(finalShape)

def addEdges(finalShape:Shape,startShape:Shape, listPts:list):
    l=len(listPts)
    nbEdges=len(startShape.edges)
    nbVertices=len(startShape.vertices)

    #Edges de la forme de départ
    for i in range( l ):
        for j in range(nbEdges):
            edge=np.array(startShape.edges[j])
            edge[0]=edge[0]+i*nbVertices
            edge[1]=edge[1]+i*nbVertices
            finalShape.edges.append(tuple(edge))
            
    #Edges et faces de la connection
    for i in range(l-1):
        for j in range(nbVertices):
            finalShape.edges.append( ( nbVertices*i+j , nbVertices*(i+1)+j ) )



    return(finalShape)

def addFaces(finalShape:Shape,startShape:Shape, listPts:list):
    l=len(listPts)
    nbEdges=len(startShape.edges)
    nbVertices=len(startShape.vertices)

    for i in range(l-1):
        for j in range(nbEdges):
            e1=i*nbEdges+j
            e2=(i+1)*nbEdges+j
            face=(finalShape.edges[e1][0],finalShape.edges[e2][0],finalShape.edges[e2][1],finalShape.edges[e1][1])

            
            finalShape.faces.append(tuple(face))
    
    #Ajout de la face de début et de fin
    firstFace=[]
    lastFace=[]  
    for i in range(nbVertices):
        firstFace.append(i)
        lastFace.append(nbVertices*l-i-1)
    
    finalShape.faces.append(tuple(firstFace))
    finalShape.faces.append(tuple(lastFace))
    
    return(finalShape)






def giveMeTheMesh(listPts):

    finalShape=addVertices(shapeStart,listPts)
    finalShape=addEdges(finalShape,shapeStart, listPts)
    finalShape=addFaces(finalShape,shapeStart, listPts)

    return(finalShape.vertices,finalShape.edges,finalShape.faces)

