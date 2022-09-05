node {
    stage('Checkout') {
        checkout scm
    }

    stage('Stop current service') {
        sh 'docker-compose down --rmi local'
    }

    stage('Deploy'){
        withCredentials([usernamePassword(credentialsId: 'vtes-statics-credentials', usernameVariable: 'statics-user', passwordVariable: 'statics-password')]) {
            sh "STATICS_USER=${statics-user} STATICS_PASSWORD=${statics-password} docker-compose up -d --build --force-recreate"
        }
    }
}



