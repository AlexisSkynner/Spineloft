import copy
import math
import bpy


#Forme à copier
class Shape():
    def __init__(self, vertices, edges, faces):
        self.vertices = vertices
        self.edges = edges
        self.faces = faces

def cos_sin_between_vectors(u, v):
    dot_product = sum(i*j for i, j in zip(u, v))
    vect_product = u[0]*v[1]-u[1]*v[0]
    norm_u = math.sqrt(sum(i**2 for i in u))
    norm_v = math.sqrt(sum(i**2 for i in v))

    if norm_u*norm_v==0:
        cos_theta=1
        sin_theta=0
    else:
        cos_theta = dot_product / (norm_u * norm_v)
        sin_theta = vect_product / (norm_u * norm_v)
    return (cos_theta,sin_theta)




def norm(u):
    return(math.sqrt(sum(i**2 for i in u)))



def sum_matrices(A,B):
    C=[]
    for i in range(len(A)):
        C.append(A[i]+B[i])
    return(C)


def diff_matrices(A,B):
    C=[]
    for i in range(len(A)):
        C.append(A[i]-B[i])
    return(C)

def dot(matrice, vecteur):
    n = len(matrice)
    resultat = []

    for i in range(n):
        somme = 0
        for j in range(n):
            produit = matrice[i][j] * vecteur[j]
            somme = somme + produit
        resultat.append(somme)

    return resultat



def rot(shape:Shape,cos_sin_theta:float):
    c=cos_sin_theta[0]
    s=cos_sin_theta[1]

    mat=[[c,s,0],[-s,c,0],[0,0,1]]


    shape2=copy.deepcopy(shape)
    vertices=shape2.vertices
    

    for i in range(len(vertices)):
        col=list(vertices[i])
        res=dot(mat,col)
        vertices[i]=tuple(res)

    return(shape2)

def homo(shape:Shape,h:float):
    shape2=copy.deepcopy(shape)
    vertices=list(shape2.vertices)


    for i in range(len(vertices)):
        vertices[i]=tuple([x * h for x in vertices[i]])
    shape2.vertices=vertices
    return(shape2)

def transl(shape:Shape,vect:tuple):
    shape2=copy.deepcopy(shape)
    vertices=shape2.vertices
    
    for i in range(len(vertices)):
        vertices[i]=tuple(sum_matrices(list(vertices[i]), list(vect)))
    return(shape2)

def middle(p1:tuple,p2:tuple):
    return ( ( (p1[0]+p2[0])/2 , (p1[1]+p2[1])/2 , (p1[2]+p2[2])/2))





                 




#########################################################################################################################
#Données à entrer

# Figure à répéter
#Heart
A=[(0,0,0),(-2,0,2),(-2,0,3),(-1,0,4),(0,0,3),(1,0,4),(2,0,3),(2,0,2)] #Il faut une figure qui fait face vers les y (y=0 pour tout point), dont le centre est en 0,0,0, de largeur 1
B=[(0,7)]+[(i,i+1) for i in range(7)]
C=[]

shapeHeart=copy.deepcopy(homo(Shape(A,B,C),0.25))

#Circle
A=[(math.cos(2*math.pi*k/20), 0, math.sin(2*math.pi*k/20)) for k in range(20)] #Il faut une figure qui fait face vers les y (y=0 pour tout point), dont le centre est en 0,0,0, de largeur 1
B=[(0,19)]+[(i,i+1) for i in range(19)]
C=[]

shapeCircle=copy.deepcopy(homo(Shape(A,B,C),0.5))

#Square
A=[(-0.5,0,-0.5),(0.5,0,-0.5),(0.5,0,0.5),(-0.5,0,0.5)]
B=[(0,3)]+[(i,i+1) for i in range (3)]
C=[]
shapeSquare=copy.deepcopy(Shape(A,B,C))

