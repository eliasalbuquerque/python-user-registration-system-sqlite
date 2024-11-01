from prometheus_client import Gauge, start_http_server
import psutil
import time
import threading

# Gauge para monitorar o uso da CPU
cpu_usage = Gauge(
    'cpu_usage', 
    'Uso da CPU', 
    ['hostname']
)

# Gauge para monitorar o uso de memória total do sistema
system_memory_total = Gauge(
    'system_memory_total', 
    'Total de memória do sistema em bytes', 
    ['hostname']
)

# Gauge para monitorar o uso de memória pelo processo da aplicação
app_memory_usage = Gauge(
    'app_memory_usage', 
    'Uso de memória pelo aplicativo em bytes', 
    ['hostname']
)

# Define o hostname
hostname = 'wsl2-server'

# Função para coletar métricas e iniciar o servidor HTTP
def monitor_metrics():
    while True:
        cpu_percent = psutil.cpu_percent()
        system_memory = psutil.virtual_memory().total
        app_memory = psutil.Process().memory_info().rss

        # Métricas
        cpu_usage.labels(hostname=hostname).set(cpu_percent)
        system_memory_total.labels(hostname=hostname).set(system_memory)
        app_memory_usage.labels(hostname=hostname).set(app_memory)

        # print(f"CPU: {cpu_percent}, Total Memória: {system_memory}, Memória App: {app_memory}")

        time.sleep(15)

# Crie uma thread para executar a função monitor_metrics
monitor_thread = threading.Thread(target=monitor_metrics)
monitor_thread.daemon = True  # Define a thread como daemon para que ela termine com o programa principal
monitor_thread.start()

# Inicie o servidor HTTP para o Prometheus
start_http_server(9100)
