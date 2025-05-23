pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "rugged-alloy-459317-j5"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }
    stages {
        stage('Check Dir') {
            steps {
                sh 'pwd'
                sh 'ls -la'
                sh 'git status || echo "Not in a git repo"'
            }
        }
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github repo to Jenkins.....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Github_MLOps_token', url: 'https://github.com/VDNT11NULL/Hotel_Cancellation_Prediction.git']])
                }
            }
        }
        stage('Start Docker Daemon') {
            steps {
                script {
                    echo 'Starting Docker daemon for DinD.....'
                    sh '''
                    if ! pgrep dockerd > /dev/null; then
                        sudo dockerd &
                        sleep 5
                    fi
                    '''
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
                        set +e
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker pull python:3.11 || true
                        docker build -t gcr.io/${GCP_PROJECT}/hotel-ml-project:latest .
                        
                        timeout 60 docker push gcr.io/${GCP_PROJECT}/hotel-ml-project:latest
                        EXIT_CODE=$?

                        if [ $EXIT_CODE -eq 124 ]; then
                            echo "[WARNING] Docker push hit timeout (124), but it may have succeeded. Continuing pipeline..."
                        elif [ $EXIT_CODE -ne 0 ]; then
                            echo "[ERROR] Docker push failed with exit code $EXIT_CODE"
                            exit $EXIT_CODE
                        fi
                        '''
                    }
                }
            }
        }
        stage('Deploy to Google Cloud Run'){
            steps{
                withCredentials([file(credentialsId: 'gcp_hotel_pre_ML' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Deploy to Google Cloud Run.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}


                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy hotel-ml-project \
                            --image=gcr.io/${GCP_PROJECT}/hotel-ml-project:latest \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated 
                        '''
                    }
                }
            }
        }
    }
}