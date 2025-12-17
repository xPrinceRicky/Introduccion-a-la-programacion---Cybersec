#include <iostream>
#include <string>
#include <iomanip>
using namespace std;

struct Producto {
    string nombre;
    float precio;
    int cantidad;
};

int main() {
    Producto productos[5];
    float valorTotal = 0;
    
    cout << "INVENTARIO DE PRODUCTOS" << endl;
    
    for(int i = 0; i < 5; i++) {
        cout << "\nProducto " << i+1 << ":" << endl;
        cout << "Nombre: ";
        cin.ignore();
        getline(cin, productos[i].nombre);
        cout << "Precio: $";
        cin >> productos[i].precio;
        cout << "Cantidad: ";
        cin >> productos[i].cantidad;
        
        valorTotal += productos[i].precio * productos[i].cantidad;
    }
    
    cout << fixed << setprecision(2);
    cout << "\nVALOR TOTAL DEL INVENTARIO" << endl;
    cout << "Valor total: $" << valorTotal << endl;

    cout << "\nDETALLE PRODUCTOS" << endl;
    for(int i = 0; i < 5; i++) {
        float valorProducto = productos[i].precio * productos[i].cantidad;
        cout << productos[i].nombre << ": $" << valorProducto << endl;
    }
    
    return 0;
}