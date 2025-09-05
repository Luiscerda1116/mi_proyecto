import sqlite3
import os
from typing import Dict, List, Optional, Tuple

class Producto:
    """
    Clase que representa un libro en la librería
    Utiliza encapsulamiento para proteger los datos
    """
    
    def __init__(self, id_producto: int, nombre: str, autor: str, cantidad: int, precio: float, genero: str = "General"):
        """
        Constructor de la clase Producto (Libro)
        
        Args:
            id_producto (int): ID único del libro
            nombre (str): Título del libro
            autor (str): Autor del libro
            cantidad (int): Cantidad en stock
            precio (float): Precio del libro
            genero (str): Género literario
        """
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__autor = autor
        self.__cantidad = cantidad
        self.__precio = precio
        self.__genero = genero
    
    # Métodos getter (acceso a atributos privados)
    @property
    def id_producto(self) -> int:
        return self.__id_producto
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @property
    def autor(self) -> str:
        return self.__autor
    
    @property
    def cantidad(self) -> int:
        return self.__cantidad
    
    @property
    def precio(self) -> float:
        return self.__precio
    
    @property
    def genero(self) -> str:
        return self.__genero
    
    # Métodos setter (modificación controlada de atributos)
    @nombre.setter
    def nombre(self, valor: str):
        if valor.strip():
            self.__nombre = valor.strip()
        else:
            raise ValueError("El nombre no puede estar vacío")
    
    @autor.setter
    def autor(self, valor: str):
        if valor.strip():
            self.__autor = valor.strip()
        else:
            raise ValueError("El autor no puede estar vacío")
    
    @cantidad.setter
    def cantidad(self, valor: int):
        if valor >= 0:
            self.__cantidad = valor
        else:
            raise ValueError("La cantidad no puede ser negativa")
    
    @precio.setter
    def precio(self, valor: float):
        if valor > 0:
            self.__precio = valor
        else:
            raise ValueError("El precio debe ser mayor a 0")
    
    @genero.setter
    def genero(self, valor: str):
        if valor.strip():
            self.__genero = valor.strip()
        else:
            raise ValueError("El género no puede estar vacío")
    
    def __str__(self) -> str:
        """Representación en cadena del producto"""
        return f"ID: {self.__id_producto} | '{self.__nombre}' por {self.__autor} | Stock: {self.__cantidad} | Precio: ${self.__precio:.2f} | Género: {self.__genero}"
    
    def __repr__(self) -> str:
        """Representación técnica del objeto"""
        return f"Producto({self.__id_producto}, '{self.__nombre}', '{self.__autor}', {self.__cantidad}, {self.__precio}, '{self.__genero}')"
    
    def to_dict(self) -> Dict:
        """Convierte el producto a diccionario para facilitar operaciones"""
        return {
            'id_producto': self.__id_producto,
            'nombre': self.__nombre,
            'autor': self.__autor,
            'cantidad': self.__cantidad,
            'precio': self.__precio,
            'genero': self.__genero
        }


