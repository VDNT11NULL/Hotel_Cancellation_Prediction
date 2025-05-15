pipeline{
    agent any

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins.....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Github_MLOps_token', url: 'https://github.com/VDNT11NULL/Hotel_Cancellation_Prediction.git']])
                }
            }
        }
    }
}