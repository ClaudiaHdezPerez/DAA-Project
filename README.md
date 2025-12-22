# DAA-Project

## Problem Description:

#### El Comerciante Holandés

La prestigiosa Compañía Holandesa de las Indias Orientales, en su afán por dominar el comercio mundial, se enfrenta a un desafío monumental. Un capitán experimentado, al mando de una de sus valiosas flotas, debe emprender una expedición comercial que partirá de Ámsterdam y, tras recorrer los puertos más lucrativos del Viejo y Nuevo Continente, deberá regresar a su puerto de origen.

Los inversores de la Compañía han proporcionado un capital inicial considerable y han establecido un plazo máximo para la duración de la expedición. El capitán tiene la libertad de elegir qué puertos visitar y en qué orden, con la única condición de no visitar el mismo puerto dos veces en el mismo viaje (por cuestiones de acuerdos comerciales y evitar saturación del mercado).

En cada puerto, el capitán encontrará una lista de mercancías disponibles, con sus respectivos precios de compra y venta (que pueden variar significativamente). El capitán puede vender las mercancías que lleva a bordo y comprar nuevas. Sin embargo, debe ser astuto:

- La capacidad de carga de su barco es limitada, por lo que no puede llevar más de lo que su bodega permite.
- No es necesario vender todas las mercancías al llegar a un puerto; el capitán puede decidir retener parte de su cargamento si cree que podrá venderlo a un precio más alto en un puerto posterior.
- Debe asegurarse de que, después de cada operación de compra, le quede suficiente dinero para cubrir los salarios de la tripulación, los impuestos portuarios y las posibles reparaciones del barco hasta el siguiente destino.
- El tiempo es oro; la duración total del viaje, incluyendo el tiempo de navegación entre puertos, no debe exceder el plazo fijado por los inversores.

El objetivo del capitán es claro: planificar la ruta y las transacciones en cada puerto de tal manera que, al regresar a Amsterdam, el capital final de la expedición sea el máximo posible, superando con creces la inversión inicial.


## Ejecución de los algoritmos
1. Ir al directorio `src/solutions`:
   ```bash
   cd src/solutions
   ```
Nota: En el archivo main.py, descomentar la línea del algoritmo que se desea ejecutar.
Por defecto, está activa la solución por fuerza bruta.
Si se quiere probar otro algoritmo, basta con descomentar su línea correspondiente y comentar las demás.

2. Ejecutar el comando:
    ```bash
    python main.py
    ```

## Ejecución del tester
1. Ir al directorio `src`:
    ```bash
    cd src
    ```

2. Generar los casos de prueba con el siguiente comando:
    ```bash
    python -m tester.generator
    ```

3. Ejecutar los algoritmos sobre los casos de prueba generados:
    ```bash
    python -m tester.validator
    ```