# Sistema de Monitoramento com Prometheus e Grafana

Este repositório contém instruções para iniciar, acessar e encerrar o sistema de monitoramento de métricas de desempenho da aplicação com **Prometheus** e **Grafana**.

---

## Requisitos

- **Python 3.x** com as bibliotecas:
  - `prometheus_client`
  - `psutil`
- **Prometheus**
- **Grafana**

## Montando ambiente de monitoramento da aplicação

1. **Instalação e configuração do Prometheus**
   - Instalação:
     ```bash
     sudo apt update && sudo apt install prometheus
     ```
   - Configuração:
     ```bash
     cd /etc/prometheus/
     sudo nvim prometheus.yml
     ```

     Certifique-se de que o `prometheus.yml` está configurado para coletar métricas do servidor de monitoramento em `localhost:9100`:
     ```yaml
     scrape_configs:
       - job_name: 'app_monitoring'
         static_configs:
           - targets: ['localhost:9100']
     ```

2. **Instalação do Grafana**
   - Instalação via Snap:
     ```bash
     sudo snap install grafana
     ```

3. **Preparação do Ambiente e Execução da Aplicação**
   - Navegue até a pasta do projeto:
     ```bash
     cd </path/of/project>
     ```
   - Crie e ative um ambiente virtual:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Instale as dependências de monitoramento:
     ```bash
     pip install prometheus_client psutil
     ```
   - Instale as dependências do projeto:
     ```bash
     pip install -r requirements.txt
     ```
   - Execute a aplicação:
     ```bash
     python3 <app_monitoramento.py>
     ```

---

## Passo a Passo para Iniciar o Monitoramento

1. **Iniciar o Prometheus**
   - Habilite o Prometheus para iniciar automaticamente:
     ```bash
     sudo systemctl enable prometheus
     ```
   - Inicie o Prometheus:
     ```bash
     sudo systemctl start prometheus
     ```
   - Verifique o status do Prometheus:
     ```bash
     sudo systemctl status prometheus
     ```

2. **Iniciar o Grafana**
   - Verifique se o Grafana está funcionando:
     ```bash
     sudo systemctl start grafana-server
     sudo systemctl status grafana-server
     ```

---

## Acessando e Monitorando as Métricas

Após configurar o painel no Grafana, você poderá acompanhar as métricas em tempo real para monitorar o desempenho da aplicação.

- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Grafana**: [http://localhost:3000](http://localhost:3000)

---

## Configurando o Grafana

Após acessar o Grafana em: [http://localhost:3000](http://localhost:3000)

1. **Configuração do Grafana**:  
   - Crie um painel no Grafana e adicione o Prometheus como fonte de dados (`http://localhost:9090`).

2. **Configuração das Visualizações para as Métricas**:  
   - Adicione painéis, escolha o tipo de visualização e insira as seguintes queries:
     - **Uso da CPU**: `cpu_usage{hostname="wsl2-server"}`
     - **Memória Total do Sistema**: `system_memory_total{hostname="wsl2-server"}`
     - **Uso de Memória da Aplicação**: `app_memory_usage{hostname="wsl2-server"} / system_memory_total{hostname="wsl2-server"} * 100`

---

## Finalizando o Monitoramento

1. **Finalizar o Prometheus**
   - Comando para parar o Prometheus:
     ```bash
     sudo systemctl stop prometheus
     ```
   - Verifique se o Prometheus parou de fato:
     ```bash
     sudo systemctl status prometheus
     ```

2. **Finalizar o Grafana Server**
   - Comando para parar o Grafana:
     ```bash
     sudo snap stop grafana
     ```
   - Verifique se o Grafana parou:
     ```bash
     sudo netstat -a -p | grep 3000
     ```

   Se não funcionar, utilize o passo abaixo:
   - Execute o comando abaixo para encontrar o PID do grafana-server:
     ```bash
     sudo netstat -tulnp | grep 3000
     ```
   - Após localizar o PID, use-o para parar o processo:
     ```bash
     sudo kill <PID>
     ```
   - Verifique se o Grafana parou:
     ```bash
     sudo netstat -tulnp | grep 3000
     ```

3. **Finalizar a Aplicação**
   - Finalize o script da aplicação pressionando `Ctrl+C` no terminal onde ela está em execução.

--- 
