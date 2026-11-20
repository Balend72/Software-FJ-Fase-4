"""Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ.
Curso Programación 213023A_2204 | UNAD | Python 3 | Sin base de datos.
"""
from abc import ABC, abstractmethod
import logging
import re

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger("SoftwareFJ")


class SoftwareFJError(Exception):
    """Excepción base de la aplicación."""


class ValidationError(SoftwareFJError):
    """Dato inválido."""


class ServiceUnavailableError(SoftwareFJError):
    """Servicio no disponible."""


class ReservationStateError(SoftwareFJError):
    """Operación incompatible con el estado de una reserva."""


class Entity(ABC):
    def __init__(self, entity_id):
        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValidationError("El identificador es obligatorio.")
        self._id = entity_id.strip()

    @property
    def id(self):
        return self._id

    @abstractmethod
    def describe(self):
        """Describe la entidad."""


class Client(Entity):
    def __init__(self, client_id, name, email, phone):
        super().__init__(client_id)
        self.name = name
        self.email = email
        self.phone = phone

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value.strip()) < 2:
            raise ValidationError("El nombre debe tener al menos dos caracteres.")
        self._name = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", value.strip()
        ):
            raise ValidationError("El correo electrónico no es válido.")
        self._email = value.strip().lower()

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        digits = re.sub(r"\D", "", str(value))
        if not 7 <= len(digits) <= 15:
            raise ValidationError("El teléfono debe contener entre 7 y 15 dígitos.")
        self._phone = digits

    def describe(self):
        return f"Cliente {self.id}: {self.name} ({self.email})"


class Service(Entity, ABC):
    def __init__(self, service_id, name, hourly_rate, available=True):
        super().__init__(service_id)
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("El nombre del servicio es obligatorio.")
        if (
            isinstance(hourly_rate, bool)
            or not isinstance(hourly_rate, (int, float))
            or hourly_rate <= 0
        ):
            raise ValidationError("La tarifa debe ser un número positivo.")
        if not isinstance(available, bool):
            raise ValidationError("La disponibilidad debe ser booleana.")
        self.name = name.strip()
        self.hourly_rate = float(hourly_rate)
        self.available = available

    @abstractmethod
    def validate_parameters(self, **kwargs):
        """Valida parámetros particulares del servicio."""

    @abstractmethod
    def describe(self):
        """Describe el servicio."""

    def calculate_cost(self, hours, tax_rate=0.0, discount=0.0):
        if (
            isinstance(hours, bool)
            or not isinstance(hours, (int, float))
            or hours <= 0
        ):
            raise ValidationError("La duración debe ser mayor que cero.")
        if not isinstance(tax_rate, (int, float)) or not 0 <= tax_rate <= 1:
            raise ValidationError("El impuesto debe estar entre 0 y 1.")
        if not isinstance(discount, (int, float)) or not 0 <= discount <= 1:
            raise ValidationError("El descuento debe estar entre 0 y 1.")
        subtotal = self.hourly_rate * hours
        return round(subtotal * (1 - discount) * (1 + tax_rate), 2)


class RoomReservation(Service):
    def __init__(self, service_id, hourly_rate, capacity, available=True):
        super().__init__(service_id, "Reserva de salas", hourly_rate, available)
        self.capacity = capacity
        self.validate_parameters()

    def validate_parameters(self, attendees=None, **kwargs):
        if (
            isinstance(self.capacity, bool)
            or not isinstance(self.capacity, int)
            or self.capacity <= 0
        ):
            raise ValidationError("La capacidad debe ser un entero positivo.")
        if attendees is not None and (
            not isinstance(attendees, int) or not 1 <= attendees <= self.capacity
        ):
            raise ValidationError("La cantidad de asistentes supera la capacidad.")

    def describe(self):
        return (
            f"{self.name}: capacidad {self.capacity}, "
            f"tarifa/hora ${self.hourly_rate:,.2f}"
        )


