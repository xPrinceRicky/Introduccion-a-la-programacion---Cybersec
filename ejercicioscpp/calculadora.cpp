#include <iostream>
using namespace std;

int main() {
    int opcion;
    float num1, num2, resultado;
    
    do {
        cout << "\nMENU CALCULADORA" << endl;
        cout << "1. Sumar" << endl;
        cout << "2. Restar" << endl;
        cout << "3. Multiplicar" << endl;
        cout << "4. Salir" << endl;
        cout << "Seleccione una opcion: ";
        cin >> opcion;
        
        if(opcion >= 1 && opcion <= 3) {
            cout << "Ingrese primer numero: ";
            cin >> num1;
            cout << "Ingrese segundo numero: ";
            cin >> num2;
        }
        
        switch(opcion) {
            case 1:
                resultado = num1 + num2;
                cout << "Resultado: " << resultado << endl;
                break;
            case 2:
                resultado = num1 - num2;
                cout << "Resultado: " << resultado << endl;
                break;
            case 3:
                resultado = num1 * num2;
                cout << "Resultado: " << resultado << endl;
                break;
            case 4:
                cout << "Saliendo del programa..." << endl;
                break;
            default:
                cout << "Opcion no valida. Intente de nuevo." << endl;
        }
        
    } while(opcion != 4);
    
    return 0;
}