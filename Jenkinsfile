pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins.....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Github_MLOps_token', url: 'https://github.com/VDNT11NULL/Hotel_Cancellation_Prediction.git']])
                }
            }
        }

        stage('Setting up virtual env and Installing dependency'){
            steps{
                script{
                    echo 'Setting up venv.....'
                    sh '''
                    sudo apt-get update
                    sudo apt-get install -y python3-venv

                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate

                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}