class EquipmentRental(Service):
    def __init__(self, service_id, hourly_rate, equipment_type, available=True):
        super().__init__(service_id, "Alquiler de equipos", hourly_rate, available)
        if not isinstance(equipment_type, str) or not equipment_type.strip():
            raise ValidationError("Debe especificarse el tipo de equipo.")
        self.equipment_type = equipment_type.strip()

    def validate_parameters(self, quantity=1, **kwargs):
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValidationError("La cantidad debe ser un entero positivo.")

    def calculate_cost(self, hours, tax_rate=0.0, discount=0.0, quantity=1):
        self.validate_parameters(quantity=quantity)
        return round(
            super().calculate_cost(hours, tax_rate, discount) * quantity, 2
        )

    def describe(self):
        return (
            f"{self.name}: {self.equipment_type}, "
            f"tarifa/hora ${self.hourly_rate:,.2f}"
        )


class SpecializedConsulting(Service):
    def __init__(self, service_id, hourly_rate, specialty, available=True):
        super().__init__(
            service_id, "Asesorías especializadas", hourly_rate, available
        )
        if not isinstance(specialty, str) or not specialty.strip():
            raise ValidationError("Debe especificarse el área de asesoría.")
        self.specialty = specialty.strip()

    def validate_parameters(self, topic=None, **kwargs):
        if topic is not None and (
            not isinstance(topic, str) or not topic.strip()
        ):
            raise ValidationError("El tema de la asesoría no puede estar vacío.")

    def describe(self):
        return (
            f"{self.name}: {self.specialty}, "
            f"tarifa/hora ${self.hourly_rate:,.2f}"
        )


class Reservation(Entity):
    def __init__(self, reservation_id, client, service, duration):
        super().__init__(reservation_id)
        if not isinstance(client, Client):
            raise ValidationError("La reserva requiere un cliente válido.")
        if not isinstance(service, Service):
            raise ValidationError("La reserva requiere un servicio válido.")
        if (
            isinstance(duration, bool)
            or not isinstance(duration, (int, float))
            or duration <= 0
        ):
            raise ValidationError("La duración debe ser mayor que cero.")
        self.client = client
        self.service = service
        self.duration = float(duration)
        self.status = "PENDIENTE"

    def confirm(self):
        if self.status != "PENDIENTE":
            raise ReservationStateError("Solo se confirman reservas pendientes.")
        if not self.service.available:
            raise ServiceUnavailableError("El servicio no está disponible.")
        self.status = "CONFIRMADA"
        logger.info("Reserva %s confirmada.", self.id)

    def cancel(self):
        if self.status not in ("PENDIENTE", "CONFIRMADA"):
            raise ReservationStateError("No se puede cancelar en este estado.")
        self.status = "CANCELADA"
        logger.info("Reserva %s cancelada.", self.id)

    def process(self):
        try:
            if self.status != "CONFIRMADA":
                raise ReservationStateError(
                    "La reserva debe estar confirmada antes de procesarse."
                )
            total = self.service.calculate_cost(self.duration)
        except SoftwareFJError as exc:
            logger.exception("Error al procesar la reserva %s.", self.id)
            raise RuntimeError(
                f"No fue posible procesar la reserva {self.id}."
            ) from exc
        else:
            self.status = "PROCESADA"
            logger.info("Reserva %s procesada por %.2f.", self.id, total)
            return total
        finally:
            logger.info("Finalizó el intento de procesamiento %s.", self.id)

    def describe(self):
        return (
            f"Reserva {self.id}: {self.client.name} - "
            f"{self.service.name} - {self.status}"
        )


