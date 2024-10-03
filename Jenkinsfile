node {
    stage('Checkout') {
        checkout scm
    }

    stage('Stop current service') {
        sh 'docker compose down --rmi local'
    }

    stage('Deploy'){
        withCredentials([usernamePassword(credentialsId: 'vtes-statics-credentials', usernameVariable: 'staticsuser', passwordVariable: 'staticspassword')]) {
            withCredentials([string(credentialsId: 'vtes-private-cards', variable: 'pcards')]) {
                sh "STATICS_USER=${staticsuser} STATICS_PASSWORD=${staticspassword} docker compose up -d --build --force-recreate"
            }
        }
    }
}
