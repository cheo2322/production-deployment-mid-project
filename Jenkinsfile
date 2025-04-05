pipeline {
    agent any
    stages {
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
        stage('Unit testing') {
            steps {
                script {
                    sh '''#!/bin/bash
                    echo "Activating virtual environment..."
                    source $VENV_PATH/bin/activate
                    echo "Running unit tests with coverage..."
                    coverage run -m unittest discover tests
                    echo "Generating coverage report..."
                    coverage xml -o coverage.xml
                    '''
                }
            }
        }

        stage('Publish coverage report') {
            steps {
                coverageTool reportFile: 'coverage.xml'
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