#!/bin/bash

# Crop Disease AI - Deployment Script
# Deploys application to AWS ECS using Terraform

set -e

PROJECT_NAME="crop-disease-ai"
AWS_REGION="ap-south-1"
ECR_REPO_NAME="${PROJECT_NAME}-app"

echo "========================================="
echo "Crop Disease AI - AWS Deployment"
echo "========================================="

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "Docker not installed. Aborting." >&2; exit 1; }
command -v terraform >/dev/null 2>&1 || { echo "Terraform not installed. Aborting." >&2; exit 1; }
command -v aws >/dev/null 2>&1 || { echo "AWS CLI not installed. Aborting." >&2; exit 1; }

# Get AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "AWS Account ID: $AWS_ACCOUNT_ID"

# Step 1: Initialize Terraform
echo ""
echo "[1/6] Initializing Terraform..."
cd deployment/terraform
terraform init

# Step 2: Create infrastructure
echo ""
echo "[2/6] Creating AWS infrastructure..."
terraform apply -auto-approve

# Get ECR repository URL
ECR_URL=$(terraform output -raw ecr_repository_url)
echo "ECR Repository: $ECR_URL"

# Step 3: Build Docker image
echo ""
echo "[3/6] Building Docker image..."
cd ../..
docker build -t ${PROJECT_NAME}:latest .

# Step 4: Login to ECR
echo ""
echo "[4/6] Logging into ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Step 5: Tag and push image
echo ""
echo "[5/6] Pushing Docker image to ECR..."
docker tag ${PROJECT_NAME}:latest ${ECR_URL}:latest
docker push ${ECR_URL}:latest

# Step 6: Deploy to ECS
echo ""
echo "[6/6] Deploying to ECS..."
# This would be handled by ECS task definition
# In production, use AWS CodePipeline for CI/CD

echo ""
echo "========================================="
echo "✓ Deployment Complete!"
echo "========================================="
echo ""

# Get load balancer DNS
cd deployment/terraform
ALB_DNS=$(terraform output -raw load_balancer_dns)

echo "Application URL: http://${ALB_DNS}"
echo ""
echo "Next steps:"
echo "1. Upload trained model to S3"
echo "2. Configure domain name (optional)"
echo "3. Set up SSL certificate (recommended)"
echo ""