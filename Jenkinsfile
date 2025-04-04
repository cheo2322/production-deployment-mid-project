pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Setup enviroment') {
            steps {
                sh '''#!/bin/bash
                source D:\\Maestria\\Production\\project\\.venv\\Scripts\\activate
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                sh '''#!/bin/bash
                docker build -t movies-recomendation .
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
