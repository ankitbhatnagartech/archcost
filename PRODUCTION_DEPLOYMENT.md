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
    *   `HOST`: Your Droplet IP address (e.g., `164.x.x.x`).
    *   `USERNAME`: `root`
    *   `KEY`: The **Private SSH Key** matching the public key you added to the Droplet.
        *   If you used a password, you'd need to modify the workflow to use `password` instead of `key`, but SSH key is highly recommended for CI/CD.

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

## 5. Post-Deployment Checklists (Critical)

### ✅ Security
-   [ ] **Firewall**: In DigitalOcean Networking > Firewalls, create a firewall allowing only Inbound SSH (22), HTTP (80), and HTTPS (443).
-   [ ] **SSL (HTTPS)**: Currently the site runs on HTTP (port 80). To enable HTTPS for free:
    1.  Install Certbot on the host: `snap install --classic certbot`
    2.  Use the Nginx on the host (not container) to proxy to localhost:80, OR use a solution like `traefik` or `nginx-proxy` container that handles SSL automatically unless you want to mount certs into your Nginx container.
    *Simple approach*: Run `certbot` on the host, generate certs, and mount `/etc/letsencrypt` into your nginx container.
-   [ ] **Mongo Auth**: Ensure `MONGO_INITDB_ROOT_USERNAME` and password variables are set in a `.env` file on the server (do not commit `.env`).

### ✅ Monitoring
-   [ ] **Logs**: Run `docker compose -f docker-compose.prod.yml logs -f` to see live logs.
-   [ ] **Uptime**: Use a free UptimeRobot account to ping `https://archcostestimator.com` every 5 minutes.

### ✅ Performance
-   [ ] **Caching**: Redis is configured. Ensure backend is using it.
-   [ ] **Frontend**: The `nginx` container serves static files. Browser caching headers should be added to `nginx/default.conf` for assets.

### ✅ Maintenance
-   [ ] **Backups**: Enable "Backups" (Weekly) in DigitalOcean Droplet settings ($1.20/month extra).
-   [ ] **Updates**: Periodically run `apt update` on the server.

---

**Congratulations!** Your app should now be live at `http://archcostestimator.com`.
