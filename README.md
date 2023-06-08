# Prueba de Concepto de Timbre

Hardware

- Raspberry Pi 4 Model B 8GB
- Sensor PIR
- LED
- Buzzer
- Resistencia de 1 kOhm
- Servo Motor SG90
- Jumpers


Tecnologías


|nombre|version|
|--|--|
|Python|3.9.2|
|NodeJS|18|

## Configuración de la Raspberry Pi

Conectar los siguientes componentes en los pines GPIO especificados a continuación:

|Componente|GPIO|
|--|--|
|Buzzer|4|
|PIR Sensor|17|
|Servo Motor|27|
|LED|26|

Recomendamos utilizar el Raspberry Pi Imager para grabar el Sistema Operativo Raspberry Pi OS en una microSD y preconfigurar el usuario por defecto y la contraseña, así también como cargar los datos de la red Wi-Fi para podernos conectar tranquilamente por SSH a la Raspberry Pi.

Para conectarnos por SSH, primero debemos ubicar nuestra dirección IP en la red Wi-Fi, esto lo podemos descubrir
con comandos como ipconfig en Windows o ifconfig en Linux.

Luego, una vez conectado todo, enchufar la Raspberry Pi
y esperar unos minutos para que arranque correctamente,
luego a partir de la IP de nuestra computadora podemos utilizar herramientas como NMAP para escanear la red
y descubrir la IP de la Raspberry, es importante conservar esta IP puesto que se utilizará para configurar la intefaz
web.

Podemos escanear la red mediante el siguiente comando de nmap:

```bash
sudo nmap -sn 192.168.0.0/24
```

Los primeros 3 segmentos de la IP en el comando corresponden a los primeros 3 segmentos de nuestra propia IP.

Luego podemos conectarnos por SSH a la Raspberry Pi:

```bash
ssh <usuario>@<ip_raspberry>
```

Ingresamos la contraseña y habremos accedido a la Raspberry.

## Instalación

Instalar previamente las siguientes dependencias dentro de
la Raspberry Pi

```bash
sudo apt install python-setuptools python3-setuptools python3-pip python3-venv
```

Instalar "pigpiod" dentro de la Raspberry Pi para evitar 
la vibración intermitente del servo motor.

```bash
sudo apt install pigpio
```

después activar el daemon y configurarlo para que se inicie siempre:

```bash
sudo systemctl start pigpiod
```

```bash
sudo systemctl enable pigpiod
```

Clonar este repositorio desde adentro de la Raspberry Pi
mediante el comando

```bash
git clone https://github.com/YuutoG/mip115-2023-timbre-domotica
```

Desde la carpeta raíz del proyecto se deberá crear el entorno
virtual de python mediante

```bash
python -m venv venv
```

luego activarlo mediante:

```bash
source venv/bin/activate
```

instalar en el entorno virtual las dependencias del proyecto mediante:

```bash
pip install -r backend/requirements.txt
```

Para ejecutar en segundo plano nuestros archivos debemos tener Node.js 18

Instalar Node.js mediante nvm

```bash
curl | bash
```

A continuación instalamos Node.js 18 mediante

```bash
nvm install --lts
```

Luego instalamos globalmente la herramienta PM2 para gestionar todos nuetros programas.

```bash
npm install -g pm2
```

### Timbre

Primeramente para mantener el proceso de timbre nos desplazamos al directorio de timbre

```bash
cd timbre
```

Podemos probar el timbre localmente mediante:

```bash
python door_bell.py
```

Pero para que se mantenga ejecutando en segundo plano sin obstruir la consola, utilizar el siguiente comando:

```bash
pm2 start ./door_bell.py --name "timbre" --interpreter ../venv/bin/python
```

### Backend

Nos desplazamos al directorio de backend para levantar el servicio que controlará el LED y el servo motor (bisagra de puerta):

```bash
cd ../backend
```

Aquí ejecutaremos en servicio para que PM2 lo mantenga en segundo plano, por defecto se ejecutará en el puerto 8080, pero se puede cambiar la bandera --port para ejecutarlo en el puerto que considere más conveniente:
```bash
pm2 start "../venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload" --name "aPi"
```

### Frontend

Nos desplazamos para la carpeta frontend para ejecutar la interfaz web:

```bash
cd ../frontend
```

Primeramente instalamos toda las dependencias en limpio con

```bash
npm ci
```

Copiamos el archivo .env-local y lo renombramos .env.local.
Editamos este mismo archivo .env.local y nos aseguramos que solamente tenga
la siguiente línea en el archivo:

```
NEXT_PUBLIC_ENDPOINT=http://raspi:8080
```

Sustituir la palabra "raspi" por la IP de la Raspberry Pi. Esto es para que nuestra interfaz
web pueda interactuar con la API REST de Python con FastAPI.

Podemos levantar la interfaz web en modo desarrollo mediante:

```bash
npm run dev
```
Por defecto se ejecutará en el puerto 3000.

Para adaptarlo para producción, ejecutar el siguiente comando:

```bash
npm run build
```

Seguidamente podemos ejecutar el siguiente comando para que se ejecute en segundo plano con PM2:

```bash
pm2 start npm --name "nextjs" -- start
```

Ahora nos podemos dirigir a la interfaz web en la dirección:

```
http://<ip_de_raspberry>:3000/
```

Y podremos interactuar con la interfaz web para mover el servo motor y encender/apagar el LED.
