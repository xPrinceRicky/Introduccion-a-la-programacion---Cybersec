#include <iostream>
using namespace std;

int main() {
    int numero;
    
    cout << "=== TABLA DE MULTIPLICAR ===" << endl;
    cout << "Ingrese un numero: ";
    cin >> numero;
    
    cout << "\nTabla del " << numero << ":" << endl;
    for(int i = 1; i <= 12; i++) {
        cout << numero << " x " << i << " = " << numero * i << endl;
    }
    
    return 0;
}