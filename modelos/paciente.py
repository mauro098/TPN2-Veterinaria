class Paciente: 
    def __init__(self,codigo,nombre,especie,raza,edad,duenio):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__especie = especie
        self.__raza = raza
        self.edad = edad
        self.duenio = duenio

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def especie(self):
        return self.__especie

    @property
    def raza(self):
        return self.__raza

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