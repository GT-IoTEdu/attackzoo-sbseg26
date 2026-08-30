# Demonstração rápida — AttackZoo Redux

> Execute somente no laboratório Docker local e a partir da **raiz do repositório**.

## 1. Preparação (executar uma vez antes do evento)

```bash
./setup.sh dependencies
newgrp docker
```

Quando o novo prompt aparecer, ainda na raiz do repositório:

```bash
./setup.sh redux
```

- `dependencies` instala os pacotes do sistema, o ambiente Python `.venv` e o Docker.
- `newgrp docker` abre uma nova sessão de shell com acesso ao Docker.
- `redux` constrói **7 imagens de ataque** e **3 servidores-alvo**, inicia os servidores e não constrói clientes benignos.

O primeiro build do perfil `redux` normalmente leva alguns minutos. Faça-o antes da apresentação.

| Categoria | ID usado no comando | Imagem atacante | Alvo da demonstração |
| --- | --- | --- | --- |
| Reconhecimento | `recon_arp_scan` | `attack-arp-scan` | Rede Docker local |
| Interceptação de rede | `net_arp_spoof` | `attack-arp-spoof` | Rede Docker local |
| Aplicação Web | `web_simple_scanner` | `attack-web-simple-scanner` | `server-http-server` |
| Força bruta | `bf_ssh` | `attack-ssh-bruteforce` | `server-ssh-server` |
| Exfiltração e tunelamento | `exf_icmp_tunnel` | `attack-icmp-tunnel` | `server-ssh-server` |
| Negação de serviço | `dos_http_simple` | `attack-dos-http-simple` | `server-http-server` |
| IoT | `iot_mqtt_publisher` | `attack-mqtt-publisher` | `server-mqtt-broker` |

Os servidores expõem HTTP em `8080`, SSH em `2222` e MQTT em `1883` no host. Os ataques abaixo usam diretamente as portas internas `80`, `22` e `1883`.

## 2. Preparação do terminal da demonstração

Execute este bloco uma vez ao abrir o terminal:

```bash
source .venv/bin/activate
./servers.sh start redux

HTTP_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server-http-server)
SSH_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server-ssh-server)
MQTT_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server-mqtt-broker)
DEMO_NET=$(docker network inspect bridge -f '{{(index .IPAM.Config 0).Subnet}}')
DEMO_GW=$(docker network inspect bridge -f '{{(index .IPAM.Config 0).Gateway}}')

python3 attackzoo.py status
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' --filter 'name=server-'
```

O `status` deve mostrar `docker_available=true` e os três servidores devem aparecer como `Up`.

## 3. Escolha e execute um ataque

### 1 — Descoberta de hosts por ARP

Realiza descoberta de hosts na rede Docker do laboratório.

```bash
python3 attackzoo.py run recon_arp_scan --target "$DEMO_NET"
```

### 2 — ARP spoofing

Simula interceptação entre o gateway e a rede Docker por 5 segundos.

```bash
python3 attackzoo.py run net_arp_spoof --spoof_gw "$DEMO_GW" --target "$DEMO_NET" --duration 5
```

### 3 — Scanner de vulnerabilidades Web

Executa o Nikto contra o servidor HTTP por até 10 segundos.

```bash
python3 attackzoo.py run web_simple_scanner --target "$HTTP_IP" --port 80 --duration 10
```

### 4 — Força bruta SSH

Executa tentativas de autenticação contra o servidor SSH por 10 segundos.

```bash
python3 attackzoo.py run bf_ssh --target "$SSH_IP" --port 22 --duration 10
```

### 5 — Túnel ICMP para SSH

Simula um túnel para o serviço SSH usando tráfego ICMP por 10 segundos.

```bash
python3 attackzoo.py run exf_icmp_tunnel --target "$SSH_IP" --port 22 --duration 10
```

### 6 — DoS HTTP

Envia 100 requisições HTTP com até 10 requisições simultâneas.

```bash
python3 attackzoo.py run dos_http_simple --target "$HTTP_IP" --port 80 --count 100 --concurrency 10 --delay_ms 20
```

### 7 — Flood de publicação MQTT

Publica 100 mensagens rapidamente no broker MQTT.

```bash
python3 attackzoo.py run iot_mqtt_publisher --target "$MQTT_IP" --port 1883 --count 100 --delay_ms 10 --payload_size 64
```

## 4. Comandos de apoio

```bash
# Ver ataques em execução
python3 attackzoo.py ps

# Ver os últimos logs de um ataque ainda ativo
python3 attackzoo.py logs ID_DO_ATAQUE

# Interromper um ataque manualmente
python3 attackzoo.py stop ID_DO_ATAQUE

# Reiniciar os três alvos se necessário
./servers.sh restart redux

# Encerrar o laboratório ao final do evento
./servers.sh stop redux

# Ver logs dos servidores
docker logs server-http-server
docker logs server-ssh-server
docker logs server-mqtt-broker
```

Exemplo de interrupção: `python3 attackzoo.py stop net_arp_spoof`.
