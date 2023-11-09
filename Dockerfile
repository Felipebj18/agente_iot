# Usa una imagen base de Ubuntu 20.04
FROM ubuntu:20.04

# Actualiza el sistema y realiza instalaciones iniciales
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.9 python3-pip wget && \
    apt-get clean

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de tu aplicación al contenedor
COPY . /app

# Instala las dependencias de Python
RUN pip3 install -r requirements.txt

# Instala otras dependencias necesarias (por ejemplo, Selenium)
# Aquí puedes agregar las instrucciones para instalar controladores de navegador, si es necesario.

# Expone los puertos si tu aplicación escucha en un puerto específico
EXPOSE 80

# Comando para ejecutar tu aplicación
CMD [ "python3", "app.py" ]

