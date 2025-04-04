pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Setup and Run') {
            steps {
                sh '''#!/bin/bash
                source /var/jenkins_home/.venv/bin/activate
                python --version
                '''
            }
        }
        stage('Run Docker Container') {
            steps {
                script {
                    sh 'docker stop movies-recomendation-container || true && docker rm movies-recomendation-container || true'
                    
                    sh 'docker run --name movies-recomendation-container -d movies-recomendation'
                }
            }
        }
    }
}
