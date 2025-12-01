class CuentaBancaria:
    def __init__(self, titular, balance=0):
        self.titular = titular
        self.balance = balance
    
    def depositar(self, monto):
        self.balance += monto
        print(f"Se depositaro ${monto:.2f}. Balance actual: ${self.balance:.2f}")
    
    def retirar(self, monto):
        if monto <= self.balance:
            self.balance -= monto
            print(f"Se retiro ${monto:.2f}. Balance actual: ${self.balance:.2f}")
        else:
            print(f"Fondos insuficientes. Balance: ${self.balance:.2f}")
    
    def mostrar_balance(self):
        print(f"Titular: {self.titular}")
        print(f"Balance: ${self.balance:.2f}")

#prueba de la clase
if __name__ == "__main__":
    cuenta = CuentaBancaria("Rikenny Encarnacion", 50000)
    cuenta.mostrar_balance()
    
    cuenta.depositar(500)
    cuenta.retirar(200)
    cuenta.retirar(5000)