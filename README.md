Number Classification API

Overview

This project is a Flask-based API that classifies numbers based on mathematical properties and provides fun facts. The API is deployed on an AWS EC2 instance using Gunicorn and Nginx for production.

Features

Classifies numbers as prime, perfect, Armstrong, etc.

Provides interesting facts about numbers.

Publicly accessible via an AWS EC2 instance.

Uses Flask, Gunicorn, and Nginx for a scalable deployment.

Installation and Setup

1. Launch an EC2 Instance

Choose an Ubuntu 22.04 LTS AMI.

Select an appropriate instance type (e.g., t2.micro for free-tier eligibility).

Configure security group:

Allow SSH (22) from your IP.

Allow HTTP (80) from all.

Allow custom TCP (5000) from your IP (for testing).

2. Connect to Your EC2 Instance

ssh -i your-key.pem ubuntu@your-ec2-public-ip

3. Update and Install Required Packages

sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx git

4. Clone the Repository

git clone https://github.com/your-repo/number-classification-api.git
cd number-classification-api

5. Create a Virtual Environment & Install Dependencies

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

6. Test the Flask App

python app.py

The API should now be accessible at http://your-ec2-public-ip:5000/api/classify-number?number=153

Deployment with Gunicorn & Nginx

7. Configure Gunicorn

sudo nano /etc/systemd/system/number-classification.service
Paste the following:

[Unit]
Description=Number Classification API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/number-classification-api
Environment="PATH=/home/ubuntu/number-classification-api/venv/bin"
ExecStart=/home/ubuntu/number-classification-api/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target

Save and exit, then enable and start the service:

sudo systemctl daemon-reload
sudo systemctl enable number-classification
sudo systemctl start number-classification
sudo systemctl status number-classification

8. Configure Nginx as a Reverse Proxy

# Install Nginx
sudo apt install nginx

# Remove default site if it exists
sudo rm /etc/nginx/sites-enabled/default

# Create new Nginx configuration
sudo nano /etc/nginx/sites-available/number-classification
Paste the following:

server {
    listen 80 default_server;
    server_name _;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

Save and exit.

Activate the configuration:

# Create symbolic link
sudo ln -sf /etc/nginx/sites-available/number-classification /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

9. Test the API

Visit:

http://your-ec2-public-ip/api/classify-number?number=153

If the API responds correctly, the deployment is successful!


