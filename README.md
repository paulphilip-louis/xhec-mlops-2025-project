<div align="center">

# MLOps Project: Abalone Age Prediction

[![Python Version](https://img.shields.io/badge/python-3.10%20or%203.11-blue.svg)]()
[![Linting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&logoColor=white)](https://github.com/artefactory/xhec-mlops-project-student/blob/main/.pre-commit-config.yaml)
</div>

## 🎯 Project Overview

Welcome to your MLOps project! In this hands-on project, you'll build a complete machine learning system to predict the age of abalone (a type of sea snail) using physical measurements instead of the traditional time-consuming method of counting shell rings under a microscope.

**Your Mission**: Transform a simple ML model into a production-ready system with automated training, deployment, and prediction capabilities.

## 📊 About the Dataset

Traditionally, determining an abalone's age requires:
1. Cutting the shell through the cone
2. Staining it
3. Counting rings under a microscope (very time-consuming!)

**Your Goal**: Use easier-to-obtain physical measurements (shell weight, diameter, etc.) to predict the age automatically.

📥 **Download**: Get the dataset from the [Kaggle page](https://www.kaggle.com/datasets/rodolfomendes/abalone-dataset)


## 🚀 Quick Start

### Prerequisites
- GitHub account
- [Kaggle account](https://www.kaggle.com/account/login?phase=startRegisterTab&returnUrl=%2F) (for dataset download)
- Python 3.10 or 3.11

### Setup Steps

1. **Fork this repository**
   - ⚠️ **Important**: Uncheck "Copy the `main` branch only" to get all project branches

2. **Add your team members** as admins to your forked repository

3. **Set up your development environment**:
   ```bash
   # Create and activate a virtual environment
   uv sync
   source venv/bin/activate # on Windows: venv\Scripts\activate

   # Install pre-commit hooks for code quality
    uv pip install pre-commit
    uv run pre-commit install
   ```

## 📋 What You'll Build

By the end of this project, you'll have created:

### 🤖 **Automated ML Pipeline**
- Training workflows using Prefect
- Automatic model retraining on schedule
- Reproducible model and data processing

### 🌐 **Prediction API**
- REST API for real-time predictions
- Input validation with Pydantic
- Docker containerization

### 📊 **Production-Ready Code**
- Clean, well-documented code
- Automated testing and formatting
- Proper error handling

## 📝 How to Work on This Project

### The Branch-by-Branch Approach

This project is organized into numbered branches, each representing a step in building your MLOps system. Think of it like a guided tutorial where each branch teaches you something new!

**Here's how it works**:

1. **Each branch = One pull request** with specific tasks
2. **Follow the numbers** (branch_0, branch_1, etc.) in order
3. **Read the PR instructions** (PR_0.md, PR_1.md, etc.) before starting
4. **Complete all TODOs** in that branch's code
5. **Create a pull request** when done
6. **Merge and move to the next branch**

### Step-by-Step Workflow

For each numbered branch:

```bash
# Switch to the branch
git checkout branch_number_i

# Get latest changes (except for branch_1)
git pull origin main
# Note: A VIM window might open - just type ":wq" to close it

# Push your branch
git push
```

Then:
1. 📖 Read the PR_i.md file carefully
2. 💻 Complete all the TODOs in the code
3. 🔧 Test your changes
4. 📤 Open **ONE** pull request to your main branch
5. ✅ Merge the pull request
6. 🔄 Move to the next branch

> **💡 Pro Tip**: Always integrate your previous work when starting a new branch (except branch_1)!

### 🔍 Understanding Pull Requests

Pull Requests (PRs) are how you propose and review changes before merging them into your main codebase. They're essential for team collaboration!

**Important**: When creating a PR, make sure you're merging into YOUR forked repository, not the original:

❌ **Wrong** (merging to original repo):
![PR Wrong](assets/PR_wrong.png)

✅ **Correct** (merging to your fork):
![PR Right](assets/PR_right.png)

## 🔄 Running the Training Pipeline with Prefect

This project uses [Prefect](https://www.prefect.io/) to orchestrate the ML training pipeline with flows and tasks for better observability and monitoring.

### Starting the Prefect Server

Before running the training pipeline, you need to configure and start the Prefect server:

1. **Configure the Prefect API URL** (first time setup):
   ```bash
   prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
   ```

2. **Start the Prefect server**:
   ```bash
   uv run prefect server start
   ```

   Keep this terminal window open while you work with Prefect.

3. **Access the Prefect UI**:

   Open your browser and navigate to `http://localhost:4200`

### Running the Training Flow

You can run the training pipeline using `uv run` (recommended) or directly with Python:

1. **Using uv run** (recommended - automatically manages dependencies):
   ```bash
   uv run src/modelling/main.py --trainset_path data/abalone.csv
   ```

   Or with the default path:
   ```bash
   uv run src/modelling/main.py
   ```

2. **Using Python directly** (requires activated virtual environment):
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   python src/modelling/main.py --trainset_path data/abalone.csv
   ```

### Viewing Flow Runs in the UI

Once you've started the Prefect server and run the training pipeline, you can monitor and inspect your runs:

1. **Open the Prefect UI** at `http://localhost:4200`
2. **Navigate to Flow Runs**:
   - Click on "Runs" in the left sidebar
   - You'll see all your `training-pipeline` executions
3. **Inspect a Flow Run**:
   - Click on any flow run to see:
     - Execution status and duration
     - The `prepare-data` subflow with its tasks (load_data, encode_sex, splitting_data)
     - The `train` task showing model training
     - Detailed logs for each task
     - Visual execution timeline

**Pipeline Structure**:
- **Main Flow**: `training-pipeline` - orchestrates the entire process
- **Subflow**: `prepare-data` - handles data loading, encoding, and splitting
- **Tasks**: Individual operations (load_data, encode_sex, splitting_data, train, pickle_object)

All flow runs are tracked and can be reviewed in the UI, even after completion!

## 🚀 Complete MLOps Stack Deployment

This project includes a complete MLOps stack with Docker Compose orchestration:

### 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │   Prefect      │
│   Frontend      │    │   Backend       │    │   Orchestrator │
│   Port: 8501    │    │   Port: 8000    │    │   Port: 4200   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   MLflow        │
                    │   Tracking      │
                    │   Port: 5000    │
                    └─────────────────┘
```

### 🚀 Quick Deployment

#### Prerequisites
- Docker and Docker Compose installed
- Dataset `abalone.csv` in `data/` directory
- Git repository cloned

#### One-Command Deployment
```bash
# Make script executable and run
chmod +x deploy.sh
./deploy.sh start
```

This will:
- ✅ Build all Docker containers
- ✅ Start all services
- ✅ Verify health checks
- ✅ Display access URLs

#### Access the services:
- 🌐 **Streamlit Frontend**: http://localhost:8501
- 🔧 **API Backend**: http://localhost:8000
- 📚 **API Documentation**: http://localhost:8000/docs
- 🔄 **Prefect UI**: http://localhost:4200
- 📈 **MLflow UI**: http://localhost:5000

#### Deploy Prefect pipeline (once Prefect is ready):
```bash
./deploy.sh deploy-prefect
```

#### Stop services:
```bash
./deploy.sh stop
```

### 🔧 Manual Deployment

#### Step 1: Prepare Environment
```bash
# Create directories
mkdir -p data src/web_service/local_objects

# Download dataset (if not present)
# Place abalone.csv in data/ directory
```

#### Step 2: Start Services
```bash
# Start all services
docker compose up --build -d

# Check logs
docker compose logs -f
```

#### Step 3: Verify Deployment
```bash
# Check service health
curl http://localhost:8000/health    # API
curl http://localhost:8501/_stcore/health  # Streamlit
curl http://localhost:4200/api/health      # Prefect
curl http://localhost:5000/health         # MLflow
```

### 📊 Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Streamlit** | http://localhost:8501 | Interactive frontend |
| **API** | http://localhost:8000 | REST API backend |
| **API Docs** | http://localhost:8000/docs | Swagger documentation |
| **Prefect** | http://localhost:4200 | Workflow orchestration |
| **MLflow** | http://localhost:5000 | Model tracking |

### 🔄 Automated Training

#### Prefect Deployment
```bash
# Create Prefect deployment
python deploy_prefect.py

# View in Prefect UI
open http://localhost:4200
```

**Schedule**: Daily at 2 AM UTC  
**Tags**: mlops, training, abalone, production

#### Manual Training
```bash
# Run training pipeline
python src/modelling/main.py

# With custom parameters
python src/modelling/main.py --trainset_path data/abalone.csv
```

### 📈 Model Tracking

#### MLflow Integration
- **Automatic logging** of model parameters and metrics
- **Model versioning** and artifact storage
- **Experiment tracking** for model comparison

#### View Experiments
```bash
# Open MLflow UI
open http://localhost:5000

# View experiments, runs, and models
```

### 🧪 Testing

#### API Testing
```bash
# Health check
curl http://localhost:8000/health

# Prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sex": "M",
    "length": 0.455,
    "diameter": 0.365,
    "height": 0.095,
    "whole_weight": 0.514,
    "shucked_weight": 0.2245,
    "viscera_weight": 0.101,
    "shell_weight": 0.15
  }'
```

#### Frontend Testing
1. Open http://localhost:8501
2. Adjust sliders in sidebar
3. Click "Prédire l'âge"
4. Verify prediction results

### 🛠️ Troubleshooting

#### Common Issues

**Services Not Starting**
```bash
# Check Docker status
docker ps

# View logs
docker compose logs [service_name]

# Restart services
docker compose restart
```

**Port Conflicts**
```bash
# Check port usage
netstat -tulpn | grep :8000
netstat -tulpn | grep :8501
netstat -tulpn | grep :4200
netstat -tulpn | grep :5000

# Modify ports in docker-compose.yml if needed
```

**Data Issues**
```bash
# Verify dataset
ls -la data/abalone.csv

# Check data format
head -5 data/abalone.csv
```

#### Logs and Monitoring
```bash
# View all logs
docker compose logs

# Follow specific service logs
docker compose logs -f api
docker compose logs -f streamlit
docker compose logs -f prefect
docker compose logs -f mlflow
```

### 🛑 Stopping Services

#### Graceful Shutdown
```bash
# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# Stop and remove images
docker compose down --rmi all
```

### 📊 Production Considerations

#### Performance
- **API Response Time**: < 100ms
- **Concurrent Users**: 100+ simultaneous
- **Model Accuracy**: R² > 0.8

#### Monitoring
- **Health Checks**: Automatic every 30s
- **Logs**: Structured logging with timestamps
- **Metrics**: Response time, error rate, throughput

#### Scaling
- **Horizontal Scaling**: Multiple API instances
- **Load Balancing**: Nginx or similar
- **Database**: PostgreSQL for production data

### 🎯 Success Criteria

✅ **All services running** and healthy  
✅ **API responding** to prediction requests  
✅ **Streamlit interface** functional  
✅ **Prefect workflows** executing  
✅ **MLflow tracking** model experiments  
✅ **Docker containers** properly orchestrated

## 💡 Development Tips

### Managing Dependencies

Use uv to manage dependencies. Install or update packages with:

```bash
uv add <package>==<version>
```

Then sync the environment and regenerate the dependency files:

```bash
uv sync
```

### Code Quality
- The pre-commit hooks will automatically format your code
- Remove all TODOs and unused code before final submission
- Use clear variable names and add docstrings

### Continuous Integration

This project includes automated CI workflows that run on every push and pull request:

**What the CI checks:**
- ✅ Python 3.10 and 3.11 compatibility
- ✅ Pre-commit hooks (formatting, linting, file checks)
- ✅ Ruff linting and formatting
- ✅ Pytest with coverage reporting

The CI workflow automatically validates your code quality and ensures compatibility across Python versions. Make sure all CI checks pass before merging your pull requests!

## 📊 Evaluation Criteria

Your project will be evaluated on:

### 🔍 **Code Quality**
- Clean, readable code structure
- Proper naming conventions
- Good use of docstrings and type hints

### 🎨 **Code Formatting**
- Consistent style (automated with pre-commit)
- Professional presentation

### ⚙️ **Functionality**
- Code runs without errors
- All requirements implemented correctly

### 📖 **Documentation & Reproducibility**
- Clear README with setup instructions
- Team member names and GitHub usernames
- Step-by-step instructions to run everything

### 🤝 **Collaboration**
- Effective use of Pull Requests
- Good teamwork and communication

---

## 🎯 Final Deliverables Checklist

When you're done, your repository should contain:

✅ **Automated Training Pipeline**
- [x] Prefect workflows for model training
- [x] Separate modules for training and inference
- [x] Reproducible model and encoder generation

✅ **Automated Deployment**
- [x] Prefect deployment for regular retraining

✅ **Production API**
- [x] Working REST API for predictions
- [x] Pydantic input validation
- [x] Docker containerization

✅ **Professional Documentation**
- [x] Updated README with clear instructions
- [x] Complete setup and run instructions
- [x] All TODOs removed from code

---

**Ready to start? Head to branch_0 and read PR_0.md for your first task! 🚀**
