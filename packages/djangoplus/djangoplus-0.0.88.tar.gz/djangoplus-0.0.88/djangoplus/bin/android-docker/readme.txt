docker build . -t android-sdk
docker run -v /tmp/releases:/tmp/releases android-sdk /bin/bash build.sh "educ.ifrn.edu.br" "Educ" "brenokcc@yahoo.com.br" "https://media.cdnandroid.com/5c/48/2f/70/37/imagen-slack-0thumb.jpg"
docker run -v /tmp/releases:/tmp/releases android-sdk /bin/bash build.sh simop.analisarn.com.br SiMOP brenokcc@yahoo.com.br https://digipro.analisarn.com.br/media/config/logo_z34kWcT.png