class BaseDatos:
    """
    Clase para manejar todas las operaciones de base de datos
    Implementa el patrón Singleton para una sola conexión
    """
    
    def __init__(self, nombre_bd: str = "libreria_inventario.db"):
        """
        Inicializa la conexión a la base de datos
        
        Args:
            nombre_bd (str): Nombre del archivo de base de datos
        """
        self.nombre_bd = nombre_bd
        self.crear_tabla()
    
    def crear_tabla(self):
        """Crea la tabla productos si no existe"""
        try:
            with sqlite3.connect(self.nombre_bd) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS productos (
                        id_producto INTEGER PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        autor TEXT NOT NULL,
                        cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
                        precio REAL NOT NULL CHECK(precio > 0),
                        genero TEXT NOT NULL
                    )
                ''')
                conn.commit()
                print("✅ Base de datos inicializada correctamente")
        except sqlite3.Error as e:
            print(f"❌ Error al crear la tabla: {e}")
    
    def insertar_producto(self, producto: Producto) -> bool:
        """Inserta un producto en la base de datos"""
        try:
            with sqlite3.connect(self.nombre_bd) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO productos (id_producto, nombre, autor, cantidad, precio, genero)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (producto.id_producto, producto.nombre, producto.autor, 
                     producto.cantidad, producto.precio, producto.genero))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            print(f"❌ Error: Ya existe un producto con ID {producto.id_producto}")
            return False
        except sqlite3.Error as e:
            print(f"❌ Error al insertar producto: {e}")
            return False
    
    def obtener_todos_productos(self) -> List[Tuple]:
        """Obtiene todos los productos de la base de datos"""
        try:
            with sqlite3.connect(self.nombre_bd) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM productos ORDER BY id_producto')
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"❌ Error al obtener productos: {e}")
            return []
    
    def obtener_producto_por_id(self, id_producto: int) -> Optional[Tuple]:
        """Obtiene un producto específico por su ID"""
        try:
            with sqlite3.connect(self.nombre_bd) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM productos WHERE id_producto = ?', (id_producto,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"❌ Error al obtener producto: {e}")
            return None
    
    def actualizar_producto(self, id_producto: int, **kwargs) -> bool:
        """Actualiza campos específicos de un producto"""
        try:
            # Construir la consulta dinámicamente
            campos = []
            valores = []
            for campo, valor in kwargs.items():
                if campo in ['nombre', 'autor', 'cantidad', 'precio', 'genero']:
                    campos.append(f"{campo} = ?")
                    valores.append(valor)
            
            if not campos:
                return False
            
            valores.append(id_producto)
            consulta = f"UPDATE productos SET {', '.join(campos)} WHERE id_producto = ?"
            
            with sqlite3.connect(self.nombre_bd) as conn:
                cursor = conn.cursor()
                cursor.execute(consulta, valores)
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"❌ Error al actualizar producto: {e}")
            return False
    
    def eliminar_producto(self, id_producto: int) -> bool:
        """Elimina un producto de la base de datos"""
        try:
            with sqlite3.connect(self.nombre_bd) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM productos WHERE id_producto = ?', (id_producto,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"❌ Error al eliminar producto: {e}")
            return False
    
    def buscar_productos(self, termino: str) -> List[Tuple]:
        """Busca productos por nombre o autor"""
        try:
            with sqlite3.connect(self.nombre_bd) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM productos 
                    WHERE nombre LIKE ? OR autor LIKE ?
                    ORDER BY nombre
                ''', (f'%{termino}%', f'%{termino}%'))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"❌ Error al buscar productos: {e}")
            return []


