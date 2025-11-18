pipeline {
    agent any
    
    environment {
        PYTHON = "/usr/bin/python3"
        VENV_DIR = "venv"
    }
    
    stages {

        stage('Checkout Code') {
            steps {
                echo "Fetching latest code from Git..."
                checkout scm
            }
        }
        
        stage('Setup Python Environment and run Suite') {
            steps {
                echo "Creating virtual environment..."
                sh """
                    ${PYTHON} -m venv ${VENV_DIR}
                    call venv\\Scripts\\activate
                    ${PYTHON} -m pip install
                    pip install -r requirements.txt
                    pytest --alluredir=reports
                """
            }
        }

    }
    
    post {
        success {
            echo "🎉 Pytest suite completed successfully!"
        }
        failure {
            echo "❌ Pytest suite failed. Check the logs and reports for details."
        }
    }
}
