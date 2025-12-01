class Coche:
    def __init__(self, marca, velocidad=0):
        self.marca = marca
        self.velocidad = velocidad
    
    def aumentar_velocidad(self, incremento):
        self.velocidad += incremento
        print(f"Velocidad aumentada en {incremento} km/h. Velocidad actual: {self.velocidad} km/h")
    
    def mostrar_info(self):
        print(f"Coche: {self.marca}, Velocidad: {self.velocidad} km/h")

#prueba de la clase
if __name__ == "__main__":
    mi_coche = Coche("Hyundai Sante Fe")
    mi_coche.mostrar_info()
    
    mi_coche.aumentar_velocidad(20)
    mi_coche.aumentar_velocidad(15)
    mi_coche.mostrar_info()