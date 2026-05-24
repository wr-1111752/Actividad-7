"""Repositorio JSON para persistir estudiantes."""

import json
import os
from typing import List

from app.exceptions import (
    EstudianteDuplicadoError,
    EstudianteNoEncontradoError,
)
from app.interfaces.i_repositorio_estudiante import IRepositorioEstudiante
from app.models.estudiante import Estudiante
from app.utils.constantes_negocio import RUTA_ESTUDIANTES_JSON


class EstudianteJsonRepositorio(IRepositorioEstudiante):
    """Repositorio que almacena estudiantes en un archivo JSON.

    Args:
        ruta_archivo: ruta del archivo donde se guardan los registros.
    """

    def __init__(self, ruta_archivo: str = RUTA_ESTUDIANTES_JSON) -> None:
        self._ruta = ruta_archivo
        self._inicializar_archivo()

    def _inicializar_archivo(self) -> None:
        directorio = os.path.dirname(self._ruta)
        if directorio:
            os.makedirs(directorio, exist_ok=True)
        if not os.path.exists(self._ruta):
            self._escribir_todos([])

    def _leer_todos(self) -> List[Estudiante]:
        with open(self._ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return [Estudiante.from_dict(item) for item in datos]

    def _escribir_todos(self, estudiantes: List[Estudiante]) -> None:
        with open(self._ruta, "w", encoding="utf-8") as archivo:
            json.dump(
                [estudiante.to_dict() for estudiante in estudiantes],
                archivo,
                indent=2,
                ensure_ascii=False,
            )

    def crear(self, estudiante: Estudiante) -> None:
        """Guarda un estudiante nuevo y valida codigo unico.

        Args:
            estudiante: estudiante validado a persistir.
        """
        estudiantes = self._leer_todos()
        if any(item.codigo == estudiante.codigo for item in estudiantes):
            raise EstudianteDuplicadoError(estudiante.codigo)
        estudiantes.append(estudiante)
        self._escribir_todos(estudiantes)

    def listar(self) -> List[Estudiante]:
        """Retorna todos los estudiantes.

        Returns:
            Lista de estudiantes almacenados.
        """
        return self._leer_todos()

    def buscar_por_codigo(self, codigo: str) -> Estudiante:
        """Busca un estudiante por codigo.

        Args:
            codigo: codigo institucional.

        Returns:
            Estudiante encontrado.
        """
        codigo_normalizado = codigo.strip().upper()
        for estudiante in self._leer_todos():
            if estudiante.codigo == codigo_normalizado:
                return estudiante
        raise EstudianteNoEncontradoError(codigo)

    def actualizar(self, estudiante: Estudiante) -> None:
        """Actualiza un estudiante existente.

        Args:
            estudiante: estudiante con los datos nuevos.
        """
        estudiantes = self._leer_todos()
        for indice, actual in enumerate(estudiantes):
            if actual.codigo == estudiante.codigo:
                estudiantes[indice] = estudiante
                self._escribir_todos(estudiantes)
                return
        raise EstudianteNoEncontradoError(estudiante.codigo)

    def eliminar(self, codigo: str) -> None:
        """Elimina un estudiante por codigo.

        Args:
            codigo: codigo institucional.
        """
        codigo_normalizado = codigo.strip().upper()
        estudiantes = self._leer_todos()
        filtrados = [
            estudiante
            for estudiante in estudiantes
            if estudiante.codigo != codigo_normalizado
        ]
        if len(filtrados) == len(estudiantes):
            raise EstudianteNoEncontradoError(codigo)
        self._escribir_todos(filtrados)
