class Dispositivo:
    def encender(self):
        pass

class Laptop(Dispositivo):
    def encender(self):
        return "La laptop muestra el logo y carga el sistema operativo"

class Telefono(Dispositivo):
    def encender(self):
        return "El teléfono muestra la pantalla de inicio y pide el patron de desbloqueo"

# Ejemplo de uso
if __name__ == "__main__":
    dispositivos = [
        Laptop(),
        Telefono()
    ]
    
    for dispositivo in dispositivos:
        print(dispositivo.encender())