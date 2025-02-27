
<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a>
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">GreenhouseIOT</h3>

  <p align="center">
    Proyecto dedicado a la gestión de invernaderos inteligentes.
    <br />
    <a href="https://youtu.be/kXLEq7E9CJQ">View Demo</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Índice</summary>
  <ol>
    <li>
      <a href="#about-the-project">GreenhouseIOT</a>
      <ul>
        <li><a href="#built-with">Tecnologías</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Primeros pasos</a>
      <ul>
        <li><a href="#prerequisites">Prerequisitos</a></li>
        <li><a href="#installation">Instalación</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contacto</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## GreenhouseIOT

[![Product Name Screen Shot][product-screenshot]]()

GreenhouseIOT es un sistema que parte del programa de prácticas Vinci.
El objetivo principal detrás del proyecto es la gestión de pequeños módulos de invernadero inteligentes. Estos módulos incorporan conjuntos de sensores que envian sus lecturas periódicamente al sistema y permite al usuario su visualización y gestión a través de una interfaz web. El proyecto se divide en tres capas principales.

Arquitectura:
* Una primera capa de datos que engloba los módulos de invernadero y una api que recibe y prepara los datos para ser enviados a través de kafka
* Una segunda capa que engloba la base de datos, un servicio que consume los datos de la capa de origen y una api que gestiona el aceso a la base de datos
* Una capa dedicada a la explotación de datos a través de una interfaz web

El proyecto ha sido desarrollado en python. Los módulos de invernadero pueden ser replicados facilmente ya que en este proyecto encontrarás los archivos para poder imprimirlos en 3D y el esquema eléctrico empleado.

Para iniciar la aplicación consulte el apartado `Primeros pasos`.

<p align="right">(<a href="#readme-top">Volver al índice</a>)</p>



### Tecnologías

En esta sección se encuentra el listado de tecnologías utilizadas para el desarrollo del proyecto.

* [![FastAPI](https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white)](#)
* [![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
* [![Reflex](https://img.shields.io/badge/Reflex-37764B)](#)
* [![Blender](https://img.shields.io/badge/Blender-%23F5792A.svg?logo=blender&logoColor=white)](#)
* [![C++](https://img.shields.io/badge/C++-%2300599C.svg?logo=c%2B%2B&logoColor=white)](#)
* [![MariaDB](https://img.shields.io/badge/MariaDB-003545?logo=mariadb&logoColor=white)](#)
* [![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)](#)
* [![Kafka](https://img.shields.io/badge/Kafka-000545)](#)

<p align="right">(<a href="#readme-top">Volver al índice</a>)</p>



<!-- GETTING STARTED -->
## Primeros pasos

Para configurar el proyecto sigue estos simples pasos.

### Prerequisitos

Es necesario tener instalado:
* Docker (Se recomienda instalar docker desktop)
* El proyecto se inicia desde un archivo docker compose permitiendo iniciar todos los servicios o un subconjunto de ellos. Para un correcto funcionamiento es necesario crear una red docker externa:
  ```sh
  docker network create red_local_compartida
  ```

### Instalación

_Los siguientes pasos parten de la premisa de cumplir el listado de prerequisitos de la sección anterior_

1. Descargue el proyecto
2. Inicie docker desktop o los servicios docker equivalentes
3. Desde la raíz de proyecto, ejecute:
   ```sh
   docker compose --profile all up --build
   ```
4. Utilice su gestor de base de datos sql favorito para cargar el script que crea la base de datos y su estructura de tablas
   ```sh
   Ejemplo de flujo para HeidiSQL
   
    3.1 Cargar script SQL
    3.2 Cargar el archivo ddbb_schema.sql contenido en COMPONENTS/S01_GreenHouse_DataCore/ddbb_schema.sql
    3.3 Ejecutar el script
   ```
5. Cuando todos los contenedores se hayan iniciado podrá acceder a la web
   ```js
   http://localhost:80
   ```
6. Las diferentes APIs tienen documentación Swagger
   ```sh
   Origen de datos
   http://localhost:8001/docs

   Procesamiento de datos
   http://localhost:8002/docs
   ```
Es posible iniciar de forma parcial la aplicación, permitiedo separar las diferentes capas. Para ello se utilizan perfiles docker.

Perfiles disponibles:
* layer1
* layer2
* layer12
* layer3
* layerDB
* all

Ejemplo de uso de perfil que inicia solo la base de datos:
   ```sh
   docker compose --profile layerDB up --build
   ```
<p align="right">(<a href="#readme-top">Volver al índice</a>)</p>



<!-- CONTACT -->
## Contacto

José Antonio López Pérez - jose.lppz03@gmail.com

<p align="right">(<a href="#readme-top">Volver al índice</a>)</p>



<!-- CONTACT -->
## Posibles errores y su solución

Cuando se modifican las dependencias o en caso de nueva instalación es posible que se produzca un error con las dependencias de node, en caso de suceder se recomienda: 

 1- Pausar los contenedores, eliminar los contenedores, volumenes e imagenes asociadas

 2- Eliminar del proyecto la carpeta de node-modules y package-lock.json

 3- En local ejecutar npm install desde la raiz del componente vite

 4- Volver a iniciar los contenedores como se indica en la guia de inicio rapido

<p align="right">(<a href="#readme-top">Volver al índice</a>)</p>



[product-screenshot]: images/screenshot.png
