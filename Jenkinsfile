pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Setup') {
            steps {
                sh '''#!/bin/bash
                source /var/jenkins_home/.venv/bin/activate
                python --version
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }
        stage('Training') {
            steps {
                sh '''#!/bin/bash
                source /var/jenkins_home/.venv/bin/activate
                pwd
                python models/train_models.py
                '''
            }
        }
    }
}
