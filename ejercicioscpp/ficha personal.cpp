#include <iostream>
#include <string>
using namespace std;

int main() {
    string nombre;
    int edad;
    float estatura;
    
    cout << "=== REGISTRO PERSONAL ===" << endl;
    cout << "Ingrese su nombre: ";
    getline(cin, nombre);
    
    cout << "Ingrese su edad: ";
    cin >> edad;
    
    cout << "Ingrese su estatura (en metros): ";
    cin >> estatura;
    
    cout << "\n=== FICHA PERSONAL ===" << endl;
    cout << "Nombre: " << nombre << endl;
    cout << "Edad: " << edad << " años" << endl;
    cout << "Estatura: " << estatura << " metros" << endl;
    
    return 0;
}