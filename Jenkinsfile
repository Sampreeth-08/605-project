pipeline {
    agent any
    
    stages {
        stage('Cloning from Github Repo') {
            steps {
                script {
                    echo 'Cloning from Github Repo...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: '605-github-token', url: 'https://github.com/Sampreeth-08/605-project.git']])
                }
            }
        }
    }
}