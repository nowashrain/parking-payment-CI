pipeline {
    agent any

    environment {
        DOCKER_IMAGE_OWNER = 'ashashrain'
        DOCKER_BUILD_TAG = "v${env.BUILD_NUMBER}"
        DOCKER_PWD = credentials('dockerhub')
        GIT_CREDENTIALS = credentials('github_token')  
        REPO_URL = 'gongbu22/project-parking-CD'
        COMMIT_MESSAGE = 'Update README.md via Jenkins Pipeline'
    }

    stages {
        stage('clone from SCM') {
            steps {
                sh '''
                rm -rf parking-payment-CI
                git clone https://github.com/nowashrain/parking-payment-CI.git
                '''
            }
        }

        stage('Docker Image Building') {
            steps {
                dir('parking-payment-CI'){
                sh '''
                ls -l 
                ls -l ./arm64-payment-service 
                docker build --platform linux/arm64 -t ${DOCKER_IMAGE_OWNER}/arm64-payment-service:latest -t ${DOCKER_IMAGE_OWNER}/arm64-payment-service:${DOCKER_BUILD_TAG} ./arm64-payment-service
                docker tag ${DOCKER_IMAGE_OWNER}/arm64-payment-service:latest ${DOCKER_IMAGE_OWNER}/arm64-payment-service:${DOCKER_BUILD_TAG}
                '''
                }
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USR', passwordVariable: 'DOCKER_PWD')]) {
                sh "echo $DOCKER_PWD | docker login -u $DOCKER_USR --password-stdin"}
            }
        }

        stage('Docker Image pushing') {
            steps {
                sh '''
                docker push ${DOCKER_IMAGE_OWNER}/arm64-payment-service:${DOCKER_BUILD_TAG}
                docker push ${DOCKER_IMAGE_OWNER}/arm64-payment-service:latest
                '''
            }
        }

        stage('Docker Logout') {
            steps {
                sh '''
                docker logout
                '''
            }
        }

        stage('Clone Repository') {
            steps {
                sh '''
                rm -rf project-parking-CD
                git clone https://github.com/${REPO_URL}.git
                '''
            }
        }

        stage('Modify README.md') {
            steps {
                sh """
                    cd project-parking-CD
                    echo "# Updated README" > README.md
                    echo "This README was updated by Jenkins Build #${env.BUILD_NUMBER} on \$(date)" >> README.md
                """
            }
        }

        stage('Commit Changes') {
            steps {
                dir('project-parking-CD') {
                sh '''
                    git config user.name "nowashrain"
                    git config user.email "rltkanth@gmail.com"
                    git add README.md
                    git commit -m "${COMMIT_MESSAGE}"
                '''
                }
            }
        }

        stage('Push Changes') {
            steps {
                dir('project-parking-CD') {
                sh '''
                    git push https://${GIT_CREDENTIALS_USR}:${GIT_CREDENTIALS_PSW}@github.com/${REPO_URL}.git main
                '''
                }
            }
        }
    }
}
