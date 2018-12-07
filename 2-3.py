# 2-3 Tree
# balanced tree data structure with up to 2 data items per node
import os
class Node:
	def __init__(self, data, t, g, par = None):
		self.data = list([data]) #Puntaje/clave o score del anime
		self.t = list([t]) #Titulo del anime
		self.g = list([g]) #Genero del anime, float (1,10)
		self.parent = par
		self.child = list()
		
	def __str__(self):
		if self.parent:
			return str(self.parent.data) + ' : ' + str(self.data)
		return 'Root : ' + str(self.data)
	
	def __lt__(self, node):
		return self.data[0] < node.data[0]
		
	def _isLeaf(self):
		return len(self.child) == 0
			
	# merge new_node sub-tree into self node
	def _add(self, new_node):
		# print ("Node _add: " + str(new_node.data) + ' to ' + str(self.data))
		for child in new_node.child:
			child.parent = self
		self.data.extend(new_node.data)
		self.data.sort()
		self.t.extend(new_node.t)
		self.t.sort()
		self.g.extend(new_node.g)
		self.g.sort()
		self.child.extend(new_node.child)
		if len(self.child) > 1:
			self.child.sort()
		if len(self.data) > 2:
			self._split()
	
	# find correct node to insert new node into tree
	def _insert(self, new_node):
		# print ('Node _insert: ' + str(new_node.data) + ' into ' + str(self.data))
		
		# leaf node - add data to leaf and rebalance tree
		if self._isLeaf():
			self._add(new_node)
			
		# not leaf - find correct child to descend, and do recursive insert
		elif new_node.data[0] > self.data[-1]:
			self.child[-1]._insert(new_node)
		else:
			for i in range(0, len(self.data)):
				if new_node.data[0] < self.data[i]:
					self.child[i]._insert(new_node)
					break
	
	# 3 items in node, split into new sub-tree and add to parent	
	def _split(self):
		# print("Node _split: " + str(self.data))
		left_child = Node(self.data[0], self.t[0], self.g[0], self)
		right_child = Node(self.data[2], self.t[2], self.g[2], self)
		if self.child:
			self.child[0].parent = left_child
			self.child[1].parent = left_child
			self.child[2].parent = right_child
			self.child[3].parent = right_child
			left_child.child = [self.child[0], self.child[1]]
			right_child.child = [self.child[2], self.child[3]]
					
		self.child = [left_child]
		self.child.append(right_child)
		self.data = [self.data[1]]
		self.t = [self.t[1]]
		self.g = [self.g[1]]
		
		# now have new sub-tree, self. need to add self to its parent node
		if self.parent:
			if self in self.parent.child:
				self.parent.child.remove(self)
			self.parent._add(self)
		else:
			left_child.parent = self
			right_child.parent = self
			
	# find an item in the tree; return item, or False if not found		
	def _find(self, item):
		# print ("Find " + str(item))
		if item in self.data:
			return item
		elif self._isLeaf():
			return False
		elif item > self.data[-1]:
			return self.child[-1]._find(item)
		else:
			for i in range(len(self.data)):
				if item < self.data[i]:
					return self.child[i]._find(item)
		
	def _remove(self, item):
		pass

	# print preorder traversal		
	def _preorder(self):
		j = 0
		for titulo in self.t:
		    print (titulo, self.data[j]) 
		    j=j+1
		for child in self.child:
			child._preorder()

class Tree:
	def __init__(self):
		self.root = None
		
	def insert(self, item, t, g):
		print("Tree insert: " + str(item))
		if self.root is None:
			self.root = Node(item, t, g)
		else:
			self.root._insert(Node(item, t, g))
			while self.root.parent:
				self.root = self.root.parent
		return True
	
	def find(self, item):
		return self.root._find(item)
		
	def remove(self, item):
		self.root.remove(item)

	def mejor(self):
		print ('----Menor puntaje----')
		sel = self.root
		while (sel.child):
			sel = sel.child
		print(sel.data)

	def preorder(self):
		print ('----Preorder----')
		self.root._preorder()


arbol = Tree()
from jikanpy import Jikan
jikan = Jikan()
action = jikan.genre(type='anime', genre_id=1) # Obtiene los anime correspondientes a genero_id, 1=action
for anime in action["anime"]:
    #arbol.insert(anime["score"])
    arbol.insert(anime["score"],anime["title"],1)
    #print(anime["titulo"], anime["score"]) # Imprime cada anime con su respectiva puntuación

while True:
    os.system("cls")
    print("Arbol 2-3")
    opc = input("\n1.-Insertar nodo(anime) \n2.-Lista de Animes\n3.-Buscar \n4.-Eliminar \n5.-Salir \n\nElige una opcion -> ")

    if opc == '1':
        name = input("\nIngresa el nombre -> ")
        score = input("\nIngresa puntuacion -> ")
        genero = input("\nIngresa id_genero -> ")
        arbol.insert(float(score),name,float(genero))
    elif opc == '2':
        #arbol.preorder()
        arbol.mejor()
    elif opc == '3':
        nodo = input("\nIngresa el puntaje del nodoAnime a buscar -> ")
        nodo = float(nodo)
        res = arbol.search(nodo)
    elif opc == '4':
        nodo = input("\nIngresa el puntaje del nodoAnime a Eliminar -> ")
        nodo = float(nodo)
        arbol.delete(nodo)
    elif opc == '5':
        print("\nElegiste salir...\n")
        os.system("pause")
        break
    else:
        print("\nElige una opcion correcta...")
    print()
    os.system("pause")

print()