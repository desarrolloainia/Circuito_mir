from dataclasses import dataclass


@dataclass
class Empresa:
    nombre: str
    telefono: str
    correo_electronico: str
    cod_cliente: str
    persona_contacto: str

def validar_invariantes(self) -> None:
    if not self.nombre:
        raise ValueError("El nombre de la empresa no puede estar vacío.")
    if not self.telefono:
        raise ValueError("El teléfono de la empresa no puede estar vacío.")
    if not self.correo_electronico:
        raise ValueError("El correo electrónico de la empresa no puede estar vacío.")
    if not self.cod_cliente:
        raise ValueError("El código de cliente de la empresa no puede estar vacío.")
    if not self.persona_contacto:
        raise ValueError("La persona de contacto de la empresa no puede estar vacía.")