class Inventario:
    """
    Clase principal para gestionar el inventario de la librería
    Utiliza múltiples colecciones para optimizar diferentes operaciones
    """
    
    def __init__(self):
        """Inicializa el inventario con diferentes estructuras de datos"""
        # Diccionario principal: ID -> Producto (búsqueda O(1))
        self.__productos: Dict[int, Producto] = {}
        
        # Set para IDs únicos (verificación rápida de existencia)
        self.__ids_existentes: set = set()
        
        # Diccionario para búsqueda por género (organización)
        self.__productos_por_genero: Dict[str, List[int]] = {}
        
        # Lista para mantener orden de inserción
        self.__orden_insercion: List[int] = []
        
        # Instancia de base de datos
        self.__bd = BaseDatos()
        
        # Cargar datos existentes
        self.cargar_desde_bd()
    
    def cargar_desde_bd(self):
        """Carga todos los productos desde la base de datos al iniciar"""
        productos_bd = self.__bd.obtener_todos_productos()
        print(f"📚 Cargando {len(productos_bd)} productos desde la base de datos...")
        
        for producto_data in productos_bd:
            id_prod, nombre, autor, cantidad, precio, genero = producto_data
            producto = Producto(id_prod, nombre, autor, cantidad, precio, genero)
            
            # Añadir a todas las colecciones
            self.__productos[id_prod] = producto
            self.__ids_existentes.add(id_prod)
            self.__orden_insercion.append(id_prod)
            
            # Actualizar índice por género
            if genero not in self.__productos_por_genero:
                self.__productos_por_genero[genero] = []
            self.__productos_por_genero[genero].append(id_prod)
    
    def añadir_producto(self, id_producto: int, nombre: str, autor: str, 
                       cantidad: int, precio: float, genero: str = "General") -> bool:
        """
        Añade un nuevo producto al inventario
        
        Returns:
            bool: True si se añadió correctamente, False si ya existe
        """
        # Verificación rápida con set O(1)
        if id_producto in self.__ids_existentes:
            print(f"❌ Error: Ya existe un producto con ID {id_producto}")
            return False
        
        try:
            # Crear objeto producto
            nuevo_producto = Producto(id_producto, nombre, autor, cantidad, precio, genero)
            
            # Guardar en base de datos primero
            if self.__bd.insertar_producto(nuevo_producto):
                # Añadir a todas las colecciones
                self.__productos[id_producto] = nuevo_producto
                self.__ids_existentes.add(id_producto)
                self.__orden_insercion.append(id_producto)
                
                # Actualizar índice por género
                if genero not in self.__productos_por_genero:
                    self.__productos_por_genero[genero] = []
                self.__productos_por_genero[genero].append(id_producto)
                
                print(f"✅ Producto '{nombre}' añadido exitosamente")
                return True
            else:
                return False
                
        except ValueError as e:
            print(f"❌ Error de validación: {e}")
            return False
    
    def eliminar_producto(self, id_producto: int) -> bool:
        """Elimina un producto del inventario"""
        if id_producto not in self.__ids_existentes:
            print(f"❌ No existe un producto con ID {id_producto}")
            return False
        
        # Eliminar de base de datos
        if self.__bd.eliminar_producto(id_producto):
            # Obtener datos antes de eliminar
            producto = self.__productos[id_producto]
            genero = producto.genero
            
            # Eliminar de todas las colecciones
            del self.__productos[id_producto]
            self.__ids_existentes.remove(id_producto)
            self.__orden_insercion.remove(id_producto)
            
            # Actualizar índice por género
            if genero in self.__productos_por_genero:
                self.__productos_por_genero[genero].remove(id_producto)
                if not self.__productos_por_genero[genero]:
                    del self.__productos_por_genero[genero]
            
            print(f"✅ Producto '{producto.nombre}' eliminado exitosamente")
            return True
        return False
    
    def actualizar_cantidad(self, id_producto: int, nueva_cantidad: int) -> bool:
        """Actualiza la cantidad de un producto"""
        if id_producto not in self.__ids_existentes:
            print(f"❌ No existe un producto con ID {id_producto}")
            return False
        
        try:
            if nueva_cantidad < 0:
                raise ValueError("La cantidad no puede ser negativa")
            
            # Actualizar en base de datos
            if self.__bd.actualizar_producto(id_producto, cantidad=nueva_cantidad):
                # Actualizar en memoria
                self.__productos[id_producto].cantidad = nueva_cantidad
                print(f"✅ Cantidad actualizada a {nueva_cantidad}")
                return True
            return False
            
        except ValueError as e:
            print(f"❌ Error: {e}")
            return False
    
    def actualizar_precio(self, id_producto: int, nuevo_precio: float) -> bool:
        """Actualiza el precio de un producto"""
        if id_producto not in self.__ids_existentes:
            print(f"❌ No existe un producto con ID {id_producto}")
            return False
        
        try:
            if nuevo_precio <= 0:
                raise ValueError("El precio debe ser mayor a 0")
            
            # Actualizar en base de datos
            if self.__bd.actualizar_producto(id_producto, precio=nuevo_precio):
                # Actualizar en memoria
                self.__productos[id_producto].precio = nuevo_precio
                print(f"✅ Precio actualizado a ${nuevo_precio:.2f}")
                return True
            return False
            
        except ValueError as e:
            print(f"❌ Error: {e}")
            return False
    
    def buscar_por_nombre(self, termino: str) -> List[Producto]:
        """
        Busca productos por nombre o autor
        Utiliza la base de datos para búsqueda eficiente
        """
        productos_encontrados = self.__bd.buscar_productos(termino)
        resultado = []
        
        for producto_data in productos_encontrados:
            id_prod = producto_data[0]
            if id_prod in self.__productos:
                resultado.append(self.__productos[id_prod])
        
        return resultado
    
    def obtener_producto_por_id(self, id_producto: int) -> Optional[Producto]:
        """Obtiene un producto específico por ID"""
        return self.__productos.get(id_producto)
    
    def mostrar_todos_productos(self):
        """Muestra todos los productos ordenados por ID"""
        if not self.__productos:
            print("📚 El inventario está vacío")
            return
        
        print("\n" + "="*80)
        print("📚 INVENTARIO COMPLETO DE LA LIBRERÍA")
        print("="*80)
        
        # Mostrar estadísticas generales
        total_libros = sum(p.cantidad for p in self.__productos.values())
        valor_total = sum(p.cantidad * p.precio for p in self.__productos.values())
        
        print(f"📊 Resumen: {len(self.__productos)} títulos diferentes | {total_libros} libros en stock | Valor total: ${valor_total:.2f}")
        print("-"*80)
        
        # Mostrar productos ordenados por ID
        for id_producto in sorted(self.__productos.keys()):
            producto = self.__productos[id_producto]
            print(f"  {producto}")
        
        print("="*80)
    
    def mostrar_por_genero(self):
        """Muestra productos organizados por género"""
        if not self.__productos_por_genero:
            print("📚 No hay productos en el inventario")
            return
        
        print("\n" + "="*60)
        print("📚 INVENTARIO POR GÉNERO LITERARIO")
        print("="*60)
        
        for genero in sorted(self.__productos_por_genero.keys()):
            ids_productos = self.__productos_por_genero[genero]
            print(f"\n📖 {genero.upper()} ({len(ids_productos)} títulos):")
            print("-" * 40)
            
            for id_producto in sorted(ids_productos):
                producto = self.__productos[id_producto]
                print(f"  • {producto.nombre} - {producto.autor} (Stock: {producto.cantidad})")
    
    def obtener_estadisticas(self) -> Dict:
        """Obtiene estadísticas del inventario"""
        if not self.__productos:
            return {}
        
        total_titulos = len(self.__productos)
        total_libros = sum(p.cantidad for p in self.__productos.values())
        valor_total = sum(p.cantidad * p.precio for p in self.__productos.values())
        precio_promedio = sum(p.precio for p in self.__productos.values()) / total_titulos
        
        # Género más popular (más títulos)
        genero_mas_titulos = max(self.__productos_por_genero.keys(), 
                                key=lambda g: len(self.__productos_por_genero[g]))
        
        # Producto más caro y más barato
        precios = [(p.precio, p.nombre) for p in self.__productos.values()]
        precio_max, libro_mas_caro = max(precios)
        precio_min, libro_mas_barato = min(precios)
        
        return {
            'total_titulos': total_titulos,
            'total_libros': total_libros,
            'valor_total': valor_total,
            'precio_promedio': precio_promedio,
            'genero_mas_titulos': genero_mas_titulos,
            'libro_mas_caro': (libro_mas_caro, precio_max),
            'libro_mas_barato': (libro_mas_barato, precio_min)
        }


