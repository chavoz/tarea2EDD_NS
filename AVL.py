import os
import time
class Node():
    def __init__(self, key,titulo,genero):
        self.key = key #Puntaje o Calificacion del anime, numero float entre 1 y 10
        self.titulo = titulo
        self.genero = genero
        self.left = None 
        self.right = None 


class AVLTree():
    def __init__(self):
        self.node = None 
        self.height = -1  
        self.balance = 0; 
                
    def height(self):
        if self.node: 
            return self.node.height 
        else: 
            return 0 
    
    def is_leaf(self):
        return (self.height == 0) 
    
    def insert(self, key,tit,gen):
        tree = self.node
        newnode = Node(key,tit,gen)
        if tree == None:
            self.node = newnode 
            self.node.left = AVLTree() 
            self.node.right = AVLTree()
            #print("Inserted key [" + str(key) + "]")
        elif key < tree.key: 
            self.node.left.insert(key,tit,gen)
            
        elif key > tree.key: 
            self.node.right.insert(key,tit,gen)
        else: 
            self.node.left.insert(key,tit,gen)
            print("Key [" + str(key) + "] added duplicated.")
        self.rebalance() 
        
    def rebalance(self):
        # key inserted. Let's check if we're balanced
        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1: 
            if self.balance > 1:
                if self.node.left.balance < 0:  
                    self.node.left.lrotate() # we're in case II
                    self.update_heights()
                    self.update_balances()
                self.rrotate()
                self.update_heights()
                self.update_balances()
                
            if self.balance < -1:
                if self.node.right.balance > 0:  
                    self.node.right.rrotate() # we're in case III
                    self.update_heights()
                    self.update_balances()
                self.lrotate()
                self.update_heights()
                self.update_balances()


            
    def rrotate(self):
        # Rotate left pivoting on self
        print('Rotating ' + str(self.node.key) + ' right') 
        A = self.node 
        B = self.node.left.node 
        T = B.right.node 
        
        self.node = B 
        B.right.node = A 
        A.left.node = T 

    
    def lrotate(self):
        # Rotate left pivoting on self
        print('Rotating ' + str(self.node.key) + ' left') 
        A = self.node 
        B = self.node.right.node 
        T = B.left.node 
        
        self.node = B 
        B.left.node = A 
        A.right.node = T 
        
            
    def update_heights(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.update_heights()
                if self.node.right != None:
                    self.node.right.update_heights()
            
            self.height = max(self.node.left.height,
                              self.node.right.height) + 1 
        else: 
            self.height = -1 
            
    def update_balances(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.update_balances()
                if self.node.right != None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height 
        else: 
            self.balance = 0 

    def search(self, key):
        if self.node != None: 
            if self.node.key == key: 
                print("Anime Encontrado ... " + self.node.titulo + " = " + str(key))  
                return  
            elif key < self.node.key: 
                self.node.left.search(key)  
            elif key > self.node.key: 
                self.node.right.search(key)
        else: 
            print("No Encontrado anime con calificacion ",str(key)," ...")  
            return 

    def delete(self, key):
        # print("Trying to delete at node: " + str(self.node.key))
        if self.node != None: 
            if self.node.key == key: 
                print("Borrando ... " + self.node.titulo + " = " + str(key))  
                if self.node.left.node == None and self.node.right.node == None:
                    self.node = None # leaves can be killed at will 
                # if only one subtree, take that 
                elif self.node.left.node == None: 
                    self.node = self.node.right.node
                elif self.node.right.node == None: 
                    self.node = self.node.left.node
                
                # worst-case: both children present. Find logical successor
                else:  
                    replacement = self.logical_successor(self.node)
                    if replacement != None: # sanity check 
                        print("Found replacement for " + str(key) + " -> " + str(replacement.key))  
                        self.node.key = replacement.key 
                        self.node.titulo = replacement.titulo
                        self.node.genero = replacement.genero
                        
                        # replaced. Now delete the key from right child 
                        self.node.right.delete(replacement.key)
                    
                self.rebalance()
                return  
            elif key < self.node.key: 
                self.node.left.delete(key)  
            elif key > self.node.key: 
                self.node.right.delete(key)
                        
            self.rebalance()
        else: 
            return 

    def logical_predecessor(self, node):
        node = node.left.node 
        if node != None: 
            while node.right != None:
                if node.right.node == None: 
                    return node 
                else: 
                    node = node.right.node  
        return node 
    
    def logical_successor(self, node):
        node = node.right.node  
        if node != None: # just a sanity check  
            
            while node.left != None:
                if node.left.node == None: 
                    return node 
                else: 
                    node = node.left.node  
        return node 

    def check_balanced(self):
        if self == None or self.node == None: 
            return True
        
        # We always need to make sure we are balanced 
        self.update_heights()
        self.update_balances()
        return ((abs(self.balance) < 2) and self.node.left.check_balanced() and self.node.right.check_balanced())  

    def inorder_traverse(self):
        if self.node == None:
            return [] 
        
        inlist = [] 
        l = self.node.left.inorder_traverse()
        for i in l: 
            inlist.append(i) 

        inlist.append(self.node.titulo+" "+str(self.node.key))

        l = self.node.right.inorder_traverse()
        for i in l: 
            inlist.append(i) 
        return inlist 

id_genero = input('Ingrese ID del tipo/genero anime desea agregar al arbol -> ')
from jikanpy import Jikan
jikan = Jikan()
action = jikan.genre(type='anime', genre_id=int(id_genero)) # Obtiene los anime correspondientes a genero_id, 1=action
arbol = AVLTree()
inicio = time.time()
for anime in action["anime"]:
    arbol.insert(anime["score"],anime["title"],float(id_genero))
print("Animes del genero ", str(id_genero), "agregados")
final = time.time()
print("Se demoro",(final-inicio),"segundos")
    #print(anime["titulo"], anime["score"]) # Imprime cada anime con su respectiva puntuación
    
while True:
    #os.system("cls")
    print("Arbol AVL")
    opc = input("\n1.-Insertar nodo(anime) \n2.-Inorden (Lista animes MENOR a MAYOR calificacion)\n3.-Buscar \n4.-Eliminar \n5.-Salir \n\nElige una opcion -> ")

    if opc == '1':
        name = input("\nIngresa el nombre -> ")
        score = input("\nIngresa puntuacion -> ")
        genero = input("\nIngresa id_genero -> ")
        arbol.insert(float(score),name,float(genero))
    elif opc == '2':
        list = arbol.inorder_traverse()
        for anime in list:
            print(anime)
    elif opc == '3':
        inicio = time.time()
        nodo = input("\nIngresa el puntaje del nodoAnime a buscar -> ")
        nodo = float(nodo)
        res = arbol.search(nodo)
        fin = time.time()
        print("Se demoro",(fin-inicio),"segundos")
    elif opc == '4':
        inicio = time.time()
        nodo = input("\nIngresa el puntaje del nodoAnime a Eliminar -> ")
        nodo = float(nodo)
        arbol.delete(nodo)
        fin = time.time()
        print("Se demoro",(fin-inicio),"segundos")
    elif opc == '5':
        print("\nElegiste salir...\n")
        os.system("pause")
        break
    else:
        print("\nElige una opcion correcta...")
    print()
    os.system("pause")

print()
        
