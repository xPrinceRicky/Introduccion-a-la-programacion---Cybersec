class Vehiculo:
    def mover(self):
        pass

class Carro(Vehiculo):
    def mover(self):
        return "El carro avanza por la avenida"

class Bicicleta(Vehiculo):
    def mover(self):
        return "La bicicleta avanza por la ciclovia"

#prueba
if __name__ == "__main__":
    vehiculos = [
        Carro(),
        Bicicleta()
    ]
    
    for vehiculo in vehiculos:
        print(vehiculo.mover())