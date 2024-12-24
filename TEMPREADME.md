
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

### Prerequisites

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
4. Cuando todos los contenedores se hayan iniciado podrá acceder a la web
   ```js
   http://localhost:80
   ```
5. Las diferentes APIs tienen documentación Swagger
   ```sh
   Origen de datos
   http://localhost:8001/docs

   Procesamiento de datos
   http://localhost:8002/docs
   ```

<p align="right">(<a href="#readme-top">Volver al índice</a>)</p>



<!-- CONTACT -->
## Contacto

José Antonio López Pérez - jose.lppz03@gmail.com

<p align="right">(<a href="#readme-top">Volver al índice</a>)</p>



[product-screenshot]: images/screenshot.png
