from fastapi import APIRouter, HTTPException, status
from app.kafka.producer import send_data_to_kafka
from app.models.models import SensorData



router = APIRouter(tags=["Data Source"], prefix="/send")



@router.post("/sensordata", status_code=status.HTTP_201_CREATED, description="Send the sensor data here.")
async def receive_data(data: SensorData):
    try:
        print(f"gh_name: {data.gh_name}, gh_ip: {data.gh_ip}, Temperature: {data.temperature} °C, Humidity: {data.humidity} %, Water Level: {data.water_level}, Moist: {data.moist}, Light: {data.light_level} ")
        send_data_to_kafka(data.model_dump())
        return {"message": "Data received and sent to Kafka successfully."}
    except Exception as e:
        print(f"Error while sending data to Kafka: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the data. Please try again later.",
        )
