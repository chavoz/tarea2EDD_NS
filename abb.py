import os
class NodoArbol:
    def __init__(self,clave,titulo,genero,izquierdo=None,derecho=None,padre=None):
        self.clave = clave
        self.titulo = titulo
        self.genero = genero
        self.hijoIzquierdo = izquierdo
        self.hijoDerecho = derecho
        self.padre = padre
    def tieneHijoIzquierdo(self):
        return self.hijoIzquierdo
    def tieneHijoDerecho(self):
        return self.hijoDerecho
    def esHijoIzquierdo(self):
        return self.padre and self.padre.hijoIzquierdo == self
    def esHijoDerecho(self):
        return self.padre and self.padre.hijoDerecho == self
    def esRaiz(self):
        return not self.padre
    def esHoja(self):
        return not (self.hijoDerecho or self.hijoIzquierdo)
    def Hijo(self):
        return self.hijoDerecho or self.hijoIzquierdo
    def tieneAmbosHijos(self):
        return self.hijoDerecho and self.hijoIzquierdo
    def reemplazarDatoDeNodo(self,clave,titulo,genero,hizq,hder):
        self.clave = clave
        self.titulo = titulo
        self.genero = genero
        self.hijoIzquierdo = hizq
        self.hijoDerecho = hder
        if self.tieneHijoIzquierdo():
            self.hijoIzquierdo.padre = self
        if self.tieneHijoDerecho():
            self.hijoDerecho.padre = self

class ArbolABB:

    def __init__(self):
        self.raiz = None
        self.tamano = 0
    def longitud(self):
        return self.tamano
    def __len__(self):
        return self.tamano
    def agregar(self,clave,titulo,genero):
        if self.raiz:
            self._agregar(clave,titulo,genero,self.raiz)
        else:
            self.raiz = NodoArbol(clave,titulo,genero)
        self.tamano = self.tamano + 1
    def _agregar(self,clave,titulo,genero,nodoActual):
        if clave < nodoActual.clave:
            if nodoActual.tieneHijoIzquierdo():
                   self._agregar(clave,titulo,genero,nodoActual.hijoIzquierdo)
            else:
                   nodoActual.hijoIzquierdo = NodoArbol(clave,titulo,genero,padre=nodoActual)
        else:
            if nodoActual.tieneHijoDerecho():
                   self._agregar(clave,titulo,genero,nodoActual.hijoDerecho)
            else:
                   nodoActual.hijoDerecho = NodoArbol(clave,titulo,genero,padre=nodoActual)
    def __setitem__(self,c,v):
       self.agregar(c,v)
    def obtener(self,clave):
       if self.raiz:
           res = self._obtener(clave,self.raiz)
           if res:
                  return res.titulo
           else:
                  return None
       else:
           return None
    def _obtener(self,clave,nodoActual):
       if not nodoActual:
           return None
       elif nodoActual.clave == clave:
           return nodoActual
       elif clave < nodoActual.clave:
           return self._obtener(clave,nodoActual.hijoIzquierdo)
       else:
           return self._obtener(clave,nodoActual.hijoDerecho)
    def __getitem__(self,clave):
       return self.obtener(clave)
    def __contains__(self,clave):
       if self._obtener(clave,self.raiz):
           return True
       else:
           return False
    def eliminar(self,clave):
      if self.tamano > 1:
         nodoAEliminar = self._obtener(clave,self.raiz)
         if nodoAEliminar!=None:
             print("[",nodoAEliminar.clave,"] =",nodoAEliminar.titulo," Fue eliminado")
             self.remover(nodoAEliminar)
             self.tamano = self.tamano-1
         else:
             print('Error, la clave no está en el árbol')
      elif self.tamano == 1 and self.raiz.clave == clave:
         self.raiz = None
         self.tamano = self.tamano - 1
      else:
         print('Error, la clave no está en el árbol')
    def __delitem__(self,clave):
       self.eliminar(clave)
    def empalmar(self):
       if self.esHoja():
           if self.esHijoIzquierdo():
                  self.padre.hijoIzquierdo = None
           else:
                  self.padre.hijoDerecho = None
       elif self.Hijo():
           if self.tieneHijoIzquierdo():
                  if self.esHijoIzquierdo():
                     self.padre.hijoIzquierdo = self.hijoIzquierdo
                  else:
                     self.padre.hijoDerecho = self.hijoIzquierdo
                  self.hijoIzquierdo.padre = self.padre
           else:
                  if self.esHijoIzquierdo():
                     self.padre.hijoIzquierdo = self.hijoDerecho
                  else:
                     self.padre.hijoDerecho = self.hijoDerecho
                  self.hijoDerecho.padre = self.padre
    def inorder(self, a):
        if a == None:
            return None
        else:
            self.inorder(a.hijoIzquierdo)
            print(a.titulo, a.clave)
            self.inorder(a.hijoDerecho)
    def preorder(self, a):
        if a == None:
            return None
        else:
            print(a.titulo, a.clave)
            self.preorder(a.hijoIzquierdo)
            self.preorder(a.hijoDerecho)
    def postorder(self, a):
        if a == None:
            return None
        else:
            self.postorder(a.hijoIzquierdo)
            self.postorder(a.hijoDerecho)
            print(a.titulo, a.clave)
    def encontrarSucesor(self):
      suc = None
      if self.tieneHijoDerecho():
          suc = self.hijoDerecho.encontrarMin()
      else:
          if self.padre:
                 if self.esHijoIzquierdo():
                     suc = self.padre
                 else:
                     self.padre.hijoDerecho = None
                     suc = self.padre.encontrarSucesor()
                     self.padre.hijoDerecho = self
      return suc
    def encontrarMin(self):
      actual = self
      while actual.tieneHijoIzquierdo():
          actual = actual.hijoIzquierdo
      return actual
    def remover(self,nodoActual):
         if nodoActual.esHoja(): #hoja
           if nodoActual == nodoActual.padre.hijoIzquierdo:
               nodoActual.padre.hijoIzquierdo = None
           else:
               nodoActual.padre.hijoDerecho = None
         elif nodoActual.tieneAmbosHijos(): #interior
           suc = nodoActual.encontrarSucesor()
           suc.empalmar()
           nodoActual.clave = suc.clave
           nodoActual.titulo = suc.titulo
           nodoActual.genero = suc.genero

         else: # este nodo tiene un (1) hijo
           if nodoActual.tieneHijoIzquierdo():
             if nodoActual.esHijoIzquierdo():
                 nodoActual.hijoIzquierdo.padre = nodoActual.padre
                 nodoActual.padre.hijoIzquierdo = nodoActual.hijoIzquierdo
             elif nodoActual.esHijoDerecho():
                 nodoActual.hijoIzquierdo.padre = nodoActual.padre
                 nodoActual.padre.hijoDerecho = nodoActual.hijoIzquierdo
             else:
                 nodoActual.reemplazarDatoDeNodo(nodoActual.hijoIzquierdo.clave,
                                    nodoActual.hijoIzquierdo.titulo,
                                    nodoActual.hijoIzquierdo.genero,
                                    nodoActual.hijoIzquierdo.hijoIzquierdo,
                                    nodoActual.hijoIzquierdo.hijoDerecho)
           else:
             if nodoActual.esHijoIzquierdo():
                 nodoActual.hijoDerecho.padre = nodoActual.padre
                 nodoActual.padre.hijoIzquierdo = nodoActual.hijoDerecho
             elif nodoActual.esHijoDerecho():
                 nodoActual.hijoDerecho.padre = nodoActual.padre
                 nodoActual.padre.hijoDerecho = nodoActual.hijoDerecho
             else:
                 nodoActual.reemplazarDatoDeNodo(nodoActual.hijoDerecho.clave,
                                    nodoActual.hijoDerecho.titulo,
                                    nodoActual.hijoDerecho.genero,
                                    nodoActual.hijoDerecho.hijoIzquierdo,
                                    nodoActual.hijoDerecho.hijoDerecho)


