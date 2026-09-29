from pathlib import Path
import psutil

def get_temperature():
	temperature_file = Path("/sys/class/thermal/thermal_zone0/temp")
	raw_temperature = temperature_file.read_text()

	return int(raw_temperature) / 1000

def get_state(temperature):
	if temperature < 60:
		return "Normal"
	elif temperature <= 80:
		return "Warm"
	else:
		return "Critical"

def get_system_metrics():
	temperature = get_temperature()

	return {
		"temperature": temperature,
		"cpu_usage": psutil.cpu_percent(interval=1),
		"ram_usage": psutil.virtual_memory().percent,
		"disk_usage": psutil.disk_usage("/"). percent,
		"state": get_state(temperature)
	}

