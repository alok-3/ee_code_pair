pipeline {
    agent any
    
    environment {
        SONARQUBE_URL = 'http://localhost:9000'
        SCANNER_HOME = tool 'sonar-scanner'
        SONARQUBE_CREDENTIALS = 'sonarqube-token'
        DOCKER_IMAGE = 'github-gists-api:${BUILD_ID}'
        //KUBECONFIG = credentials('minikube')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'solution', credentialsId: 'Github', url: 'https://github.com/alok-3/equal-experts-academic-friendly-gorgeous-memory-c5d1e69ffc31.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "[DEBUG] Jenkins Build ID: ${BUILD_ID}" && \
                    echo "Installing dependencies..." && \
                    python3 -m venv /opt/venv && \
                    /opt/venv/bin/pip install -r requirements.txt
                    '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    echo "Running unit tests..." && \
                    PYTHONPATH=.:$PYTHONPATH pytest -v --junitxml=report.xml && \
                    coverage run -m pytest tests/test_*.py --junit-xml=target/test-results/report.xml && \
                    coverage xml -i  
                    '''
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }
        
        // stage('Static Code Analysis') {
        //     steps {
        //         withSonarQubeEnv(credentialsId: SONARQUBE_CREDENTIALS) {
        //             echo 'Running SonarQube Scanner...'
        //             sh 'sonar-scanner -Dsonar.projectKey=github-gists-api -Dsonar.sources=.'
        //         }
        //     }
        // }
        
        // stage('Quality Gate Check') {
        //     steps {
        //         timeout(time: 5, unit: 'MINUTES') {
        //             echo 'Waiting for SonarQube Quality Gate to complete...'
        //             waitForQualityGate abortPipeline: true
        //         }
        //     }
        // }
        
        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker image..." && \
                    docker build -t github-gists-api:${BUILD_ID} .
                '''
            }
        }
        
        stage('Scan Image with Trivy') {
            steps {
                sh 'echo "Scanning for High and Critical Vulnerabilities" && trivy image --severity HIGH,CRITICAL github-gists-api:${BUILD_ID}' // --exit-code 1
            }
        }
        
        stage('Check Cluster Info') {
            steps {
                withCredentials([file(credentialsId: 'working', variable: 'KUBECONFIG')]) {
                    sh '''
                        echo "Checking cluster info..." && \
                        kubectl cluster-info && \
                        kubectl get nodes
                    '''
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'working', variable: 'KUBECONFIG')]) {
                    sh '''
                        echo "Deploying to Kubernetes..." && \
                        export IMAGE_TAG=${BUILD_ID} && \
                        envsubst < k8s/deployment.yaml | kubectl apply -f - && \
                        kubectl apply -f k8s/service.yaml
                    '''
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                withCredentials([file(credentialsId: 'working', variable: 'KUBECONFIG')]) {
                    sh '''
                        echo "Verifying deployment..." && \
                        kubectl get pods && \
                        kubectl get svc
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
