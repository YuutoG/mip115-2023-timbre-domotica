from gpiozero import Buzzer, MotionSensor

# Instanciamos un objeto de la clase buzzer
# configurada para manejar el GPIO4
buzz = Buzzer(4)
# Y aquí para manejar el sensor PIR
# en el GPIO17
pir = MotionSensor(17)

# Mantenerse continuamente escuchando
while True:
    # Iniciar con el Buzzer apagado
    buzz.off()
    print("Timbre apagado")
    print("Esperando movimiento...")
    # Aquí se espera a que el PIR reciba alguna señal
    pir.wait_for_motion()
    print("¡Movimiento detectado!")
    print("Activando timbre...")
    # una vez recibe señal se activa el buzzer
    buzz.on()
    print("Esperando no movimiento...")
    # espera a que ya no reciba ninguna señal
    pir.wait_for_no_motion()
    print("¡Sin Movimiento!")
    print("Apagando el timbre...")
    # apaga el Buzzer una vez ya no detecta movimiento
    buzz.off()
