class Figura:
    def area(self):
        pass

class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio
    
    def area(self):
        return 3.1416 * self.radio ** 2

class Cuadrado(Figura):
    def __init__(self, lado):
        self.lado = lado
    
    def area(self):
        return self.lado ** 2

class Triangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
    
    def area(self):
        return (self.base * self.altura) / 2

#prueba
if __name__ == "__main__":
    figuras = [
        Circulo(5),
        Cuadrado(4),
        Triangulo(6, 3)
    ]
    
    for figura in figuras:
        print(f"Área: {figura.area():.2f}")