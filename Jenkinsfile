node {
    def image_name = "bloodlibrary"
    def image = null

    stage('Checkout') {
        checkout scm
    }

    stage('Build') {
        image = docker.build("${image_name}:${env.BUILD_ID}")
    }

    stage('Deploy'){
        try{
            sh "docker stop ${image_name} && docker rm ${image_name}"
        }catch(Exception e){
            echo e.getMessage()
        }
        withCredentials([string(credentialsId: 'vtes-django-secret-key', variable: 'bloodlibrary_django_secret')]) {
        withCredentials([string(credentialsId: 'vtes-api-db-user', variable: 'dbuser')]) {
        withCredentials([string(credentialsId: 'vtes-api-db-password', variable: 'dbpassword')]) {

            def runArgs = '\
-e "DJANGO_SECRET=$bloodlibrary_django_secret" \
-e "DB_USER=$dbuser" \
-e "DB_PASSWORD=$dbpassword" \
--network DEFAULT \
--ip 172.18.0.4 \
--restart unless-stopped \
--name ' + image_name

            def container = image.run(runArgs)
        }
        }
        }
    }
}



