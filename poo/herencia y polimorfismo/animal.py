class Animal:
    def __init__(self, nombre):
        self.nombre = nombre
    
    def hablar(self):
        return "El animal hace un sonido"
    
    def describir(self):
        return f"Soy un animal llamado {self.nombre}"

class Perro(Animal):
    def hablar(self):
        return "JAU JAU"
    
    def describir(self):
        return f"Soy un perro llamado {self.nombre}"

class Gato(Animal):
    def hablar(self):
        return "MIAU MIAU"
    
    def describir(self):
        return f"Soy un gato llamado {self.nombre}"

#prueba
if __name__ == "__main__":
    animales = [
        Perro("Toby"),
        Gato("Loki")
    ]
    
    for animal in animales:
        print(f"{animal.describir()} -> {animal.hablar()}")