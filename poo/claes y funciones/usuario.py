class Usuario:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
    
    def mostrar_datos(self):
        print(f"Nombre: {self.nombre}")
        print(f"Edad: {self.edad}")

#prueba de la clase
if __name__ == "__main__":
    usuario1 = Usuario("Rikenny Encarnacion", 25)
    usuario2 = Usuario("Kendry Encarnacion", 16)
    
    print("=== DATOS DEL USUARIO 1 ===")
    usuario1.mostrar_datos()
    
    print("\n=== DATOS DEL USUARIO 2 ===")
    usuario2.mostrar_datos()