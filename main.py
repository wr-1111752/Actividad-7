"""Punto de entrada de la aplicacion."""

from app.repositories.estudiante_json_repositorio import (
    EstudianteJsonRepositorio,
)
from app.services.estudiante_servicio import EstudianteServicio
from app.ui.menu_principal import MenuPrincipal


def main() -> None:
    """Instancia dependencias y arranca la interfaz de consola."""
    repositorio = EstudianteJsonRepositorio()
    servicio = EstudianteServicio(repositorio)
    menu = MenuPrincipal(servicio)
    menu.ejecutar()


if __name__ == "__main__":
    main()
