import logging
import time
import datetime
from typing import Optional, List
from Backend.services.interfaces import IProductoService

logger = logging.getLogger(__name__)


class ValidacionDecorator(IProductoService):
    def __init__(self, servicio: IProductoService):
        self._servicio = servicio

    def obtener_todos(self, orden: str = None, filtro: str = None) -> List:
        return self._servicio.obtener_todos(orden, filtro)

    def obtener_por_id(self, id: int) -> Optional[object]:
        if id <= 0:
            raise ValueError("El ID debe ser un entero positivo")
        return self._servicio.obtener_por_id(id)

    def crear_producto(self, datos: dict) -> object:
        if not datos.get("nombre", "").strip():
            raise ValueError("El nombre no puede estar vacío")
        if datos.get("precio", -1) <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return self._servicio.crear_producto(datos)

    def actualizar_producto(self, id: int, datos: dict) -> Optional[object]:
        if not datos.get("nombre", "").strip():
            raise ValueError("El nombre no puede estar vacío")
        if datos.get("precio", -1) <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return self._servicio.actualizar_producto(id, datos)

    def eliminar_producto(self, id: int) -> Optional[object]:
        if id <= 0:
            raise ValueError("El ID debe ser un entero positivo")
        return self._servicio.eliminar_producto(id)


class LoggingDecorator(IProductoService):


    def __init__(self, servicio: IProductoService):
        self._servicio = servicio

    def _ejecutar(self, operacion: str, fn, **meta):
        inicio = time.time()
        try:
            resultado = fn()
            ms = (time.time() - inicio) * 1000
            logger.info(f"[LOG] {operacion} | OK | {ms:.1f}ms | {meta}")
            return resultado
        except Exception as e:
            ms = (time.time() - inicio) * 1000
            logger.error(f"[LOG] {operacion} | ERROR={e} | {ms:.1f}ms | {meta}")
            raise

    def obtener_todos(self, orden: str = None, filtro: str = None) -> List:
        return self._ejecutar("obtener_todos", orden=orden, filtro=filtro,
                              fn=lambda: self._servicio.obtener_todos(orden, filtro))

    def obtener_por_id(self, id: int) -> Optional[object]:
        return self._ejecutar("obtener_por_id", id=id,
                              fn=lambda: self._servicio.obtener_por_id(id))

    def crear_producto(self, datos: dict) -> object:
        return self._ejecutar("crear_producto", nombre=datos.get("nombre"),
                              fn=lambda: self._servicio.crear_producto(datos))

    def actualizar_producto(self, id: int, datos: dict) -> Optional[object]:
        return self._ejecutar("actualizar_producto", id=id,
                              fn=lambda: self._servicio.actualizar_producto(id, datos))

    def eliminar_producto(self, id: int) -> Optional[object]:
        return self._ejecutar("eliminar_producto", id=id,
                              fn=lambda: self._servicio.eliminar_producto(id))


class AuditoriaDecorator(IProductoService):

    def __init__(self, servicio: IProductoService):
        self._servicio = servicio

    def _auditar(self, operacion: str, detalle: str):
        ts = datetime.datetime.utcnow().isoformat()
        logger.info(f"[AUDITORÍA] {ts} | op={operacion} | {detalle}")

    def obtener_todos(self, orden: str = None, filtro: str = None) -> List:
        return self._servicio.obtener_todos(orden, filtro)

    def obtener_por_id(self, id: int) -> Optional[object]:
        return self._servicio.obtener_por_id(id)

    def crear_producto(self, datos: dict) -> object:
        resultado = self._servicio.crear_producto(datos)
        self._auditar("CREAR", f"nombre='{datos.get('nombre')}' precio={datos.get('precio')}")
        return resultado

    def actualizar_producto(self, id: int, datos: dict) -> Optional[object]:
        resultado = self._servicio.actualizar_producto(id, datos)
        if resultado:
            self._auditar("ACTUALIZAR", f"id={id} nombre='{datos.get('nombre')}'")
        return resultado

    def eliminar_producto(self, id: int) -> Optional[object]:
        resultado = self._servicio.eliminar_producto(id)
        if resultado:
            self._auditar("ELIMINAR", f"id={id}")
        return resultado
