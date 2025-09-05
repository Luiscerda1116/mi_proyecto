# 📚 Sistema de Inventario de Librería

Un sistema completo de gestión de inventario para librerías desarrollado en Python con SQLite.

![Python](https://img.shields.io/badge/Python-3.13.7-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-green.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)

## ✨ Características

- 📝 **Añadir nuevos libros** al inventario
- 🗑️ **Eliminar libros** del inventario
- 📊 **Actualizar cantidades** en stock
- 💰 **Actualizar precios** de productos
- 🔍 **Buscar libros** por título, autor o ID
- 📋 **Mostrar inventario completo**
- 📚 **Filtrar por género**
- 📈 **Ver estadísticas** detalladas del inventario
- 🎨 **Interfaz de línea de comandos** amigable con emojis

## 🚀 Instalación y Uso

### Requisitos previos
- Python 3.7 o superior
- SQLite3 (incluido con Python)

### Instalación local
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/inventario-libreria.git
cd inventario-libreria

# Ejecutar el programa
python inventario_libreria.py
```

### 🌐 Demo en línea
[Ver demo en Render](https://tu-app.render.com)

## 📖 Guía de Uso

El programa presenta un menú interactivo:

```
📚 SISTEMA DE INVENTARIO - LIBRERÍA
==================================================
1. 📝 Añadir nuevo libro
2. 🗑️  Eliminar libro
3. 📊 Actualizar cantidad
4. 💰 Actualizar precio
5. 🔍 Buscar libros
6. 📋 Mostrar inventario completo
7. 📚 Mostrar por género
8. 📈 Ver estadísticas
9. ❌ Salir
```

### Ejemplo de uso:
1. **Añadir un libro:**
   - ID: `1`
   - Título: `Cien años de soledad`
   - Autor: `Gabriel García Márquez`
   - Cantidad: `10`
   - Precio: `25.50`
   - Género: `Ficción`

## 🗄️ Base de Datos

El sistema utiliza SQLite con la siguiente estructura:

```sql
CREATE TABLE libros (
    id INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    genero TEXT
);
```

## 📊 Funcionalidades

- ✅ **CRUD completo** (Create, Read, Update, Delete)
- ✅ **Validación de datos** de entrada
- ✅ **Manejo de errores** robusto
- ✅ **Interfaz intuitiva** con emojis
- ✅ **Estadísticas en tiempo real**
- ✅ **Búsqueda avanzada**
- ✅ **Categorización por género**

## 🛠️ Tecnologías Utilizadas

- **Python 3.13.7** - Lenguaje de programación
- **SQLite3** - Base de datos
- **OS/System** - Interfaz de línea de comandos

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

Desarrollado con ❤️ por [Tu Nombre]

---

⭐ **¡Si te gusta este proyecto, dale una estrella!** ⭐