class Estudiante:
    def __init__(self, nombre, calificaciones):
        self.nombre = nombre
        self.calificaciones = calificaciones
    
    def calcular_promedio(self):
        if not self.calificaciones:
            return 0
        return sum(self.calificaciones) / len(self.calificaciones)
    
    def mostrar_info(self):
        promedio = self.calcular_promedio()
        print(f"Estudiante: {self.nombre}")
        print(f"Calificaciones: {self.calificaciones}")
        print(f"Promedio: {promedio:.2f}")

#prueba de la clase
if __name__ == "__main__":
    estudiante1 = Estudiante("Kendry Encarnacion", [85, 90, 78, 92, 88])
    estudiante1.mostrar_info()