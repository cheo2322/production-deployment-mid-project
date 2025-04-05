pipeline {
    agent any
    stages {
        stage('Training Model') {
            steps {
                script {
                    sh '''#!/bin/bash
                    echo "Activating virtual environment..."
                    source $VENV_PATH/bin/activate
                    pip install -r requirements.txt
                    echo "Training model..."
                    python3 models/train_model.py
                    '''
                }
            }
        }
        stage('Unit testing') {
            steps {
                script {
                    sh '''#!/bin/bash
                    echo "Activating virtual environment in Python..."
                    source $VENV_PATH/bin/activate
                    echo "Running unit tests with coverage..."
                    coverage run -m unittest discover tests
                    echo "Generating HTML coverage report..."
                    coverage html -d htmlcov
                    '''
                }
            }
        }

        stage('Archive HTML report') {
            steps {
                archiveArtifacts artifacts: 'htmlcov/**', allowEmptyArchive: true
            }
        }
        stage('Run Docker Container') {
            steps {
                script {
                    sh '''#!/bin/bash
                    echo "Remove existing Docker container..."
                    docker stop final-project || true
                    docker rm final-project || true
                    echo "Building Docker image..."
                    docker build -t flask-app .
                    echo "Running Docker container..."
                    docker run -d -p 5000:5000 --name final-project flask-app
                    docker network connect kafka-network final-project
                    '''
                }
            }
        }
        stage('Testing Model') {
            steps {
                script {
                    sh '''#!/bin/bash
                    echo "Activating virtual environment..."
                    source $VENV_PATH/bin/activate
                    echo "Testing model..."
                    python3 models/test_model.py
                    '''
                }
            }
        }
    }
}