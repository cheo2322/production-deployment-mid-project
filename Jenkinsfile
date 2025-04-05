pipeline {
    agent any
    stages {
        stage('Release Port') {
            steps {
                script {
                    sh '''#!/bin/bash
                    echo "Checking if port 5000 is in use..."
                    if lsof -i :5000; then
                        echo "Stopping process using port 5000..."
                        kill -9 $(lsof -t -i :5000)
                    fi
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
                    docker run -d -p 5000:5000 flask-app final-project
                    '''
                }
            }
        }
    }
}