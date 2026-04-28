# SRE Project

This project is for the Intro to SRE course (Assignments 4 & 5). 
It is a simple microservices system with monitoring and Infrastructure as Code.

## Technologies Used
- **Docker & Docker Compose:** To run the containers.
- **Terraform:** To build the server infrastructure.
- **Python (FastAPI):** For backend services.
- **PostgreSQL:** For the database.
- **Prometheus & Grafana:** For system monitoring.

## How to Run the Project

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

## How to Simulate the Incident
1. Open the `docker-compose.yml` file.
2. Find `order_service` and change the `DATABASE_URL` to a fake name (for example, `netodb`).
3. Restart the service using the terminal: `docker-compose up -d order_service`.
4. Check the website (it will show an error) and Grafana (charts will go down).
5. To fix it, change the URL back to normal and restart the service again.