id_genero = input('Ingrese ID del tipo/genero anime desea agregar al arbol -> ')
from jikanpy import Jikan
jikan = Jikan()
action = jikan.genre(type='anime', genre_id=int(id_genero)) # Obtiene los anime correspondientes a genero_id, 1=action
arbol = ArbolABB()
for anime in action["anime"]:
    arbol.agregar(anime["score"],anime["title"],float(id_genero))
print("Animes del genero ", str(id_genero), "agregados")
    #print(anime["titulo"], anime["score"]) # Imprime cada anime con su respectiva puntuación
	
while True:
    os.system("cls")
    print("Arbol ABB")
    opc = input("\n1.-Insertar nodo(anime) \n2.-Inorden (Lista animes MENOR a MAYOR calificacion) \n3.-Preorden \n4.-Postorden \n5.-Buscar \n6.-Eliminar \n7.-Salir \n\nElige una opcion -> ")

    if opc == '1':
        name = input("\nIngresa el nombre -> ")
        score = input("\nIngresa puntuacion -> ")
        genero = input("\nIngresa id_genero -> ")
        arbol.agregar(float(score),name,float(genero))
    elif opc == '2':
        if arbol.raiz == None:
            print("Vacio")
        else:
            arbol.inorder(arbol.raiz)
    elif opc == '3':
        if arbol.raiz == None:
            print("Vacio")
        else:
            arbol.preorder(arbol.raiz)
    elif opc == '4':
        if arbol.raiz == None:
            print("Vacio")
        else:
            arbol.postorder(arbol.raiz)
    elif opc == '5':
        nodo = input("\nIngresa el nodo(puntaje) a buscar -> ")
        nodo = float(nodo)
        res = arbol._obtener(nodo, arbol.raiz)
        if res == None:
            print("\nNodo no encontrado...")
        else:
            print("\nNodoAnime encontrado -> ",res.titulo, "genero", res.genero)   
    elif opc == '6':
        nodo = input("\nIngresa el puntaje del nodoAnime a Eliminar -> ")
        nodo = float(nodo)
        arbol.eliminar(nodo)
    elif opc == '7':
        print("\nElegiste salir...\n")
        os.system("pause")
        break
    else:
        print("\nElige una opcion correcta...")
    print()
    os.system("pause")

print()