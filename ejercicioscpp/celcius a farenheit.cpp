#include <iostream>
using namespace std;

int main() {
    float celsius, fahrenheit;
    
    cout << "=== CONVERSOR CELSIUS A FAHRENHEIT ===" << endl;
    cout << "Ingrese temperatura en grados Celsius: ";
    cin >> celsius;
    
    fahrenheit = (celsius * 9/5) + 32;
    
    cout << celsius << "°C equivalen a " << fahrenheit << "°F" << endl;
    
    return 0;
}