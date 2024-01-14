# Despliegue de una Aplicación Flask en Producción

### Paso 1: Desarrollo Local

1. **Crea tu Aplicación Flask**:
   - Crea una aplicación Flask simple en tu máquina local. Puedes utilizar el código que proporcionaste inicialmente:

    ```python
    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Hola Mundo'

    if __name__ == '__main__':
        app.run(debug=True, port=8000)
    ```

2. **Ejecuta tu Aplicación Localmente**:
   - Ejecuta la aplicación en tu máquina local con el comando:

    ```bash
    python hello.py
    ```

   - Verifica que tu aplicación esté funcionando visitando [http://127.0.0.1:8000/](http://127.0.0.1:8000/) en tu navegador.

### Paso 2: Configuración de AWS EC2

3. **Inicia una Instancia de EC2**:
   - Inicia sesión en [AWS Management Console](https://aws.amazon.com/console/).
   - Accede al servicio EC2.
   - Haz clic en "Launch Instance" para crear una nueva instancia EC2.

4. **Elije una Imagen de Máquina (AMI)**:
   - Selecciona una AMI de Ubuntu Server, preferiblemente la última versión LTS.

5. **Elije un Tipo de Instancia**:
   - Selecciona el tipo de instancia que se adapte a tus necesidades, como `t2.micro` para pruebas.

6. **Configura la Instancia**:
   - Deja los valores predeterminados para detalles de la instancia y almacenamiento.

7. **Agrega Reglas de Grupo de Seguridad**:
   - Configura un grupo de seguridad que abra los puertos SSH (Puerto 22), HTTP (Puerto 80) y HTTPS (Puerto 443) para permitir el tráfico necesario.

8. **Lanza la Instancia**:
   - Revisa tu configuración y lanza la instancia.

9. **Conecta a la Instancia EC2**:
   - Conéctate a tu instancia EC2 utilizando SSH y la clave `.pem` que descargaste al crear la instancia:

    ```bash
    ssh -i /ruta/a/tu/key.pem ubuntu@tu-direccion-ip-publica
    ```

### Paso 3: Configuración del Servidor

10. **Actualiza el Sistema**:
    - Actualiza los paquetes del sistema operativo:

    ```bash
    sudo apt update
    sudo apt upgrade
    ```

11. **Instala Dependencias Necesarias**:
    - Instala las dependencias necesarias, como Python 3 y Apache (si es necesario):

    ```bash
    sudo apt install python3 python3-pip
    ```

12. **Transfiere tu Aplicación Flask al Servidor**:
    - Utiliza `scp`, Git u otro método para transferir los archivos de tu aplicación Flask desde tu máquina local al servidor. Ejemplo con `scp`:

    ```bash
    scp -i /ruta/a/tu/key.pem /ruta/a/tu/app/* ubuntu@tu-direccion-ip-publica:/ruta/en/el/servidor
    ```

13. **Configura tu Aplicación en el Servidor**:
    - En el servidor, crea un entorno virtual para tu aplicación y configura las dependencias necesarias.

### Paso 4: Configuración de Nginx

14. **Instala Nginx**:
    - Instala Nginx en el servidor:

    ```bash
    sudo apt install nginx
    ```

15. **Configura Nginx como Proxy Inverso**:
    - Crea un archivo de configuración de Nginx para tu aplicación. Por ejemplo:

    ```bash
    sudo nano /etc/nginx/sites-available/myapp
    ```

    Agrega la configuración para configurar Nginx como un proxy inverso:

    ```nginx
    server {
        listen 80;
        server_name tu_direccion_ip_publica;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

    Reemplaza `tu_direccion_ip_publica` con la dirección IP pública de tu instancia EC2.

16. **Habilita el Sitio y Reinicia Nginx**:
    - Crea un enlace simbólico para habilitar el sitio y verifica la configuración de Nginx:

    ```bash
    sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
    sudo nginx -t
    ```

    Reinicia Nginx:

    ```bash
    sudo systemctl restart nginx
    ```

### Paso 5: Ejecución de la Aplicación

17. **Ejecuta tu Aplicación con Gunicorn**:
    - En el servidor, asegúrate de estar en el directorio de tu aplicación y activa el entorno virtual (si estás utilizando uno).
    - Ejecuta tu aplicación Flask con Gunicorn:

    ```bash
    gunicorn app:app
    ```

18. **Prueba tu Aplicación**:
    - Accede a tu aplicación Flask en un navegador utilizando la dirección IP pública de tu instancia EC2.

