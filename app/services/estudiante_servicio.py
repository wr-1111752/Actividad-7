"""Servicio de negocio para gestionar estudiantes."""

from datetime import datetime
from typing import List

from app.interfaces.i_repositorio_estudiante import IRepositorioEstudiante
from app.models.estudiante import Estudiante


class EstudianteServicio:
    """Orquesta las operaciones del CRUD de estudiantes.

    Args:
        repositorio: implementacion del contrato IRepositorioEstudiante.
    """

    def __init__(self, repositorio: IRepositorioEstudiante) -> None:
        self._repo = repositorio

    def registrar_estudiante(
        self,
        codigo: str,
        nombre_completo: str,
        edad: int,
        semestre: int,
        correo: str,
        programa: str,
    ) -> Estudiante:
        """Crea y persiste un nuevo estudiante.

        Args:
            codigo: codigo institucional unico.
            nombre_completo: nombres y apellidos.
            edad: edad del estudiante.
            semestre: semestre academico.
            correo: correo valido.
            programa: programa academico.

        Returns:
            Estudiante creado y persistido.
        """
        estudiante = Estudiante(
            codigo=codigo,
            nombre_completo=nombre_completo,
            edad=edad,
            semestre=semestre,
            correo=correo,
            programa=programa,
            fecha_registro=datetime.now(),
        )
        self._repo.crear(estudiante)
        return estudiante

    def listar_estudiantes(self) -> List[Estudiante]:
        """Lista estudiantes ordenados por nombre.

        Returns:
            Lista de estudiantes registrados.
        """
        return sorted(
            self._repo.listar(),
            key=lambda estudiante: estudiante.nombre_completo.lower(),
        )

    def buscar_estudiante(self, codigo: str) -> Estudiante:
        """Busca un estudiante por codigo.

        Args:
            codigo: codigo institucional.

        Returns:
            Estudiante encontrado.
        """
        return self._repo.buscar_por_codigo(codigo)

    def actualizar_estudiante(
        self,
        codigo: str,
        nombre_completo: str,
        edad: int,
        semestre: int,
        correo: str,
        programa: str,
    ) -> Estudiante:
        """Actualiza los datos editables de un estudiante.

        Args:
            codigo: codigo institucional existente.
            nombre_completo: nuevo nombre completo.
            edad: nueva edad.
            semestre: nuevo semestre.
            correo: nuevo correo.
            programa: nuevo programa academico.

        Returns:
            Estudiante actualizado.
        """
        actual = self._repo.buscar_por_codigo(codigo)
        actualizado = Estudiante(
            codigo=actual.codigo,
            nombre_completo=nombre_completo,
            edad=edad,
            semestre=semestre,
            correo=correo,
            programa=programa,
            fecha_registro=actual.fecha_registro,
        )
        self._repo.actualizar(actualizado)
        return actualizado

    def eliminar_estudiante(self, codigo: str) -> None:
        """Elimina un estudiante por codigo.

        Args:
            codigo: codigo institucional.
        """
        self._repo.eliminar(codigo)
