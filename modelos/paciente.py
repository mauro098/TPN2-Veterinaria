class Paciente: 
    def __init__(self,codigo,nombre,especie,raza,edad,duenio,telefono=None):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__especie = especie
        self.__raza = raza
        self.edad = edad
        self.duenio = duenio
        self.__telefono = telefono

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        if type(nuevo_nombre) is not str:
            raise ValueError("El nombre debe ser un texto")
        elif not nuevo_nombre.strip():
            raise ValueError("El nombre del paciente no puede estar vacío")
        else:
            self.__nombre = nuevo_nombre.strip()

    @property
    def especie(self):
        return self.__especie

    @especie.setter
    def especie(self, nueva_especie):
        if type(nueva_especie) is not str:
            raise ValueError("La especie debe ser un texto")
        elif not nueva_especie.strip():
            raise ValueError("La especie no puede estar vacía")
        else:
            self.__especie = nueva_especie.strip()

    @property
    def raza(self):
        return self.__raza

    @raza.setter
    def raza(self, nueva_raza):
        self.__raza = nueva_raza

    @property
    def edad(self):
        return self.__edad

    @edad.setter
    def edad(self, nueva_edad):
        if type(nueva_edad) is not int:
            raise ValueError("La edad debe ser un número entero")
        elif nueva_edad < 0:
            raise ValueError("La edad es inválida")
        else:
            self.__edad = nueva_edad

    @property
    def duenio(self):
        return self.__duenio

    @duenio.setter
    def duenio(self, nuevo_duenio):
        if type(nuevo_duenio) is not str:
            raise ValueError("El dueño debe ser un texto")
        elif not nuevo_duenio.strip():
            raise ValueError("El nombre del dueño no puede estar vacío")
        else:
            self.__duenio = nuevo_duenio.strip()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, nuevo_telefono):
        self.__telefono = nuevo_telefono

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} | {self.especie} - {self.raza} | {self.edad} años | Dueño: {self.duenio}"
