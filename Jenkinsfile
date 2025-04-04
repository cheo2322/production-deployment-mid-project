pipeline {
    agent any
    stages {
        stage('Verify Docker') {
            steps {
                script {
                    sh 'docker version'
                }
            }
        }
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t movies-recomendation .'
                }
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
    post {
        always {
            script {
                sh 'docker system prune -f || true'
            }
        }
    }
}