#rib
A=[(-0.5,0,0),(0.5,0,0)]
B=[(0,1)]
C=[]
shapeRib=copy.deepcopy(Shape(A,B,C))





shapeStart = shapeRib


def addVertices(startShape:Shape,listPts:list):
    l=len(listPts)
    
    #Calcul des milieux + norme de segments, et des angles avec (1,0,0)
    listMid=[]
    listAngl=[]
    listDist=[]
    for i in range(l):
        listMid.append(middle(listPts[i][0],listPts[i][1]))
        listAngl.append(cos_sin_between_vectors(diff_matrices(list(listPts[i][1]),list(listPts[i][0])) , (1,0,0) ))
        listDist.append(norm(diff_matrices(list(listPts[i][0]),list(listPts[i][1]))))

    #On trace la forme finale
    finalShape=Shape([],[],[])
    for i in range(l):
        newShape=transl(homo(rot(startShape, listAngl[i]),listDist[i]),listMid[i])
        finalShape.vertices.extend(newShape.vertices)

    return(finalShape)

def addEdges(finalShape:Shape,startShape:Shape, listPts:list, shape:int):
    l=len(listPts)
    nbEdges=len(startShape.edges)
    nbVertices=len(startShape.vertices)

    #Edges de la forme de départ
    for i in range( l ):
        for j in range(nbEdges):
            edge=list(startShape.edges[j])
            edge0=edge[0]+i*nbVertices
            edge1=edge[1]+i*nbVertices
            finalShape.edges.append((edge0,edge1))
    
    if shape!=0:       
        #Edges  de la connection
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
        lastFace.append(nbVertices*(l-1)+i) 

    finalShape.faces.append(tuple(firstFace))
    finalShape.faces.append(tuple(lastFace))
    
    return(finalShape)






def giveMeTheMesh(listPts,shape, listVertices=None):
    if shape==0:
        newList=[]
        for i in range(len(listPts)//2):
            newList.append([listPts[2*i],listPts[2*i+1]])
        
        finalShape=addVertices(shapeRib,newList)
        finalShape=addEdges(finalShape,shapeRib, newList, shape)


    elif shape==2:
        newList=[]
        for i in range(len(listPts)//2):
            newList.append([listPts[2*i],listPts[2*i+1]])
        
        finalShape=addVertices(shapeSquare,newList)
        finalShape=addEdges(finalShape,shapeSquare, newList,shape)
        finalShape=addFaces(finalShape,shapeSquare, newList)

    elif shape==3 and listVertices!=None and len(listVertices)>=2:
        newList=[]
        for i in range(len(listPts)//2):
            newList.append([listPts[2*i],listPts[2*i+1]])

        print(listVertices)
        A=[(p[0],0,p[1]) for p in listVertices] #Il faut une figure qui fait face vers les y (y=0 pour tout point), dont le centre est en 0,0,0, de largeur 1
        B=[(0,len(A)-1)]+[(i,i+1) for i in range(len(A)-1)]
        C=[]
        
        min_x=A[0][0]
        max_x=A[0][0]
        for p in A:
            x=p[0]
            if x<min_x:
                min_x=x
            if x>max_x:
                max_x=x
        
        width=max_x-min_x
        if width==0:
            width=1

        shapeCustom=copy.deepcopy(homo(Shape(A,B,C),1/width))

        finalShape=addVertices(shapeCustom,newList)
        finalShape=addEdges(finalShape,shapeCustom, newList,shape)
        finalShape=addFaces(finalShape,shapeCustom, newList)


    else: #Cas de base = cercle
        newList=[]
        for i in range(len(listPts)//2):
            newList.append([listPts[2*i],listPts[2*i+1]])
        
        finalShape=addVertices(shapeCircle,newList)
        finalShape=addEdges(finalShape,shapeCircle, newList,shape)
        finalShape=addFaces(finalShape,shapeCircle, newList)

    return(finalShape.vertices,finalShape.edges,finalShape.faces)

