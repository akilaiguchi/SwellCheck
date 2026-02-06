# 🏄‍♂️ OpenSwell: Event-Driven Ocean Data Platform

A distributed, highly-scalable backend system designed to ingest, process, and alert users based on real-time buoy data from the National Data Buoy Center (NDBC).

[Image of microservices architecture showing ingestion, kafka, and data storage layers]

## 🏗 System Architecture
This project transitions a simple scraping script into a production-grade microservices architecture to demonstrate modern backend engineering principles.

- **Ingestion Service (Python/Docker):** Polling service that fetches raw spectral buoy data and publishes events to Kafka.
- **Message Broker (Apache Kafka):** Decouples data ingestion from processing, ensuring system resiliency and backpressure management.
- **Data Processor (Go/Python):** Consumes raw streams, calculates significant wave height trends, and persists data.
- **Storage Layer (PostgreSQL + TimescaleDB):** Optimized for time-series swell data.
- **Caching Layer (Redis):** Stores "latest-read" states to provide sub-millisecond API responses.
- **API Gateway (GraphQL):** Unified interface for querying historical trends and station metadata.
- **Notification Engine:** Event-driven worker that triggers SMS/Push alerts via Twilio when specific "Swell Events" are detected.

---

## 🛠 Tech Stack
* **Language:** Python 3.x (Ingestion), Go (Processing - Optional/Planned)
* **Infrastructure:** Docker, Kubernetes (K8s), Terraform
* **Data:** PostgreSQL, Redis, Apache Kafka
* **API:** GraphQL (Apollo/Graphene)
* **CI/CD:** GitHub Actions
* **Monitoring:** Prometheus & Grafana

---

## 🚀 Scalability Features (The "Why")
- **Event-Driven:** Using Kafka allows the system to handle bursts of data from hundreds of buoys without crashing the database.
- **Containerization:** Entire stack is Dockerized for environment parity between development and my MacBook-based home server.
- **Orchestration:** K8s manifests include Horizontal Pod Autoscalers (HPA) to simulate handling high-traffic swell events.
- **Infrastructure as Code:** Terraform configurations included for automated deployment to AWS (EKS/RDS).

---

## 📦 Local Setup & Deployment

### Prerequisites
- Docker & Docker Desktop
- Tailscale (for remote access to the MacBook Air node)

### Running the Stack
```bash
# Clone the repository
git clone [https://github.com/yourusername/openswell.git](https://github.com/yourusername/openswell.git)

# Spin up the infrastructure (Postgres, Kafka, Redis)
docker-compose up -d

# Check service logs
docker logs -f ingestion-service