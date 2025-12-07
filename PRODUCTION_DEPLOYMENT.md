# Production Deployment Guide: ArchCostEstimator

To deploy **ArchCostEstimator** as a production-ready application with the lowest possible cost, follow this step-by-step guide.

**Infrastructure Overview:**
-   **Domain**: `archcostestimator.com` (from BigRock)
-   **Cloud**: DigitalOcean Basic Droplet (Ubuntu LTS)
-   **Stack**: Angular (Frontend) + FastAPI (Backend) + MongoDB + Redis + Nginx (Reverse Proxy)
-   **CI/CD**: GitHub Actions

---

## 1. Domain Configuration (BigRock)

You need to point your domain to DigitalOcean's nameservers so you can manage DNS records easily from the DigitalOcean dashboard.

1.  Log in to your [BigRock Panel](https://myorders.bigrock.in/orders).
2.  Click on your domain name (`archcostestimator.com`).
3.  Look for the **"Name Servers"** option.
4.  Change the nameservers from "BigRock/Default" to **Custom Name Servers**.
5.  Enter the following:
    -   **Name Server 1**: `ns1.digitalocean.com`
    -   **Name Server 2**: `ns2.digitalocean.com`
    -   **Name Server 3**: `ns3.digitalocean.com` (Optional)
6.  Click **Update Name Servers**. (Note: This can take 1-48 hours to propagate, but usually happens within minutes).

---

## 2. Server Setup (DigitalOcean)

### A. Create Droplet
1.  Log in to [DigitalOcean Cloud](https://cloud.digitalocean.com/droplets).
2.  Click **Create** > **Droplets**.
3.  **Region**: Select the data center closest to your target audience (e.g., Bangalore `BLR1`).
4.  **Image**: Select **Ubuntu 24.04 (LTS) x64** (or 22.04 LTS).
5.  **Size**:
    -   Select **Regular Disk (SSD)**.
    -   Choose the **$6/month** plan (1GB RAM / 1 CPU) for absolute lowest cost.
    -   *(Recommended)*: The **$12/month** (2GB RAM) plan is safer for running MongoDB + Redis + App efficiently.
6.  **Authentication**:
    -   **SSH Key** (Recommended): Create a new SSH key pair on your local machine and upload the public key.
    -   **Password**: Create a strong root password.
7.  **Hostname**: Name it `archcost-production`.
8.  Click **Create Droplet**.

### B. Configure DNS (DigitalOcean)
1.  Go to **Networking** > **Domains** in the sidebar.
2.  Enter `archcostestimator.com` and click **Add Domain**.
3.  Add the following records:
    -   **A Record**:
        -   Hostname: `@`
        -   Will Direct To: Select your droplet (`archcost-production`)
        -   TTL: 3600
    -   **A Record**:
        -   Hostname: `www`
        -   Will Direct To: Select your droplet (`archcost-production`)
        -   TTL: 3600
    -   **A Record** (for API - optional if using path routing, which we are):
        -   We are using `archcostestimator.com/api`, so no separate subdomain needed.

### C. Connect & Install Software
SSH into your server:
```bash
ssh root@archcostestimator.com
# or ssh root@<DROPLET_IP_ADDRESS>
```

Run these commands to install Docker:
```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Verify
docker compose version
```

---

## 3. GitHub Actions CI/CD Setup

We have created a workflow file `.github/workflows/deploy.yml` that will automatically deploy your code when you push to the `main` branch.

### Configure Secrets
1.  Go to your GitHub Repository > **Settings** > **Secrets and variables** > **Actions**.
2.  Click **New repository secret**.
3.  Add the following secrets:
    *   **`HOST`**: Your Droplet IP address (e.g., `164.x.x.x`).
    *   **`USERNAME`**: `root`
    
    **Option A: Using SSH Key (Recommended)**
    *   **`KEY`**: The **Private SSH Key** matching the public key you added to the Droplet.
        *   This is the contents of your local `id_rsa` (NOT `id_rsa.pub`).
        *   It starts with `-----BEGIN OPENSSH PRIVATE KEY-----`.

    **Option B: Using Password (Easier, but less secure)**
    *   **`PASSWORD`**: The root password you created when setting up the Droplet.
    *   *Note*: If you provide both `KEY` and `PASSWORD`, the workflow will default to using the Key. If you only have a password, you do **not** need to add the `KEY` secret.

---

## 4. Manual First Deployment

It is good practice to do the first deployment manually to ensure everything works.

1.  SSH into your server.
2.  Clone your repository:
    ```bash
    git clone https://github.com/ankitbhatnagartech/archcost.git
    cd archcost
    git submodule update --init --recursive
    ```
3.  Start the application with the production compose file:
    ```bash
    docker compose -f docker-compose.prod.yml up -d --build
    ```
4.  Check status:
    ```bash
    docker compose -f docker-compose.prod.yml ps
    ```

---

## 5. Post-Deployment Configuration & Hardening (Critical)

This section details the specific steps to secure and optimize your production deployment.

### 5.1. ✅ Security: Firewall Configuration
We will use `ufw` (Uncomplicated Firewall) on the DigitalOcean Droplet to restrict access.

1.  **SSH** into your droplet:
    ```bash
    ssh root@archcostestimator.com
    ```
2.  **Allow SSH Connections** (CRITICAL - Do this first or you'll lock yourself out!):
    ```bash
    ufw allow OpenSSH
    ```
3.  **Allow Web Traffic**:
    ```bash
    ufw allow 80/tcp   # HTTP
    ufw allow 443/tcp  # HTTPS
    ```
4.  **Enable Firewall**:
    ```bash
    ufw enable
    ```
    *   Type `y` and press Enter when asked to confirm.
5.  **Verify**:
    ```bash
    ufw status
    ```
    *   Output should show `22/tcp`, `80/tcp`, and `443/tcp` as allowed.

### 5.2. ✅ Security: Enable HTTPS (SSL) with Certbot
We will use Let's Encrypt to get a free SSL certificate.

**Step 1: Install Certbot**
```bash
snap install --classic certbot
```

**Step 2: Generate Certificate**
Stop Nginx momentarily to free up port 80 for verification:
```bash
docker compose -f docker-compose.prod.yml stop nginx
```
Run Certbot (Standalone Mode):
```bash
certbot certonly --standalone -d archcostestimator.com -d www.archcostestimator.com
```
*   Enter your email when prompted.
*   Agree to terms (`Y`).
*   If successful, certs are saved in `/etc/letsencrypt/live/archcostestimator.com/`.

**Step 3: Update Nginx Configuration**
Edit `nginx/default.conf` locally (or on server) to enable SSL. Replace the entire content with:

```nginx
server {
    listen 80;
    server_name archcostestimator.com www.archcostestimator.com;
    
    # Redirect HTTP to HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name archcostestimator.com www.archcostestimator.com;

    # SSL Certificates (Volume Mount Paths)
    ssl_certificate /etc/letsencrypt/live/archcostestimator.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/archcostestimator.com/privkey.pem;

    # Frontend Proxy
    location / {
        proxy_pass http://frontend:80;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Static Assets Caching
    location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg)$ {
        proxy_pass http://frontend:80;
        expires 6M;
        access_log off;
        add_header Cache-Control "public, max-age=15552000, immutable";
    }

    # Backend API Proxy
    location /api {
        rewrite ^/api/(.*) /$1 break;
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**Step 4: Update Docker Compose for SSL Volumes**
Update `docker-compose.prod.yml` to mount the certs. Add this to the `nginx` service:

```yaml
  nginx:
    # ... other config ...
    ports:
      - "80:80"
      - "443:443"  # Add port 443
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
      - /etc/letsencrypt:/etc/letsencrypt:ro  # Mount Certs
```

**Step 5: Redeploy**
Push changes to GitHub or manually restart:
```bash
docker compose -f docker-compose.prod.yml up -d --build --remove-orphans
```

### 5.3. ✅ Security: Configure MongoDB Authentication
Never run a database without a password in production.

1.  **Create .env File**:
    On your server, creating a `.env` file prevents sensitive data from being in git.
    ```bash
    nano .env
    ```
2.  **Add Credentials**:
    (Replace with YOUR strong passwords)
    ```env
    MONGO_INITDB_ROOT_USERNAME=admin
    MONGO_INITDB_ROOT_PASSWORD=YOUR_STRONG_PASSWORD_HERE
    MONGO_URL=mongodb://admin:YOUR_STRONG_PASSWORD_HERE@mongodb:27017
    REDIS_URL=redis://redis:6379
    ```
3.  **Save & Exit**: Press `Ctrl+O`, `Enter`, `Ctrl+X`.
4.  **Restart Containers** to load the new environment variables:
    ```bash
    docker compose -f docker-compose.prod.yml up -d
    ```

### 5.4. ✅ Monitoring & Logs
1.  **Live Application Logs**:
    To see what's happening right now across all services:
    ```bash
    docker compose -f docker-compose.prod.yml logs -f --tail=100
    ```
    *   To follow just one service (e.g., backend):
        ```bash
        docker compose -f docker-compose.prod.yml logs -f backend
        ```

2.  **Uptime Monitoring**:
    *   Sign up for a free account at [UptimeRobot.com](https://uptimerobot.com/).
    *   Add a "New Monitor".
    *   **Monitor Type**: HTTP(s).
    *   **Friendly Name**: ArchCost Production.
    *   **URL**: `https://archcostestimator.com` (or http if SSL is not set up yet).
    *   **Interval**: 5 minutes.
    *   It will email you instantly if your site goes down.

### 5.5. ✅ Performance
1.  **Browser Caching**:
    *   We have already configured `nginx/default.conf` to add `Cache-Control` headers for images, CSS, and JS. This speeds up the site for returning visitors.
2.  **Redis Caching**:
    *   The Redis container is running. Verify the backend is using it by checking logs for "Connected to Redis" messages.

### 5.6. ✅ Maintenance (Backups)
1.  **Enable Droplet Backups**:
    *   Go to **DigitalOcean Dashboard**.
    *   Click on your droplet `archcost-production`.
    *   Click **Backups** in the left menu.
    *   Click **Enable Backups**.
    *   **Cost**: Adds 20% to your droplet cost (e.g., +$1.20/mo on the $6 plan).
    *   **Benefit**: Weekly system-level snapshots. If you mess up the server, you can restore to last week's state in one click.

2.  **System Updates**:
    Once a month, SSH in and run:
    ```bash
    apt update && apt upgrade -y
    ```
    (Note: This might restart services. Check your site afterwards).

---

**Congratulations!** Your app should now be live at `http://archcostestimator.com`.
