import psutil
import time
from datetime import datetime
from db import TimescaleDBClient


def get_cpu_usage():
    """Get CPU usage percentage."""
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    """Get memory usage details."""
    memory = psutil.virtual_memory()
    return {
        "total": memory.total,
        "used": memory.used,
        "available": memory.available,
        "percent": memory.percent,
    }


def get_disk_usage():
    """Get disk usage details."""
    disk = psutil.disk_usage("/")
    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent,
    }


def get_network_io():
    """Get network I/O stats."""
    net_io = psutil.net_io_counters()
    return {
        "bytes_sent": net_io.bytes_sent,
        "bytes_received": net_io.bytes_recv,
    }


def get_system_uptime():
    """Get system uptime in seconds."""
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    return uptime_seconds


def collect_metrics():
    """Collect all system metrics."""
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "cpu_usage_percent": get_cpu_usage(),
        "memory_usage": get_memory_usage(),
        "disk_usage": get_disk_usage(),
        "network_io": get_network_io(),
        "system_uptime_seconds": get_system_uptime(),
    }
    return metrics


if __name__ == "__main__":
    while True:
        metrics = collect_metrics()
        time.sleep(5)

        db_client = TimescaleDBClient()
        db_client.connect()
        db_client.create_table()

        timestamp = datetime.utcnow()
        # db_client.insert_metric(timestamp, cpu_usage=25.5, memory_usage=65.0, disk_usage=50.2)
        db_client.insert_metric(
            timestamp,
            metrics["cpu_usage_percent"],
            metrics["memory_usage"]["percent"],
            metrics["disk_usage"]["percent"],
        )
        # db_client.bulk_insert_metrics(bulk_data)
        db_client.close()
