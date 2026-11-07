
class CatVet:

    def __init__(self, nombre: str):
       
        self.nombre = nombre
        self.subcats = []   
        self.elementos = []       


    def agrega_subcat(self, nombre_sub: str) -> "CatVet":

        nuevo = CatVet(nombre_sub)
        self.subcat.append(nuevo)
        return nuevo

    def es_hoja(self) -> bool:
        
        return len(self.subcat) == 0


    def mostrar(self, nivel: int = 0):

        prefijo = "    " * nivel
        marcador = "📄" if self.es_hoja() else "📁"
        cantidad = len(self.elementos)
        print(f"{prefijo}{marcador} {self.nombre}")

        for sub in self.subcats:
            sub.mostrar(nivel + 1)

    def buscar_categoria(self, nombre_buscado: str) -> "CatVet | None":
       
        if self.nombre.lower() == nombre_buscado.lower():
            return self

        for sub in self.subcats:
            resultado = sub.buscar_categoria(nombre_buscado)
            if resultado is not None:
                return resultado

        return None

    def contar_elementos(self) -> int:

        total = len(self.elementos)
        for sub in self.subcats:
            total += sub.contar_elementos()
        return total

    def altura(self) -> int:

        if self.es_hoja():
            return 0
        return 1 + max(sub.altura() for sub in self.subcats)

    def listar_todos(self) -> list:

        todos = list(self.elementos)  # copia de los propios
        for sub in self.subcats:
            todos.extend(sub.listar_todos())
        return todos


def construir_arbol_categorias() -> CatVet:

    raiz = CatVet("Veterinaria")

  
    perro = raiz.agregar_subcat("Perros")
    perro.agregar_subcat("Raza chica")
    perro.agregar_subcat("Raza mediana")
    perro.agregar_subcat("Raza grande")

    gato = raiz.agregar_subcat("Gatos")
    gato.agregar_subcat("Pelaje corto")
    gato.agregar_subcat("Pelaje medio")
    gato.agregar_subcat("Pelaje largo")

    conejo = raiz.agregar_subcat("Conejos")
    conejo.agregar_subcat("Raza chica")
    conejo.agregar_subcat("Raza mediana")
    conejo.agregar_subcat("Raza grande")

    return raiz


def agregar_animales(raiz: CatVet, listado: list):

    for paciente in listado:
        nodo = raiz.buscar_categoria(paciente.categoria)
        if nodo is not None:
            nodo.elementos.append(libro)
        else:
            raiz.elementos.append(paciente)
