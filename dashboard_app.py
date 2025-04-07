from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# Enable CORS for external requests (YOLOv8 app can send data here)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initial parking data
current_data = {
    "count": 0,
    "capacity": 10,
    "status": "Available"
}

# Schema for incoming data
class ParkingData(BaseModel):
    count: int
    capacity: int
    status: str

# Endpoint to update the dashboard
@app.post("/update")
def update_data(data: ParkingData):
    current_data.update(data.dict())
    return {"message": "Updated successfully"}

# HTML Dashboard view
@app.get("/", response_class=HTMLResponse)
def index():
    color = "green" if current_data["status"].lower() == "available" else "red"
    return f"""
    <html>
        <head>
            <title>Two-Wheeler Parking Dashboard</title>
            <meta http-equiv="refresh" content="1" />
        </head>
        <body style="font-family: Arial; text-align: center; padding-top: 50px;">
            <h1>🚗 Two-Wheeler Parking Status</h1>
            <h2 style="color:{color};">
                Status: {current_data["status"]}
            </h2>
            <h3>
                Count: {current_data["count"]} / {current_data["capacity"]}
            </h3>
        </body>
    </html>
    """

# 🔁 Run locally
if __name__ == "__main__":
    uvicorn.run("dashboard_app:app", host="0.0.0.0", port=10000, reload=True)