class InterfazUsuario:
    """
    Clase para manejar la interfaz de usuario de consola
    """
    
    def __init__(self):
        self.inventario = Inventario()
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        print("\n" + "="*50)
        print("📚 SISTEMA DE INVENTARIO - LIBRERÍA")
        print("="*50)
        print("1. 📝 Añadir nuevo libro")
        print("2. 🗑️  Eliminar libro")
        print("3. 📊 Actualizar cantidad")
        print("4. 💰 Actualizar precio")
        print("5. 🔍 Buscar libros")
        print("6. 📋 Mostrar inventario completo")
        print("7. 📚 Mostrar por género")
        print("8. 📈 Ver estadísticas")
        print("9. ❌ Salir")
        print("-"*50)
    
    def obtener_opcion(self) -> str:
        """Obtiene la opción del usuario con validación"""
        while True:
            try:
                opcion = input("Selecciona una opción (1-9): ").strip()
                if opcion in [str(i) for i in range(1, 10)]:
                    return opcion
                else:
                    print("❌ Por favor, ingresa un número del 1 al 9")
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                exit()
    
    def añadir_libro(self):
        """Interfaz para añadir un nuevo libro"""
        print("\n📝 AÑADIR NUEVO LIBRO")
        print("-" * 30)
        
        try:
            id_producto = int(input("ID del libro: "))
            nombre = input("Título del libro: ").strip()
            autor = input("Autor: ").strip()
            cantidad = int(input("Cantidad en stock: "))
            precio = float(input("Precio: $"))
            genero = input("Género (opcional): ").strip() or "General"
            
            self.inventario.añadir_producto(id_producto, nombre, autor, cantidad, precio, genero)
            
        except ValueError as e:
            print(f"❌ Error: Por favor ingresa valores válidos - {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def eliminar_libro(self):
        """Interfaz para eliminar un libro"""
        print("\n🗑️ ELIMINAR LIBRO")
        print("-" * 20)
        
        try:
            id_producto = int(input("ID del libro a eliminar: "))
            
            # Mostrar información del libro antes de eliminar
            producto = self.inventario.obtener_producto_por_id(id_producto)
            if producto:
                print(f"\n📖 Libro a eliminar: {producto}")
                confirmar = input("¿Estás seguro? (s/N): ").strip().lower()
                if confirmar == 's':
                    self.inventario.eliminar_producto(id_producto)
                else:
                    print("❌ Operación cancelada")
            
        except ValueError:
            print("❌ Error: Por favor ingresa un ID válido")
    
    def actualizar_cantidad(self):
        """Interfaz para actualizar cantidad"""
        print("\n📊 ACTUALIZAR CANTIDAD")
        print("-" * 25)
        
        try:
            id_producto = int(input("ID del libro: "))
            
            # Mostrar información actual
            producto = self.inventario.obtener_producto_por_id(id_producto)
            if producto:
                print(f"📖 Libro: {producto.nombre} (Stock actual: {producto.cantidad})")
                nueva_cantidad = int(input("Nueva cantidad: "))
                self.inventario.actualizar_cantidad(id_producto, nueva_cantidad)
            
        except ValueError:
            print("❌ Error: Por favor ingresa valores numéricos válidos")
    
    def actualizar_precio(self):
        """Interfaz para actualizar precio"""
        print("\n💰 ACTUALIZAR PRECIO")
        print("-" * 22)
        
        try:
            id_producto = int(input("ID del libro: "))
            
            # Mostrar información actual
            producto = self.inventario.obtener_producto_por_id(id_producto)
            if producto:
                print(f"📖 Libro: {producto.nombre} (Precio actual: ${producto.precio:.2f})")
                nuevo_precio = float(input("Nuevo precio: $"))
                self.inventario.actualizar_precio(id_producto, nuevo_precio)
            
        except ValueError:
            print("❌ Error: Por favor ingresa un precio válido")
    
    def buscar_libros(self):
        """Interfaz para buscar libros"""
        print("\n🔍 BUSCAR LIBROS")
        print("-" * 18)
        
        termino = input("Ingresa título o autor a buscar: ").strip()
        if not termino:
            print("❌ Por favor ingresa un término de búsqueda")
            return
        
        resultados = self.inventario.buscar_por_nombre(termino)
        
        if resultados:
            print(f"\n📚 Se encontraron {len(resultados)} resultados:")
            print("-" * 40)
            for producto in resultados:
                print(f"  📖 {producto}")
        else:
            print(f"❌ No se encontraron libros con '{termino}'")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas del inventario"""
        stats = self.inventario.obtener_estadisticas()
        
        if not stats:
            print("📚 No hay datos para mostrar estadísticas")
            return
        
        print("\n" + "="*60)
        print("📈 ESTADÍSTICAS DEL INVENTARIO")
        print("="*60)
        print(f"📚 Total de títulos diferentes: {stats['total_titulos']}")
        print(f"📖 Total de libros en stock: {stats['total_libros']}")
        print(f"💰 Valor total del inventario: ${stats['valor_total']:.2f}")
        print(f"📊 Precio promedio por libro: ${stats['precio_promedio']:.2f}")
        print(f"🏆 Género con más títulos: {stats['genero_mas_titulos']}")
        print(f"💎 Libro más caro: {stats['libro_mas_caro'][0]} (${stats['libro_mas_caro'][1]:.2f})")
        print(f"💵 Libro más barato: {stats['libro_mas_barato'][0]} (${stats['libro_mas_barato'][1]:.2f})")
        print("="*60)
    
    def ejecutar(self):
        """Ejecuta el programa principal"""
        print("🎉 ¡Bienvenido al Sistema de Inventario de la Librería!")
        
        while True:
            try:
                self.mostrar_menu()
                opcion = self.obtener_opcion()
                
                if opcion == '1':
                    self.añadir_libro()
                elif opcion == '2':
                    self.eliminar_libro()
                elif opcion == '3':
                    self.actualizar_cantidad()
                elif opcion == '4':
                    self.actualizar_precio()
                elif opcion == '5':
                    self.buscar_libros()
                elif opcion == '6':
                    self.inventario.mostrar_todos_productos()
                elif opcion == '7':
                    self.inventario.mostrar_por_genero()
                elif opcion == '8':
                    self.mostrar_estadisticas()
                elif opcion == '9':
                    print("\n👋 ¡Gracias por usar el Sistema de Inventario!")
                    print("📚 ¡Que tengas un excelente día!")
                    break
                
                # Pausa para leer la salida
                input("\nPresiona Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                input("Presiona Enter para continuar...")


def main():
    """
    Función principal del programa
    """
    try:
        # Crear directorio para la base de datos si no existe
        os.makedirs(os.path.dirname(os.path.abspath("libreria_inventario.db")), exist_ok=True)
        
        # Inicializar y ejecutar la aplicación
        app = InterfazUsuario()
        app.ejecutar()
        
    except Exception as e:
        print(f"❌ Error crítico al iniciar la aplicación: {e}")
        input("Presiona Enter para salir...")


# Datos de ejemplo para pruebas
def cargar_datos_ejemplo():
    """
    Función auxiliar para cargar datos de ejemplo
    (Ejecutar solo una vez para pruebas)
    """
    bd = BaseDatos()
    
    libros_ejemplo = [
        (1, "Cien años de soledad", "Gabriel García Márquez", 15, 45.50, "Ficción"),
        (2, "Don Quijote de la Mancha", "Miguel de Cervantes", 8, 38.00, "Clásico"),
        (3, "1984", "George Orwell", 12, 32.75, "Distopía"),
        (4, "El principito", "Antoine de Saint-Exupéry", 20, 25.90, "Infantil"),
        (5, "Sapiens", "Yuval Noah Harari", 6, 52.00, "Historia"),
        (6, "La sombra del viento", "Carlos Ruiz Zafón", 10, 41.25, "Misterio"),
        (7, "El código Da Vinci", "Dan Brown", 7, 39.99, "Suspenso"),
        (8, "Orgullo y prejuicio", "Jane Austen", 9, 35.50, "Romance"),
    ]
    
    print("📚 Cargando libros de ejemplo...")
    for libro_data in libros_ejemplo:
        producto = Producto(*libro_data)
        bd.insertar_producto(producto)
    
    print("✅ Datos de ejemplo cargados correctamente")


if __name__ == "__main__":
    # Para cargar datos de ejemplo (ejecutar solo una vez):
    # cargar_datos_ejemplo()
    
    # Ejecutar el programa principal
    main()