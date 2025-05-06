pipeline {
    agent any
    environment {
        VENV_DIR = '605venv'
        DOCKERHUB_CREDENTIAL_ID = '605-dockerhub'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'sampreeth08/605-mlops-app'
    }
    
    stages {
        stage('Cloning from Github Repo') {
            steps {
                script {
                    echo 'Cloning from Github Repo...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: '605-github-token', url: 'https://github.com/Sampreeth-08/605-project.git']])
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    echo 'Setup Virtual Environment...'
                    sh '''
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }

        stage('Linting Code') {
            steps {
                script {
                    echo 'Linting Code...'
                    sh '''
                        set -e
                        . ${VENV_DIR}/bin/activate
                        pylint application.py main.py --output=pylint-report.txt --exit-zero || echo "Pylint stage completed"
                        flake8 application.py main.py --ignore=E501,E302 --output=flake8-report.txt --exit-zero || echo "Flake8 stage completed"
                        black application.py main.py || echo "Black stage completed"
                    '''
                }
            }
        }

        stage('Trivy Scanning') {
            steps {
                script {
                    echo 'Trivy Scanning...'
                    sh "trivy fs ./ --format table -o trivy-fs-report.html"
                }
            }
        }

        stage('Building Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")
                }
            }
        }

        stage('Scanning Docker Image') {
            steps {
                script {
                    echo 'Scanning Docker Image...'
                    sh "trivy image ${DOCKERHUB_REPOSITORY}:latest --format table -o trivy-image-scan-report.html"
                }
            }
        }

        stage('Pushing Docker Image') {
            steps {
                script {
                    echo 'Pushing Docker Image...'
                    docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKERHUB_CREDENTIAL_ID}") {
                        dockerImage.push("latest")
                    }
                }
            }
        }

        // stage('AWS Deployment') {
        //     steps {
        //         script {
        //             echo 'AWS Deployment...'
        //             sh "aws ecs update-service --cluster 605-project-ecs --service 605_ecs_task-service --force-new-deployment"
        //         }
        //     }
        // }

        stage('AWS Deployment') {
    environment {
        AWS_DEFAULT_REGION = 'us-east-1' // or your region
    }


    steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: '605-aws-cred']]) {
            script {
                echo 'AWS Deployment........'
                sh '''
                    aws ecs update-service --cluster 605-project-ecs --service 605_ecs_task-service --force-new-deployment
                '''
            }
        }
    }
}


    }
}