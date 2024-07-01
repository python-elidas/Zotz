# Zotz

## Descripción

    Se trata de un grupo de funciones desarrolladas para extraer y copiar la información relevante de un fichero pdf a un Excel siendo dicha informacion la siguiente:

* Número de factura
* Fecha de la compra
* Listado de articulos con la siguiente infromación:
  * Nombre del articulo
  * Cantidad
  * Precio unitario
  * Precio total
  * Iva
* Total de la factura

## Requisitos técnicos

* Es necesario emplear el fichero Excel proporcionado ya que ha sido modificado (lo mínimo e imprescindible) para adecuarse a las funcionalidades solicitadas y a las funciones creadas para cubrir estas últimas.
* El nombre de los archivos deberá respetar el siguiente esquema: YY/MM/DD - Proveedor - referencia.
  Si se pretende cambiar el formato, será necesario contactar con el desarrollador.
* Desde la versión 1.3.5 No se necesita especificar el fichero Excel a emplear. En su lugar será necesario especificar, cuando el programa lo solicite o lo permita, la carpeta en la que se guardará el excel.

## Procedimiento ante cambios en Excel:

1. Consulta con el desarrollador.
1. Si se van a cambiar los identificadores de los tipos de gasto habrá de hacerse
   respetando la posicion original (D25 el primer ID, EF25 el primer concepto) de la tabla
   si se va a cambiar la posición consulta con el desarrollador para actualizar el programa.
1. Si se van a añadir nuevos elementos de ID de gastos, se han de añadir a continuación de la
   tabla original y sin dejar espacios.

## Actualizaciones pendientes:

### Version 1.x.x

* **1.1.x** Error al cerrar la version ejecutable (Hecho)
* **1.2.x** Error Handling (hecho para lectura)
* **1.3.xa** Actualización para facturas de Merkadona (Hecho)
* **1.3.xb** Creaccion de archivos excel automatica (Hecho)
* **1.4.x** Actualización para facturas de Lidl (hecho)

### Versión 2.x.x

* **2.0.xa** Cambio de paquete de lectura de PDF
* **2.0.xb** Encriptado de BBDD
* **2.1.x** Actualización para lanzar varios procesos simultaneos
* **2.2.x** Manejo de la BBDD
* **2.3.x** Actualización de las referencias de una tabla
