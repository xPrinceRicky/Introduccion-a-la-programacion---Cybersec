#include <iostream>
#include <string>
#include <vector>
#include <cctype>
#include <algorithm>
using namespace std;

struct Usuario {
    string nombre;
    string contrasena;
    bool esFuerte;
};

vector<Usuario> usuarios;

void mostrarMenu();
void registrarUsuario();
bool verificarFuerzaContrasena(const string& contrasena);
void mostrarTodosUsuarios();
void buscarUsuario();
void mostrarUsuariosDebiles();
string enmascararContrasena(const string& contrasena);
void cambiarContrasena();

int main() {
    int opcion;
    
    cout << "=== GESTOR DE CONTRASENAS SEGURAS ===" << endl;
    cout << "Bienvenido al sistema de gestion de contrasenas" << endl;
    
    do {
        mostrarMenu();
        cout << "Seleccione una opcion: ";
        cin >> opcion;
        cin.ignore();
        
        switch(opcion) {
            case 1:
                registrarUsuario();
                break;
            case 2:
                mostrarTodosUsuarios();
                break;
            case 3:
                buscarUsuario();
                break;
            case 4:
                mostrarUsuariosDebiles();
                break;
            case 5:
                cambiarContrasena();
                break;
            case 6:
                cout << "\nSaliendo del sistema..." << endl;
                cout << "Gracias por usar el Gestor de Contrasenas Seguras" << endl;
                break;
            default:
                cout << "Opcion no valida. Intente de nuevo." << endl;
        }
        
        cout << endl;
        
    } while(opcion != 6);
    
    return 0;
}

void mostrarMenu() {
    cout << "\nMENU PRINCIPAL" << endl;
    cout << "1. Registrar nuevo usuario" << endl;
    cout << "2. Mostrar todos los usuarios" << endl;
    cout << "3. Buscar usuario" << endl;
    cout << "4. Mostrar usuarios con contrasenas debiles" << endl;
    cout << "5. Cambiar contrasena" << endl;
    cout << "6. Salir" << endl;
}

void registrarUsuario() {
    Usuario nuevoUsuario;
    
    cout << "\nREGISTRAR NUEVO USUARIO" << endl;
    
    cout << "Ingrese nombre de usuario: ";
    getline(cin, nuevoUsuario.nombre);
    
    for(const auto& usuario : usuarios) {
        if(usuario.nombre == nuevoUsuario.nombre) {
            cout << "Error: El usuario ya existe." << endl;
            return;
        }
    }
    
    cout << "Ingrese contrasena (minimo 8 caracteres): ";
    getline(cin, nuevoUsuario.contrasena);
    
    nuevoUsuario.esFuerte = verificarFuerzaContrasena(nuevoUsuario.contrasena);
    
    usuarios.push_back(nuevoUsuario);
    
    cout << "\nUsuario registrado exitosamente!" << endl;
    
    if(!nuevoUsuario.esFuerte) {
        cout << "\nALERTA: La contrasena es debil!" << endl;
        cout << "Recomendaciones para una contrasena fuerte:" << endl;
        cout << "- Minimo 8 caracteres" << endl;
        cout << "- Al menos una letra mayuscula" << endl;
        cout << "- Al menos una letra minuscula" << endl;
        cout << "- Al menos un numero" << endl;
        cout << "- Al menos un caracter especial (!@#$%^&*)" << endl;
    }
}

bool verificarFuerzaContrasena(const string& contrasena) {
    bool tieneMinuscula = false;
    bool tieneMayuscula = false;
    bool tieneNumero = false;
    bool tieneEspecial = false;
    bool longitudSuficiente = contrasena.length() >= 8;
    
    string especiales = "!@#$%^&*()_+-=[]{}|;:,.<>?";
    
    for(char c : contrasena) {
        if(islower(c)) {
            tieneMinuscula = true;
        } else if(isupper(c)) {
            tieneMayuscula = true;
        } else if(isdigit(c)) {
            tieneNumero = true;
        } else if(especiales.find(c) != string::npos) {
            tieneEspecial = true;
        }
    }
    
    return tieneMinuscula && tieneMayuscula && tieneNumero && tieneEspecial && longitudSuficiente;
}

