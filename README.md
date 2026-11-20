# Software FJ — Fase 4

**Universidad Nacional Abierta y a Distancia (UNAD)**  
**Programa:** Ingeniería de Sistemas  
**Curso:** Programación (213023A_2204)  
**Estudiante:** Luna Balentina Durán Morales  
**Tutor:** Jorge Eduardo Ospina

## Descripción
Aplicación de consola en Python para administrar clientes, servicios y reservas de Software FJ. Aplica programación orientada a objetos y manejo robusto de excepciones. No utiliza bases de datos: los datos operativos permanecen en listas y objetos durante la ejecución. Los eventos y errores se registran en `software_fj.log`.

## Requisitos
- Python 3.10 o superior.
- No requiere paquetes externos.

## Ejecución
Desde la carpeta del proyecto, ejecute:

```bash
python main.py
```

El programa ejecuta catorce escenarios válidos e inválidos. Los errores esperados se controlan y la demostración continúa.

## Funcionalidades implementadas
- Abstracción mediante `Entity` y `Service`.
- Encapsulación y validación de datos de clientes.
- Herencia y polimorfismo para salas, equipos y asesorías.
- Cálculo de costos con parámetros opcionales de impuestos y descuentos.
- Reservas con confirmación, cancelación y procesamiento.
- Excepciones personalizadas, bloques `try/except/else/finally` y encadenamiento.
- Registro de eventos y errores con `logging`.

## Estructura
- `main.py`: implementación y demostración.
- `README.md`: documentación.
- `.gitignore`: exclusión de archivos temporales.

## Evidencias
Ejecute el programa en su equipo y tome capturas auténticas de la consola y del archivo `software_fj.log`. Este repositorio no contiene capturas simuladas.

## Referencias
Cuevas Álvarez, A. (2016). *Python 3: curso práctico* (pp. 373–385). RA-MA Editorial.

Romano, F., Baka, B., & Phillips, D. (2019). *Getting started with Python: Understand key data structures and use Python in object-oriented programming*. Packt Publishing.

Van Rossum, G., & Drake, F. L. (2024). *El tutorial de Python*. Python Software Foundation. https://docs.python.org/es/3.12/tutorial/errors.html

Zambrano, J. P. (2025). *Introducción al uso de GitHub* [Objeto Virtual de Información]. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/75876

Silva, F. D. (2025). *Basics of using GitHub* [Objeto Virtual de Información]. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/75882
