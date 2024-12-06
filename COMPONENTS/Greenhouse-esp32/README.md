# Greenhouse-ESP32
Files for setting up and programming greenhouse modules compatible with the GreenhouseIOT system.

## Project Structure

### ESP32_Files

This folder contains all the necessary files for the proper functioning of the module.  
The files are designed to be uploaded using the Arduino IDE.

The ESP32 will periodically send sensor data to a REST API server. The API is implemented using FastAPI.

The ESP32 model used is the **ESP32-WROOM-32**.  
More information about this model, including its pinout, can be found in an image located in the `docs` folder.

Before starting the project, ensure your ESP32 is properly configured.  
I am a beginner with IoT and ESP32, but I installed the **CH340 driver** and the **CP210x driver** for Windows to set it up.

### docs

This folder contains the documentation required to assemble the project.  
It includes images of the ESP32 pinout and the electronic system used.

> **IMPORTANT**  
> Make sure to update the WiFi credentials and server URL variables in the main file (`AutomaticReads.ino`).
