For Backend dev 

1.install Docker desktop 

To run backend locally, go to the infra folder and run

 docker compose up --build
 
 in PowerShell. No need to install Python or PostgreSQL.



Step by step guide to run 

1. install  Docker Desktop (must be running) ,Git

2. Clone the repository
git clone <repo-url>
cd Air-ticket-Booking

3.Create environment file
cp .env.example .env

4.Start backend + database
cd infra
docker compose up --build

open from browser 

Backend API: http://localhost:8000

Health check: http://localhost:8000/health

5.Stop services

Ctrl + C
docker compose down


