# ArchCost Production Deployment Guide

**Current Status**: Fully Deployed & Secure (HTTPS)
**URL**: [https://archcostestimator.com](https://archcostestimator.com)

## Quick Reference Commands

### Restart Services
```bash
docker compose -f docker-compose.prod.yml up -d
```

### View Logs
```bash
docker compose -f docker-compose.prod.yml logs -f
```

### Reload Nginx (After Config Changes)
```bash
docker compose -f docker-compose.prod.yml exec nginx nginx -s reload
```

---

## Architecture Overview

-   **Frontend**: Angular (Nginx container)
-   **Backend**: FastAPI (Python container)
-   **Database**: MongoDB (Container)
-   **Cache**: Redis (Container)
-   **Reverse Proxy**: Nginx (Container) - Handles SSL termination
-   **SSL**: Let's Encrypt (Certbot on Host Machine)

## Initial Setup Instructions (For Re-deployment)

If you strictly follow these steps, you will replicate the current working production environment.

### 1. Host Setup (Ubuntu)
Install Docker, Docker Compose, and Certbot.
```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin certbot
```

### 2. Generate SSL Certificates
Run Certbot on the host first. Nginx container must be stopped/not listening on port 80 during this step.
```bash
# Stop nginx if running
docker stop archcost-nginx-1

# Generate Certs
certbot certonly --standalone -d archcostestimator.com -d www.archcostestimator.com
```

### 3. Configure Nginx
Ensure `nginx/default.conf` uses the certificates and has inline security parameters.
*(See repository `nginx/default.conf` for exact content)*

### 4. Deploy Application
```bash
docker compose -f docker-compose.prod.yml up -d --build
```
*Note: The compose file mounts `/etc/letsencrypt` from the host to the Nginx container.*

## Troubleshooting

### Nginx Restart Loop
If Nginx keeps restarting, check logs:
```bash
docker logs archcost-nginx-1
```
**Common Cause**: Missing SSL files. Ensure `default.conf` does not refer to external files like `options-ssl-nginx.conf` unless they exist. The fixed version uses inline parameters.

### Backend Connection Failed
If Frontend shows API errors:
-   Check Backend URL in environment variables.
-   Ensure Backend container is healthy: `docker ps`.
-   Check Backend logs: `docker logs archcost-backend-1`.