class SoftwareFJ:
    """Administra las listas de clientes, servicios y reservas en memoria."""

    def __init__(self):
        self.clients = []
        self.services = []
        self.reservations = []

    @staticmethod
    def _ensure_unique(items, item_id):
        if any(item.id == item_id for item in items):
            raise ValidationError(f"Identificador duplicado: {item_id}")

    def add_client(self, client):
        if not isinstance(client, Client):
            raise ValidationError("El objeto debe ser un cliente.")
        self._ensure_unique(self.clients, client.id)
        self.clients.append(client)
        logger.info("Cliente registrado: %s.", client.id)

    def add_service(self, service):
        if not isinstance(service, Service):
            raise ValidationError("El objeto debe ser un servicio.")
        self._ensure_unique(self.services, service.id)
        self.services.append(service)
        logger.info("Servicio registrado: %s.", service.id)

    def create_reservation(self, reservation_id, client_id, service_id, duration):
        client = next((item for item in self.clients if item.id == client_id), None)
        service = next((item for item in self.services if item.id == service_id), None)
        if client is None:
            raise ValidationError(f"No existe el cliente {client_id}.")
        if service is None:
            raise ValidationError(f"No existe el servicio {service_id}.")
        self._ensure_unique(self.reservations, reservation_id)
        reservation = Reservation(reservation_id, client, service, duration)
        self.reservations.append(reservation)
        logger.info("Reserva creada: %s.", reservation_id)
        return reservation


def run_demo():
    """Ejecuta catorce escenarios y continúa después de errores controlados."""
    app = SoftwareFJ()

    def execute(number, description, operation):
        try:
            result = operation()
        except Exception as exc:
            logger.exception("Prueba %s: %s", number, description)
            print(f"{number:02}. {description}: ERROR CONTROLADO ({exc})")
        else:
            print(
                f"{number:02}. {description}: "
                f"{result if result is not None else 'Correcto'}"
            )

    print("=== SISTEMA SOFTWARE FJ: DEMOSTRACIÓN ===")
    execute(
        1, "Registro de cliente válido",
        lambda: app.add_client(
            Client("C001", "Ana Pérez", "ana@example.com", "3001234567")
        ),
    )
    execute(
        2, "Rechazo de correo inválido",
        lambda: Client("C002", "Luis Díaz", "correo-invalido", "3101234567"),
    )
    execute(
        3, "Registro de segundo cliente",
        lambda: app.add_client(
            Client("C003", "Carlos Ruiz", "carlos@example.com", "3119876543")
        ),
    )
    execute(
        4, "Creación de servicio de sala",
        lambda: app.add_service(RoomReservation("S001", 50000, 20)),
    )
    execute(
        5, "Creación de alquiler de equipo",
        lambda: app.add_service(EquipmentRental("S002", 25000, "Proyector")),
    )
    execute(
        6, "Creación de asesoría especializada",
        lambda: app.add_service(
            SpecializedConsulting("S003", 80000, "Desarrollo de software")
        ),
    )
    execute(7, "Rechazo de tarifa negativa", lambda: RoomReservation("S004", -100, 10))

    def valid_reservation():
        reservation = app.create_reservation("R001", "C001", "S001", 2)
        reservation.confirm()
        return f"{reservation.status}; total ${reservation.process():,.2f}"

    execute(8, "Reserva confirmada y procesada", valid_reservation)
    execute(
        9, "Rechazo de duración cero",
        lambda: app.create_reservation("R002", "C001", "S001", 0),
    )
    execute(
        10, "Rechazo de cliente inexistente",
        lambda: app.create_reservation("R003", "C999", "S001", 1),
    )
    execute(
        11, "Procesamiento sin confirmar (excepción encadenada)",
        lambda: app.create_reservation("R004", "C003", "S002", 1).process(),
    )

    def cancel_reservation():
        reservation = app.create_reservation("R005", "C003", "S003", 1)
        reservation.cancel()
        return reservation.status

    execute(12, "Cancelación de reserva", cancel_reservation)

    def unavailable_service():
        app.add_service(
            EquipmentRental("S005", 15000, "Computador", available=False)
        )
        reservation = app.create_reservation("R006", "C001", "S005", 1)
        reservation.confirm()

    execute(13, "Rechazo de servicio no disponible", unavailable_service)
    execute(
        14, "Costo con impuesto y descuento",
        lambda: f"$ {app.services[0].calculate_cost(2, 0.19, 0.10):,.2f}",
    )
    print(
        f"\\nResumen: {len(app.clients)} clientes, "
        f"{len(app.services)} servicios, {len(app.reservations)} reservas."
    )
    print("Los eventos y errores se registran en software_fj.log.")


if __name__ == "__main__":
    run_demo()
