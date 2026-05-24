"""Contrato abstracto para repositorios de Estudiante."""

from abc import ABC, abstractmethod
from typing import List

from app.models.estudiante import Estudiante


class IRepositorioEstudiante(ABC):
    """Define las operaciones CRUD para estudiantes."""

    @abstractmethod
    def crear(self, estudiante: Estudiante) -> None:
        """Persiste un estudiante nuevo.

        Args:
            estudiante: estudiante validado a guardar.
        """

    @abstractmethod
    def listar(self) -> List[Estudiante]:
        """Retorna todos los estudiantes almacenados.

        Returns:
            Lista de estudiantes, posiblemente vacia.
        """

    @abstractmethod
    def buscar_por_codigo(self, codigo: str) -> Estudiante:
        """Recupera un estudiante por codigo.

        Args:
            codigo: codigo institucional del estudiante.

        Returns:
            Estudiante encontrado.
        """

    @abstractmethod
    def actualizar(self, estudiante: Estudiante) -> None:
        """Reemplaza los datos de un estudiante existente.

        Args:
            estudiante: estudiante con datos actualizados.
        """

    @abstractmethod
    def eliminar(self, codigo: str) -> None:
        """Elimina un estudiante por codigo.

        Args:
            codigo: codigo institucional del estudiante.
        """
