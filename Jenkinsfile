pipeline {
    agent any
    stages {
        stage('Adjust Permissions') {
            steps {
                script {
                    sh '''#!/bin/bash
                    echo "Setting permissions for workspace directory..."
                    sudo chown -R $(whoami) .
                    sudo chmod -R 775 .
                    '''
                }
            }
        }
        stage('Prepare Environment') {
            steps {
                script {
                    sh '''#!/bin/bash
                    echo "Activating virtual environment..."
                    source $VENV_PATH/bin/activate
                    echo "Installing dependencies..."
                    pip install -r requirements.txt
                    '''
                }
            }
        }
        stage('Training Model') {
            steps {
                script {
                    sh '''#!/bin/bash
                    echo "Activating virtual environment..."
                    source $VENV_PATH/bin/activate
                    echo "Training model..."
                    python3 models/train_model.py
                    '''
                }
            }
        }
        stage('Run Docker Container') {
            steps {
                script {
                    sh '''#!/bin/bash
                    echo "Building Docker image..."
                    docker build -t flask-app .
                    echo "Running Docker container..."
                    docker run -d -p 5000:5000 flask-app
                    '''
                }
            }
        }
    }
}