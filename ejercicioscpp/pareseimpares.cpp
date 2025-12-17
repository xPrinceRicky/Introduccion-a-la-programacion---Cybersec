#include <iostream>
using namespace std;

int main() {
    int numero, pares = 0, impares = 0;
    
    cout << "=== CONTADOR DE PARES E IMPARES ===" << endl;
    cout << "Ingrese 10 numeros:" << endl;
    
    for(int i = 1; i <= 10; i++) {
        cout << "Numero " << i << ": ";
        cin >> numero;
        
        if(numero % 2 == 0) {
            pares++;
        } else {
            impares++;
        }
    }
    
    cout << "\n=== RESULTADOS ===" << endl;
    cout << "Numeros pares: " << pares << endl;
    cout << "Numeros impares: " << impares << endl;
    
    return 0;
}