from monitor import get_system_metrics

metrics = get_system_metrics()


print(f"CPU Temperature: {metrics['temperature']:.1f} Degrees C")
print(f"CPU Usage: {metrics['cpu_usage']}%")
print(f"RAM Usage: {metrics['ram_usage']}%")
print(f"Disk Usage: {metrics['disk_usage']}%")
print(f"CPU Temperature State: {metrics['state']}")
