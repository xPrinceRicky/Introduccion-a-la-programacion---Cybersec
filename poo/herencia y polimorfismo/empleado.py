class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario
    
    def calcular_bono(self):
        return 0
    
    def mostrar_informacion(self):
        bono = self.calcular_bono()
        salario_total = self.salario + bono
        return f"{self.nombre} - Salario: ${self.salario:,.2f} - Bono: ${bono:,.2f} - Total: ${salario_total:,.2f}"

class Gerente(Empleado):
    def calcular_bono(self):
        #Los gerentes reciben 30% de bono
        return self.salario * 0.30

class Tecnico(Empleado):
    def calcular_bono(self):
        #Los técnicos reciben 15% de bono
        return self.salario * 0.15

class Vendedor(Empleado):
    def calcular_bono(self):
        #Los vendedores reciben 20% de bono
        return self.salario * 0.20

#prueba
if __name__ == "__main__":
    print("SISTEMA DE NOMINA")
    
    empleados = [
        Gerente("María González", 50000),
        Tecnico("Carlos Ruiz", 30000),
        Vendedor("Ana Torres", 25000),
        Gerente("Roberto Díaz", 60000),
        Tecnico("Laura Mendoza", 32000)
    ]
    
    for empleado in empleados:
        print(empleado.mostrar_informacion())