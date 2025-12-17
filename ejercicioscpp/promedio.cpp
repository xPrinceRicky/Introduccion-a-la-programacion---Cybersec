#include <iostream>
#include <string>
using namespace std;

struct Estudiante {
    string nombre;
    int edad;
    float promedio;
};

int main() {
    Estudiante estudiantes[3];
    
    cout << "=== REGISTRO DE ESTUDIANTES ===" << endl;
    
    for(int i = 0; i < 3; i++) {
        cout << "\nEstudiante " << i+1 << ":" << endl;
        cout << "Nombre: ";
        cin.ignore();
        getline(cin, estudiantes[i].nombre);
        cout << "Edad: ";
        cin >> estudiantes[i].edad;
        cout << "Promedio: ";
        cin >> estudiantes[i].promedio;
    }
    
    float mejorPromedio = estudiantes[0].promedio;
    int indiceMejor = 0;
    
    for(int i = 1; i < 3; i++) {
        if(estudiantes[i].promedio > mejorPromedio) {
            mejorPromedio = estudiantes[i].promedio;
            indiceMejor = i;
        }
    }
    
    cout << "\n=== MEJOR ESTUDIANTE ===" << endl;
    cout << "Nombre: " << estudiantes[indiceMejor].nombre << endl;
    cout << "Edad: " << estudiantes[indiceMejor].edad << endl;
    cout << "Promedio: " << estudiantes[indiceMejor].promedio << endl;
    
    return 0;
}