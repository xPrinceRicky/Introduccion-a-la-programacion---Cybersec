class Rectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
    
    def calcular_area(self):
        return self.base * self.altura
    
    def mostrar_area(self):
        area = self.calcular_area()
        print(f"El área del rectángulo con base {self.base} y altura {self.altura} es: {area}")

#prueba de la clase
if __name__ == "__main__":
    rectangulo1 = Rectangulo(5, 3)
    rectangulo1.mostrar_area()