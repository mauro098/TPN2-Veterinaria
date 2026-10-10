from modelos.paciente import Paciente  

class GestorPacientes:
    def __init__(self):
        self.lista_pacientes = []
        self.cargar_datos_prueba() 

    def cargar_datos_prueba(self):
        p1 = Paciente("P001", "Firulais", "Perro", "Caniche", 3, "Carlos")
        p2 = Paciente("P002", "Michi", "Gato", "Siamés", 2, "Ana")
        p3 = Paciente("P003", "Roco", "Perro", "Boxer", 5, "Marcela")
        p4 = Paciente("P004", "Luna", "Gato", "Persa", 4, "Lucas")
        p5 = Paciente("P005", "Piolín", "Ave", "Canario", 1, "Sofía")
        p6 = Paciente("P006", "Boby", "Perro", "Golden Retriever", 6, "Jorge")
        p7 = Paciente("P007", "Simba", "Gato", "Común Europeo", 3, "Valeria")
        p8 = Paciente("P008", "Thor", "Perro", "Ovejero Alemán", 4, "Martín")
        p9 = Paciente("P009", "Lola", "Perro", "Beagle", 2, "Camila")
        p10 = Paciente("P010", "Manchas", "Gato", "Angora", 5, "Esteban")
        p11 = Paciente("P011", "Kira", "Perro", "Pitbull", 3, "Florencia")
        p12 = Paciente("P012", "Nala", "Gato", "Siamés", 1, "Gonzalo")
        p13 = Paciente("P013", "Coco", "Ave", "Loro", 7, "Agustina")
        p14 = Paciente("P014", "Zeus", "Perro", "Doberman", 4, "Federico")
        p15 = Paciente("P015", "Nina", "Gato", "Maine Coon", 2, "Lucía")
        p16 = Paciente("P016", "Bruno", "Perro", "Bulldog Francés", 3, "Diego")
        p17 = Paciente("P017", "Cleo", "Gato", "Sphynx", 4, "Mariana")
        p18 = Paciente("P018", "Toby", "Perro", "Labrador", 5, "Pablo")
        p19 = Paciente("P019", "Pelusa", "Gato", "Común", 6, "Carla")
        p20 = Paciente("P020", "Rocky", "Perro", "Pitbull", 2, "Hernán")
        p21 = Paciente("P021", "Princesa", "Perro", "Caniche", 8, "Romina")
        p22 = Paciente("P022", "Tom", "Gato", "Común", 3, "Julián")
        p23 = Paciente("P023", "Baco", "Perro", "San Bernardo", 5, "Natalia")
        p24 = Paciente("P024", "Mora", "Perro", "Cocker", 4, "Facundo")
        p25 = Paciente("P025", "Pancho", "Ave", "Cacatúa", 2, "Victoria")
        p26 = Paciente("P026", "Gordo", "Gato", "Persa", 6, "Ezequiel")
        p27 = Paciente("P027", "Sultán", "Perro", "Mastín", 7, "Yamila")
        p28 = Paciente("P028", "Milka", "Gato", "Angora", 1, "Leandro")
        p29 = Paciente("P029", "Tyson", "Perro", "Boxer", 4, "Sabrina")
        p30 = Paciente("P030", "Duque", "Perro", "vejero Belga", 5, "Emiliano")

        lista_temporal = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, 
                          p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, 
                          p21, p22, p23, p24, p25, p26, p27, p28, p29, p30]
        
        for p in lista_temporal:
            self.lista_pacientes.append(p)

    def insertar_paciente(self, codigo, nombre, especie, raza, edad, duenio):
        """Agrega un nuevo paciente a la lista."""
        nuevo = Paciente(codigo, nombre, especie, raza, edad, duenio)
        self.lista_pacientes.append(nuevo)
        print(f"¡Paciente {nombre} agregado con éxito!")

    def modificar_paciente(self, codigo, nueva_edad, nuevo_duenio):
        """Busca un paciente por código y modifica sus datos."""
        for paciente in self.lista_pacientes:
            if paciente.codigo == codigo:
                paciente.edad = nueva_edad
                paciente.duenio = nuevo_duenio
                print("¡Datos actualizados correctamente!")
                return True
        print("No se encontró un paciente con ese código.")
        return False

    def eliminar_paciente(self, codigo):
        """Elimina un paciente de la lista usando su código."""
        for paciente in self.lista_pacientes:
            if paciente.codigo == codigo:
                self.lista_pacientes.remove(paciente)
                print("¡Paciente eliminado de la lista!")
                return True
  print("No se encontró un paciente con ese código.")
        return False

              
        print("No se encontró un paciente con ese código.")
