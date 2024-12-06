# GreenHouse_DataCore
Data processing and persistence layer from GreenHouse IOT project

Es necesaria la creacion de una red interna si se desea correr todas las capas en la misma maquina host

docker network create red_local_compartida

docker compose up --build

En el caso contrario se debe modificar las url de acceso a las apis segun la maquina host deseada
