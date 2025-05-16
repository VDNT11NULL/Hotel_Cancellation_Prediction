pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "rugged-alloy-459317-j5"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }
    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github repo to Jenkins.....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Github_MLOps_token', url: 'https://github.com/VDNT11NULL/Hotel_Cancellation_Prediction.git']])
                }
            }
        }
        stage('Setting up virtual env and Installing dependency') {
            steps {
                script {
                    echo 'Setting up venv.....'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
        stage('Building and pushing docker image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp_hotel_pre_ML', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and pushing docker img to GCR..........'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build -t gcr.io/${GCP_PROJECT}/hotel-ml-project:latest .
                        docker push gcr.io/${GCP_PROJECT}/hotel-ml-project:latest
                        '''
                    }
                }
            }
        }
    }
}