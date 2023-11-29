# MetaCodeManufacturingPlant CLI Usage
#
# Step 1: Initialize Project and Validate Workflow
$ MetaCodeManufacturingPlant init --project=SWOT_PESTLE_Dashboard
$ MetaCodeManufacturingPlant validate --workflow=swot_pestle_ddd_multi_agent_dashboard_workflow.yaml

# Step 2: Build Backend
# Here, `--agent=SWOTAnalyzer` means that we are using the SWOTAnalyzer agent's capabilities to perform tasks
$ MetaCodeManufacturingPlant build-backend --agent=SWOTAnalyzer --task=SWOTAnalysis
$ MetaCodeManufacturingPlant build-backend --agent=PESTLEAnalyzer --task=PESTLEAnalysis

# Step 3: Generate Summary Dashboards
$ MetaCodeManufacturingPlant generate-dashboard --agent=DashboardUpdater --task=SWOTSummary
$ MetaCodeManufacturingPlant generate-dashboard --agent=DashboardUpdater --task=PESTLESummary

# Step 4: Run Backend Unit Tests
$ MetaCodeManufacturingPlant test-backend

# Step 5: Build Frontend
$ MetaCodeManufacturingPlant build-frontend

# Step 6: Run Frontend Unit Tests
$ MetaCodeManufacturingPlant test-frontend

# Step 7: Build Full-stack Docker image
$ MetaCodeManufacturingPlant build-docker --image=swot_pestle_dashboard:latest

# Step 8: Deploy to Kubernetes Cluster
$ MetaCodeManufacturingPlant deploy-kubernetes --namespace=production --image=swot_pestle_dashboard:latest

# Step 9: Validate Deployment
$ MetaCodeManufacturingPlant validate-deployment --namespace=production

# Step 10: Enable Workflow Trigger
$ MetaCodeManufacturingPlant enable-trigger --trigger=NewDataArrival

# You can also list running workflows, inspect agents, check triggers, and much more.

# Optional: Viewing Logs
$ MetaCodeManufacturingPlant logs --namespace=production