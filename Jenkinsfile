pipeline {
    agent any
    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    sh '''#!/bin/bash
                    echo "Setting up the environment..."
                    python3 -m pip install -r requirements.txt
                    '''
                }
            }
        }
        stage('Training Model') {
            steps {
                script {
                    sh '''#!/bin/bash
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
                    docker build -t my-app .
                    docker run -d -p 5000:5000 my-app
                    '''
                }
            }
        }
    }
} 