void mostrarTodosUsuarios() {
    if(usuarios.empty()) {
        cout << "\nNo hay usuarios registrados." << endl;
        return;
    }
    
    cout << "\nLISTA DE USUARIOS" << endl;
    cout << "Total de usuarios: " << usuarios.size() << endl << endl;
    
    for(int i = 0; i < usuarios.size(); i++) {
        cout << "Usuario #" << i+1 << ":" << endl;
        cout << "  Nombre: " << usuarios[i].nombre << endl;
        cout << "  Contrasena: " << enmascararContrasena(usuarios[i].contrasena) << endl;
        cout << "  Fortaleza: " << (usuarios[i].esFuerte ? "FUERTE" : "DEBIL ") << endl;
        cout << "--------------------------------" << endl;
    }
}

void buscarUsuario() {
    if(usuarios.empty()) {
        cout << "\nNo hay usuarios registrados." << endl;
        return;
    }
    
    string nombreBuscar;
    cout << "\n=== BUSCAR USUARIO ===" << endl;
    cout << "Ingrese el nombre de usuario a buscar: ";
    getline(cin, nombreBuscar);
    
    bool encontrado = false;
    
    for(const auto& usuario : usuarios) {
        if(usuario.nombre == nombreBuscar) {
            cout << "\nUsuario encontrado:" << endl;
            cout << "  Nombre: " << usuario.nombre << endl;
            cout << "  Contrasena: " << enmascararContrasena(usuario.contrasena) << endl;
            cout << "  Fortaleza: " << (usuario.esFuerte ? "FUERTE" : "DEBIL️") << endl;
            encontrado = true;
            break;
        }
    }
    
    if(!encontrado) {
        cout << "Usuario no encontrado." << endl;
    }
}

void mostrarUsuariosDebiles() {
    cout << "\n=== USUARIOS CON CONTRASENAS DEBILES ===" << endl;
    
    int contador = 0;
    
    for(const auto& usuario : usuarios) {
        if(!usuario.esFuerte) {
            cout << "\nUsuario: " << usuario.nombre << endl;
            cout << "Contrasena: " << enmascararContrasena(usuario.contrasena) << endl;
            contador++;
        }
    }
    
    if(contador == 0) {
        cout << "¡Excelente! No hay usuarios con contrasenas debiles." << endl;
    } else {
        cout << "\nTotal de usuarios con contrasenas debiles: " << contador << endl;
        cout << "Se recomienda cambiar estas contrasenas por seguridad." << endl;
    }
}

string enmascararContrasena(const string& contrasena) {
    if(contrasena.length() <= 2) {
        return string(contrasena.length(), '*');
    }
    
    string enmascarada = contrasena.substr(0, 1);
    enmascarada += string(contrasena.length() - 2, '*');
    enmascarada += contrasena.substr(contrasena.length() - 1, 1);
    
    return enmascarada;
}

void cambiarContrasena() {
    if(usuarios.empty()) {
        cout << "\nNo hay usuarios registrados." << endl;
        return;
    }
    
    string nombreUsuario, nuevaContrasena;
    cout << "\n=== CAMBIAR CONTRASENA ===" << endl;
    cout << "Ingrese el nombre de usuario: ";
    getline(cin, nombreUsuario);
    
    for(auto& usuario : usuarios) {
        if(usuario.nombre == nombreUsuario) {
            cout << "Ingrese la nueva contrasena: ";
            getline(cin, nuevaContrasena);
            
            bool esFuerte = verificarFuerzaContrasena(nuevaContrasena);
            
            usuario.contrasena = nuevaContrasena;
            usuario.esFuerte = esFuerte;
            
            cout << "\nContrasena cambiada exitosamente!" << endl;
            
            if(!esFuerte) {
                cout << "Alerta: La nueva contrasena es debil." << endl;
            }
            
            return;
        }
    }
    
    cout << "Usuario no encontrado." << endl;
}