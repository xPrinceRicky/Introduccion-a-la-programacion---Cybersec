class DatabaseConfig:
    HOST = "127.0.0.1"
    PORT = 3306
    USER = "root"
    PASSWORD = "Prince319*"
    DATABASE = "gestor_contrasenas"
    
    @classmethod
    def get_connection_string(cls):
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'database': cls.DATABASE
        }