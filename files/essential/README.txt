# Zotz

Descripción:
    Se trata de un grupo de funciones desarrolladas para extraer y copiar la información relevante de un fichero pdf a un Excel.

Caracteristicas:
   * Es necesario emplear el fichero Excel proporcionado ya que ha sido modificado (lo mínimo e imprescindible) para adecuarse a las funcionalidades solicitadas y a las funciones creadas para cubrir estas últimas.
   * El nombre de los archivos deberá respetar el siguiente esquema: YY/MM/DD - Proveedor - referencia.
   Si se pretende cambiar el formato, será necesario contactar con el desarrollador.

Si se van a realizar cambios en el Excel, habrá que hacerlos siguiendo un cierto criterio:
   * Consulta con el desarrollador.
   * Si se van a cambiar los identificadores de los tipos de gasto habrá de hacerse
     respetando la posicion original (D25 el primer ID, EF25 el primer concepto) de la tabla
     si se va a cambiar la posición consulta con el desarrollador para actualizar el programa.
   * Si se van a añadir nuevos elementos de ID de gastos, se han de añadir a continuación de la 
     tabla original y sin dejar espacios.


Actualizaciones pendientes:<br/>
   * 1.1.0 Error al cerrar la version ejecutable (Hecho)
   * 1.2.0 Error Handling (Hecho)
   * 1.3.0 Actualización para facturas de Merkadona (Hecho)
   * 1.3.5 Creacion de excel segun proveedor (Hecho)
   * 1.4.0 Actualización para facturas de Lidl (Hecho)
   * 2.0.0 Actualización para lanzar varios procesos Simultaáneos
   * 2.1.0 Manejo de la BBDD
   * 2.2.0 Actualización de las referencias de una tabla