# 🗺 Project Roadmap: OpenSwell Implementation Phases

This document outlines the step-by-step evolution of the OpenSwell platform. Each phase is designed to build upon the last, moving from a monolithic script to a resilient, task-based microservices architecture optimized for performance and observability.

---

## 🟢 Phase 1: The MVP (Minimum Viable Product)
**Goal:** Successfully scrape one buoy and send a daily text message.
- [ ] **Data Research:** Identify the NDBC Station ID for your local break (e.g., 46221 for Santa Monica Bay).
- [ ] **BuoyScanner class:** Scan desired NDBC Station ID for latest information using `requests`.
- [ ] **Messaging Integration:** Connect Telegram bot api to send buoy information to messaging app.
- [ ] **Local Automation:** Set up a `cron` job to trigger the script once daily.

---

## 🟡 Phase 2: Persistence & Containerization
**Goal:** Move from "volatile" data to a permanent database and standard environment.
- [ ] **Database Setup:** Create a **PostgreSQL** instance via Docker Compose.
- [ ] **Schema Design:** Create tables for `buoy_stations` and `swell_readings` using `TIMESTAMPTZ` for time-series accuracy.
- [ ] **Dockerization:** Wrap the Python scraper in a `Dockerfile`.
- [ ] **Volume Mapping:** Ensure database data persists on your MacBook Air even if the container restarts.

---

## 🟠 Phase 3: The "Resilient" Pivot (Task Queues)
**Goal:** Decouple the "fetching" from the "saving" using Redis and Celery to ensure no data is lost.
- [ ] **Broker Setup:** Add **Redis** to your `docker-compose.yml` to act as the message broker.
- [ ] **Asynchronous Workers:** Implement **Celery** to handle background tasks.
    - **Producer:** Scraper fetches data and dispatches a task to Redis.
    - **Worker:** A separate process that picks up the task and writes the data to PostgreSQL.
- [ ] **Resiliency Test:** Shut down the Worker, trigger a scrape, and verify that the task waits in Redis until the worker is back online.

---

## 🔴 Phase 4: API & Speed (FastAPI & Caching)
**Goal:** Make the data accessible via a modern API and optimize performance.
- [ ] **FastAPI Server:** Build an API to query swell history and the latest buoy readings.
- [ ] **Redis Caching:** Implement a "Cache-Aside" pattern. When a user asks for the latest data, the API checks Redis first before hitting PostgreSQL.
- [ ] **Pydantic Models:** Use Pydantic for strict data validation and auto-generated OpenAPI (Swagger) documentation.

---

## 🔵 Phase 5: DevOps & Scaling (Kubernetes & IaC)
**Goal:** Demonstrate production-grade infrastructure and orchestration.
- [ ] **K8s Manifests:** Write `deployment.yaml` and `service.yaml` files for the API, Worker, and Redis.
- [ ] **Local K8s:** Run the entire stack on your MacBook using **Kind** (Kubernetes-in-Docker) or **K3s**.
- [ ] **Infrastructure as Code:** Write **Terraform** scripts to define an AWS VPC and an RDS instance to show cloud-readiness.
- [ ] **Remote Access:** Install **Tailscale** to securely monitor your local "server" logs from your phone while at the beach.

---

## 🟣 Phase 6: Observability (The Final Polish)
**Goal:** Monitor the health and performance of the entire system.
- [ ] **Prometheus:** Export metrics (e.g., scrape success rates, task latency) from your Python code.
- [ ] **Grafana Dashboard:** Build a visual dashboard showing wave height trends and system CPU/RAM usage.
- [ ] **Alerting:** Set up a notification (Discord/Slack/Email) if the scraper fails or the Redis queue gets backed up.