dispositivo_red = {
    'IP': '192.168.1.10',
    'Hostname': 'Firewall-Corp',
    'Estado': 'Activo'
}

# a) Mostrar el valor de 'Hostname'
print("a) Hostname:", dispositivo_red['Hostname'])

# b) Agregar la clave 'Ubicación'
dispositivo_red['Ubicación'] = 'Centro de Datos'

# c) Cambiar el valor de 'Estado' a 'Inactivo'
dispositivo_red['Estado'] = 'Inactivo'

# d) Mostrar el diccionario actualizado
print("d) Diccionario actualizado:", dispositivo_red)