
class NodoBST:
    def __init__(self, clave, paciente):
        self.clave = clave
        self.paciente = paciente
        self.izquierda = None
        self.derecha = None


class ArbolBST:
    def __init__(self):
        self.raiz = None

    def insertar(self, clave, paciente):
        nuevo = NodoBST(clave, paciente)

        # Si el arbol está vacío, el nuevo nodo es la raíz
        if self.raiz is None:
            self.raiz = nuevo
            return
        
        # Si no está vacío, se recorre el arbol para insertar el nodo
        actual = self.raiz
        while True:
            if clave < actual.clave:
                if actual.izquierda is None:
                    actual.izquierda = nuevo
                    return
                else:
                    actual = actual.izquierda
            else:
                if actual.derecha is None:
                    actual.derecha = nuevo
                    return
                else:
                    actual = actual.derecha
    
    def buscar(self, clave):
        contador = 0
        actual = self.raiz

        while actual is not None:
            contador += 1
            if clave == actual.clave:
                return (actual.paciente, contador)
            elif clave < actual.clave:
                actual = actual.izquierda
            else:
                actual = actual.derecha
        
        return (None, contador)
    
    def recorrido_inorden(self):
        lista_ordenada = []
        self._inorden(self.raiz, lista_ordenada)
        return lista_ordenada
    
    def _inorden(self, nodo, lista_ordenada):
        if nodo is not None:
            self._inorden(nodo.izquierda, lista_ordenada)
            lista_ordenada.append(nodo.paciente)
            self._inorden(nodo.derecha, lista_ordenada)
