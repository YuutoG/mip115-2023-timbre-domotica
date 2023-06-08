from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gpiozero import Servo, LED
from gpiozero.pins.pigpio import PiGPIOFactory

# Esta instancia evita las intermitencias de servo
factory = PiGPIOFactory()
origin = [
    "*"
]

# este objeto es el encargado de levantar el servicio web
# es una Rest API.
app = FastAPI()

# esta configuración es para evitar problemas
# para consumir la API desde la interfaz web
# en el navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# instancia del LED configurado en el GPIO26
lamp = LED(26)

# Instancia para el servo motor para el GPIO27
motor = Servo(27, pin_factory=factory)
# Inicializa el servo motor en min, equivalente
# en nuestro caso a cerrado
motor.min()
print(f"Initial servomotor value: {motor.value}")


@app.get("/")
def index():
    """Index"""
    return {"Hello": "Friend"}


@app.get("/health")
def health():
    """Checkear estado del servicio"""
    return "OK"


@app.get("/door/status")
def door_status():
    """Obtener estado abierto/cerrado de la puerta"""
    return {"status": True if motor.value == 1 else False}


@app.get("/led/status")
def led_status():
    """Obtener estado encendido/apagado del LED"""
    return {"status": lamp.is_lit}


@app.get("/led")
async def toggle_led():
    """Cambiar el estado del LED"""
    lamp.toggle()
    # devuelve el nuevo estado del LED
    return {"status": lamp.is_lit}


@app.get("/door")
async def toggle_door():
    """Cambiar el estado de la puerta"""
    print("door status changed...")
    print(f"motor value {motor.value}")
    if motor.value <= 0:
        motor.max()
    elif motor.value == 1:
        motor.min()
    print(f"last value of servo motor {motor.value}")
    # devolverá el estado resultante luego
    # de cambiar la posición del servo
    return {"status": True if motor.value == 1 else False}
