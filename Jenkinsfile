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
                deactivate
                '''
            }
        }
        stage('Training') {
            steps {
                sh '''#!/bin/bash
                source /var/jenkins_home/.venv/bin/activate
                python models/train_model.py
                deactivate
                '''
            }
        }
        stage('Testing') {
            steps {
                sh '''#!/bin/bash
                source /var/jenkins_home/.venv/bin/activate
                python models/test_model.py
                deactivate
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''#!/bin/bash
                source /var/jenkins_home/.venv/bin/activate
                python app/app.py
                deactivate
                '''
            }
        }
    }
}
