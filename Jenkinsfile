node {
    stage('Checkout') {
        checkout scm
    }

    stage('Stop current service') {
        sh 'docker-compose down --rmi local'
    }

    stage('Deploy'){
        sh 'docker-compose up -d --build --force-recreate'
    }
}



