#include <iostream>
using namespace std;

int main() {
    float base, altura, area;
    
    cout << "=== CALCULO AREA RECTANGULO ===" << endl;
    cout << "Ingrese la base: ";
    cin >> base;
    
    cout << "Ingrese la altura: ";
    cin >> altura;
    
    area = base * altura;
    
    cout << "El area del rectangulo es: " << area << endl;
    
    return 0;
}