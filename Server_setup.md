
One-time Server Setup (Each Machine)
# 1. Install Docker + Compose plugin 
# (Also install NVIDIA driver and Container Toolkit on GPU servers)

# 2. Create a deploy user and add to docker group
sudo adduser --disabled-password deploy 
sudo usermod -aG docker deploy
sudo mkdir -p /opt/nepal-legal-rag 
sudo chown deploy:deploy /opt/nepal-legal-rag

# 3. Generate Deploy key (run this on your local machine); one per environment
ssh-keygen -t ed25519 -f deploy_develop -C "github-deploy-develop" -N ""
#   deploy_develop.pub  -> Add to server: /home/deploy/.ssh/authorized_keys
#   deploy_develop      -> Add to GitHub environment secret: SSH_KEY

# 4. Get known hosts signature (run locally)
ssh-keyscan -p 22 your.server.host      # -> Add output to GitHub secret: SSH_KNOWN_HOSTS


First Deploy Initialization
Run the GitHub Actions deploy workflow once. Expect it to stop at the preflight check. The release files are unpacked before the check, so afterwards you can SSH into the server and configure your environment variables:
code
Bash
cd /opt/nepal-legal-rag
mkdir -p env/develop
touch env/develop/infra.env env/develop/admin.env env/develop/user.env

# Env files are not in the repo. Open these files and add every required value
# Once configured, re-run the GitHub Actions workflow