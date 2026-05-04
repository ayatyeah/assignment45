# SRE Project

This project is for the Intro to SRE course (Assignments 4, 5, and 6).
It is a simple microservices system with monitoring, automation, and Infrastructure as Code.

## Technologies Used
- **Docker & Docker Compose:** To run the containers.
- **Terraform:** To build the server infrastructure.
- **Python (FastAPI):** For backend services.
- **PostgreSQL:** For the database.
- **Prometheus & Grafana:** For system monitoring.

## How to Run the Project

### 0. Configure Environment
1. Copy the example file:
   ```bash
   copy .env.example .env
   ```
2. Fill in the values inside `.env`.
3. Validate config:
   ```powershell
   .\scripts\validate_env.ps1
   ```

### 1. Setup Infrastructure (Terraform)
1. Open your terminal and go to the `terraform` folder:
   ```bash
   cd terraform
   ```
2. Run these commands to create the server:
   ```bash
   terraform init
   terraform apply
   ```
3. Type `yes` to confirm. 

### 2. Start the Application (Docker)
1. Go back to the main project folder:
   ```bash
   cd ..
   ```
2. Build and start all containers:
   ```bash
   docker-compose up -d --build
   ```
3. Check if everything is running:
   ```bash
   docker ps
   ```

## System Links
After starting the containers, open your browser and go to:
- **Main Website:** [http://localhost](http://localhost)
- **Prometheus (Metrics):** [http://localhost:9090](http://localhost:9090)
- **Grafana (Dashboards):** [http://localhost:3000](http://localhost:3000) *(Login: admin / Password: admin)*

## Assignment 6: Automation and Capacity Planning

### Automation Mechanisms
- **Automated deployment:** Docker Compose for repeatable multi-container startup.
- **Configuration validation:** `scripts/validate_env.ps1` checks required variables.
- **Health checks:** Each service exposes `/health` and has Docker health checks.
- **Self-healing:** `restart: unless-stopped` is configured for all services.
- **Monitoring-based alerting:** Prometheus alert rules in [prometheus/alerts.yml](prometheus/alerts.yml).
- **Log inspection automation:** `scripts/log_inspect.ps1` searches for common failure patterns.

### Monitoring and Alerting
Prometheus scrapes service metrics and evaluates rules for:
- Service downtime (`up == 0`)
- High CPU usage (`process_cpu_seconds_total` rate)
- High 5xx error rates (`http_requests_total`)

### Capacity Planning
**Metrics used:** CPU, memory, request rate, error rate, restart frequency.

**Load simulation examples:**
```bash
hey -n 500 -c 50 http://localhost/products
```

**Observed behavior under load:**
- CPU usage rises most in the Order Service.
- Response time increases as concurrency grows.
- Error rates can spike if resources are constrained.
- Database becomes a potential bottleneck.

**Capacity analysis focus:**
- Maximum sustainable request rate per service.
- Resource consumption per container.
- Failure thresholds based on error rate and latency.

**Scaling strategies:**
1. **Horizontal scaling:** multiple instances for Order Service with load balancing.
2. **Vertical scaling:** increase CPU/RAM for containers and VM size via Terraform.
3. **Database optimization:** connection pooling, index tuning, and query review.

### Log Troubleshooting
```powershell
.\scripts\log_inspect.ps1
```

## How to Simulate the Incident
1. Open the `docker-compose.yml` file.
2. Find `order_service` and change the `DATABASE_URL` to a fake name (for example, `netodb`).
3. Restart the service using the terminal: `docker-compose up -d order_service`.
4. Check the website (it will show an error) and Grafana (charts will go down).
5. To fix it, change the URL back to normal and restart the service again.