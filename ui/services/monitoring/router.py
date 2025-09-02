from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from interfaces.monitoring import MonitoringManager

router = APIRouter(
    prefix='/monitoring',
    tags=['monitoring']
)


@router.get("/")
def get_monitoring():
    with open('ui/services/monitoring/templates/monitoring.html', 'r', encoding='utf-8') as file:
        return HTMLResponse(content=file.read())



@router.get("/data")
def get_real_time():
    manager = MonitoringManager()
    real_time = manager.get_all_real_time() 
    return {
        'list_page': real_time['list_page'],
        'data_extraction': real_time['data_extraction'],
        'priority_queue': manager.get_priority_queue_details()
    }

