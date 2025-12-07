# ArchCost Deployment Guide

This guide provides step-by-step instructions to deploy ArchCost to the web on different cloud platforms.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Deploy Options](#quick-deploy-options)
3. [AWS Deployment (Recommended)](#aws-deployment)
4. [Azure Deployment](#azure-deployment)
5. [Google Cloud Platform](#google-cloud-platform)
6. [DigitalOcean (Simplest)](#digitalocean-app-platform)
7. [Render.com (Free Tier)](#rendercom)
8. [Post-Deployment Checklist](#post-deployment-checklist)

---

## Prerequisites

Before deploying, ensure you have:
- ✅ Docker Desktop installed
- ✅ Git installed
- ✅ A cloud platform account (AWS/Azure/GCP/DigitalOcean/Render)
- ✅ Your code pushed to GitHub/GitLab (optional but recommended)

---

## Quick Deploy Options

### 🎯 Recommended Based on Your Needs:

| Platform | Difficulty | Cost | Best For |
|----------|-----------|------|----------|
| **Render.com** | ⭐ Easy | Free tier available | Quick MVP, demos |
| **DigitalOcean** | ⭐⭐ Medium | ~$20/month | Production, simplicity |
| **AWS** | ⭐⭐⭐ Complex | ~$30-50/month | Enterprise, scalability |
| **Azure** | ⭐⭐⭐ Complex | ~$30-50/month | Microsoft ecosystem |
| **GCP** | ⭐⭐⭐ Complex | ~$30-50/month | Google ecosystem |

---

## DigitalOcean App Platform
**⭐ Simplest Option - Recommended for Beginners**

### Step 1: Prepare Your Repository
```bash
# Push your code to GitHub
git init
git add .
git commit -m "Prepare for deployment"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Create DigitalOcean Account
1. Go to https://www.digitalocean.com
2. Sign up (get $200 free credit for 60 days)
3. Verify your email and add payment method

### Step 3: Deploy Using App Platform
1. Click **"Create"** → **"Apps"**
2. Connect your GitHub repository
3. Select the `archcost` repository
4. Configure components:

#### Frontend Configuration
- **Type**: Web Service
- **Source Directory**: `/frontend`
- **Dockerfile Path**: `/frontend/Dockerfile`
- **HTTP Port**: 80
- **Instance Size**: Basic ($5/month)

#### Backend Configuration
- **Type**: Web Service
- **Source Directory**: `/backend`
- **Dockerfile Path**: `/backend/Dockerfile`
- **HTTP Port**: 8000
- **Instance Size**: Basic ($5/month)
- **Environment Variables**:
  ```
  MONGO_URL=<your-mongodb-connection-string>
  REDIS_URL=<your-redis-connection-string>
  ```

#### Database Configuration
- **Type**: Managed Database
- **Engine**: MongoDB
- **Plan**: Basic ($15/month)

OR use MongoDB Atlas (free tier):
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Add to backend environment variables

#### Redis Configuration
- Use DigitalOcean Managed Redis ($15/month)
- OR use Upstash (free tier): https://upstash.com

### Step 4: Update Frontend Environment
1. In App Platform, go to frontend settings
2. Add environment variable:
   ```
   API_URL=<your-backend-url>
   ```

### Step 5: Deploy
1. Click **"Create Resources"**
2. Wait 5-10 minutes for deployment
3. Your app will be available at: `https://your-app.ondigitalocean.app`

### Step 6: Configure Custom Domain (Optional)
1. Go to **Settings** → **Domains**
2. Add your custom domain
3. Update DNS records as instructed

**Total Cost: ~$25-35/month** (can use free trials and free tiers to reduce)

---

## Render.com
**⭐ Easiest with Free Tier**

### Step 1: Prepare Separate Dockerfiles
Render doesn't support docker-compose directly, so we use individual Dockerfiles.

### Step 2: Sign Up
1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repository

### Step 3: Create Services

#### Backend Service
1. Click **"New"** → **"Web Service"**
2. Connect your repository
3. Configure:
   - **Name**: archcost-backend
   - **Root Directory**: `backend`
   - **Build Command**: `docker build -t backend .`
   - **Start Command**: Leave blank (uses Dockerfile CMD)
   - **Plan**: Free (or Starter $7/month for better performance)
   - **Environment Variables**:
     ```
     MONGO_URL=<mongodb-connection-string>
     REDIS_URL=<redis-connection-string>
     ```

#### Frontend Service
1. Click **"New"** → **"Web Service"**
2. Connect repository
3. Configure:
   - **Name**: archcost-frontend
   - **Root Directory**: `frontend`
   - **Build Command**: `docker build -t frontend .`
   - **Plan**: Free
   - **Environment Variables**:
     ```
     BACKEND_URL=<backend-service-url>
     ```

#### Database
Use MongoDB Atlas (Free Tier):
1. Create cluster at https://www.mongodb.com/cloud/atlas
2. Get connection string
3. Add to backend environment variables

Use Upstash Redis (Free Tier):
1. Create database at https://upstash.com
2. Get connection string
3. Add to backend environment variables

### Step 4: Deploy
1. Render automatically deploys on git push
2. Access your app at: `https://archcost-frontend.onrender.com`

**Total Cost: FREE** (with free tier databases)

---

## AWS Deployment
**⭐⭐⭐ Most Scalable, Production-Ready**

### Option A: AWS App Runner (Simplest AWS Option)

#### Step 1: Install AWS CLI
```bash
# Windows (PowerShell)
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# Verify
aws --version
```

#### Step 2: Configure AWS CLI
```bash
aws configure
# Enter:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region: us-east-1
# - Default output format: json
```

#### Step 3: Push Images to ECR
```bash
# Create ECR repositories
aws ecr create-repository --repository-name archcost-backend
aws ecr create-repository --repository-name archcost-frontend

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
cd backend
docker build -t archcost-backend .
docker tag archcost-backend:latest <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/archcost-backend:latest
docker push <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/archcost-backend:latest

# Build and push frontend
cd ../frontend
docker build -t archcost-frontend .
docker tag archcost-frontend:latest <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/archcost-frontend:latest
docker push <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/archcost-frontend:latest
```

#### Step 4: Create MongoDB Atlas (or DocumentDB)
1. Use MongoDB Atlas (easier): https://www.mongodb.com/cloud/atlas
2. OR AWS DocumentDB (more expensive but AWS-native)

#### Step 5: Create ElastiCache for Redis
1. Go to AWS ElastiCache console
2. Create Redis cluster
3. Note the endpoint

#### Step 6: Create App Runner Services
1. Go to AWS App Runner console
2. Create service from ECR:
   - **Source**: Container registry → ECR
   - **Image**: Select `archcost-backend`
   - **Port**: 8000
   - **Environment Variables**:
     ```
     MONGO_URL=<mongodb-connection>
     REDIS_URL=<elasticache-endpoint>
     ```
3. Repeat for frontend (port 80)

#### Step 7: Access Your App
App Runner provides a URL: `https://xxxxxx.us-east-1.awsapprunner.com`

**Total Cost: ~$30-50/month**

---

### Option B: AWS ECS with Fargate (More Control)

This is more complex but gives you better control. I can provide detailed steps if needed.

---

## Azure Deployment

### Step 1: Install Azure CLI
```bash
# Windows (PowerShell)
winget install -e --id Microsoft.AzureCLI

# Login
az login
```

### Step 2: Create Resource Group
```bash
az group create --name archcost-rg --location eastus
```

### Step 3: Create Container Registry
```bash
az acr create --resource-group archcost-rg --name archcostacr --sku Basic
az acr login --name archcostacr
```

### Step 4: Build and Push Images
```bash
# Build and push backend
cd backend
az acr build --registry archcostacr --image archcost-backend:latest .

# Build and push frontend
cd ../frontend
az acr build --registry archcostacr --image archcost-frontend:latest .
```

### Step 5: Create Azure Container Apps
```bash
# Create Container Apps environment
az containerapp env create \
  --name archcost-env \
  --resource-group archcost-rg \
  --location eastus

# Deploy backend
az containerapp create \
  --name archcost-backend \
  --resource-group archcost-rg \
  --environment archcost-env \
  --image archcostacr.azurecr.io/archcost-backend:latest \
  --target-port 8000 \
  --ingress external \
  --env-vars MONGO_URL=<connection-string> REDIS_URL=<redis-connection>

# Deploy frontend
az containerapp create \
  --name archcost-frontend \
  --resource-group archcost-rg \
  --environment archcost-env \
  --image archcostacr.azurecr.io/archcost-frontend:latest \
  --target-port 80 \
  --ingress external
```

### Step 6: Setup Databases
Use MongoDB Atlas or Azure Cosmos DB
Use Azure Cache for Redis

**Total Cost: ~$30-50/month**

---

## Google Cloud Platform

### Step 1: Install gcloud CLI
```bash
# Download from: https://cloud.google.com/sdk/docs/install
# Verify
gcloud --version
```

### Step 2: Initialize and Login
```bash
gcloud init
gcloud auth login
```

### Step 3: Enable APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 4: Build and Deploy with Cloud Run
```bash
# Deploy backend
cd backend
gcloud run deploy archcost-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars MONGO_URL=<connection>,REDIS_URL=<redis>

# Deploy frontend
cd ../frontend
gcloud run deploy archcost-frontend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Total Cost: ~$20-40/month** (pay-per-use model)

---

## DigitalOcean Droplet (Docker Compose)
**⭐ Recommended for Full Control & Lower Cost**

This section describes how to manually deploy to a DigitalOcean Droplet (Virtual Machine) using `docker-compose`. This gives you full control over the infrastructure and costs essentially the same as the underlying compute (~$6/month for a basic droplet to start).

### Step 1: Create a Droplet
1.  Log in to your DigitalOcean account.
2.  Click **Create** -> **Droplets**.
3.  **Choose Region**: Select a datacenter closest to your users (e.g., Bangalore, New York, London).
4.  **Choose Image**: Select **Ubuntu 22.04 (LTS) x64** (or latest LTS).
5.  **Choose Size**:
    -   **Basic**: Regular Disk Type (SSD).
    -   Select the **$6/month** (1GB RAM / 1 CPU) plan for testing/MVP.
    -   *Recommendation*: 2GB RAM ($12/mo) is better for running frontend+backend+mongo+redis comfortably.
6.  **Authentication Method**: Select **SSH Key** (recommended for security) or Password.
    -   If SSH: Upload your public key (`id_rsa.pub`).
7.  **Hostname**: Give it a name (e.g., `archcost-prod`).
8.  Click **Create Droplet**.

### Step 2: Configure Domain & DNS (Primary/Secondary Host)
To make your app accessible via a domain (e.g., `archcost.com`), you need to configure the Nameservers (Primary and Secondary Hosts).

1.  **At your Domain Registrar (e.g., GoDaddy, Namecheap, BigRock)**:
    -   Find the "Nameservers" or "DNS Management" section.
    -   Change the nameservers from "Default" to **Custom Nameservers**.
    -   Enter DigitalOcean's nameservers:
        -   **Primary Host (NS1)**: `ns1.digitalocean.com`
        -   **Secondary Host (NS2)**: `ns2.digitalocean.com`
        -   (Optional) NS3: `ns3.digitalocean.com`
    -   Save. (Propagation can take up to 48 hours, but often happens in minutes).

2.  **At DigitalOcean**:
    -   Go to **Networking** -> **Domains**.
    -   Enter your domain name (e.g., `archcost.com`) and project.
    -   Click **Add Domain**.
    -   **Add Records**:
        -   **A Record**: Hostname `@` -> Select your Droplet (`archcost-prod`).
        -   **A Record**: Hostname `www` -> Select your Droplet.
        -   (This points `archcost.com` and `www.archcost.com` to your server's IP).

### Step 3: Server Setup
SSH into your droplet using its IP address (found on the dashboard).
```bash
ssh root@<your_droplet_ip>
# Or if using password, just enter the password when prompted.
```

#### Install Docker & Docker Compose
```bash
# Update package list
sudo apt update
sudo apt upgrade -y

# Install prerequisites
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common git

# Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-compose-plugin

# Verify installation
docker compose version
```

### Step 4: Deploy Code
Clone your repository. Since your project uses submodules (backend/frontend), you need to ensure they are cloned too.

```bash
# Clone the repository
git clone https://github.com/ankitbhatnagartech/archcost.git
cd archcost

# Initialize and update submodules (CRITICAL Step)
git submodule update --init --recursive
```

### Step 5: Configure Environment
Create the `.env` file for production configuration.

```bash
nano .env
```

Paste your configuration (adjust values as needed):
```env
# Backend defaults
MONGO_URL=mongodb://mongodb:27017
REDIS_URL=redis://redis:6379

# Or if using External Managed DBs (Specific IP/URL)
# MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net
```
Press `Ctrl+X`, then `Y`, then `Enter` to save.

### Step 6: Start Application
Use the production compose file we created.

```bash
# Pull and build the containers
docker compose -f docker-compose.prod.yml up -d --build

# Check status
docker compose -f docker-compose.prod.yml ps
```

Your application should now be live at `http://<your_droplet_ip>` or `http://archcost.com`.

### Step 7: Post-Install (Port 80 to Angular)
The `docker-compose.prod.yml` maps the Frontend container to port 80.
-   Ensure no other service (like standard Nginx/Apache) is blocking port 80 on the host.
-   If `curl localhost` works but external access doesn't, check DigitalOcean Firewalls (Networking -> Firewalls) to ensure Inbound Traffic on TCP ports 80 (HTTP) and 443 (HTTPS) is allowed.

---

## Post-Deployment Checklist

### ✅ Security
- [ ] Enable HTTPS (most platforms do this automatically)
- [ ] Set strong database passwords
- [ ] Configure CORS properly
- [ ] Enable firewall rules
- [ ] Set up environment variables securely

### ✅ Monitoring
- [ ] Enable application logs
- [ ] Set up health check monitoring
- [ ] Configure alerts for downtime
- [ ] Monitor costs

### ✅ Performance
- [ ] Enable CDN for static assets
- [ ] Configure auto-scaling
- [ ] Test load times
- [ ] Optimize database queries

### ✅ Maintenance
- [ ] Set up CI/CD for automatic deployments
- [ ] Schedule database backups
- [ ] Document deployment process
- [ ] Create rollback plan

---

## Recommended Quick Start

**For MVP/Demo (FREE):**
1. Use Render.com for frontend + backend
2. MongoDB Atlas Free Tier
3. Upstash Redis Free Tier
4. **Total: $0/month**

**For Production (Simple):**
1. DigitalOcean App Platform
2. MongoDB Atlas Shared Cluster ($0 or $9/month)
3. DigitalOcean Managed Redis ($15/month)
4. **Total: ~$25-35/month**

**For Enterprise (Scalable):**
1. AWS App Runner or Cloud Run
2. Managed MongoDB (Atlas or cloud-native)
3. Managed Redis
4. **Total: ~$30-50/month**

---

## Troubleshooting

### Container fails to start
- Check logs in cloud platform console
- Verify environment variables are set correctly
- Ensure database connection strings are correct

### Frontend can't reach backend
- Update frontend environment variable with correct backend URL
- Check CORS configuration in backend
- Verify network/firewall rules

### Database connection issues
- Whitelist your app's IP in database settings
- Check connection string format
- Ensure database is in same region (for lower latency)

---

## Next Steps

1. Choose your platform based on the table above
2. Follow the step-by-step guide for that platform
3. Test your deployment thoroughly
4. Set up monitoring and alerts
5. Configure your custom domain (optional)

**Need help?** Check the `observability.md` file for monitoring setup after deployment.
