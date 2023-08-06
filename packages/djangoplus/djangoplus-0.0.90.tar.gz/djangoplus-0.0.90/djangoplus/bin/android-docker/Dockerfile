FROM debian

ENV JAVA_HOME=/usr/lib/jvm/java-8-oracle
ENV ANDROID_HOME=/opt/android
ENV PATH=$ANDROID_HOME/platform-tools:$PATH
ENV PATH=$ANDROID_HOME/tools:$PATH
ENV PATH=/opt/gradle/gradle-5.3.1/bin:$PATH

RUN apt-get -y update
RUN apt-get install -y curl wget unzip software-properties-common
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get install -y nodejs
RUN npm install -g cordova
RUN npm install -g ionic

RUN wget https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip
RUN mkdir $ANDROID_HOME
RUN unzip sdk-tools-linux-4333796.zip -d $ANDROID_HOME

RUN add-apt-repository -y ppa:webupd8team/java
RUN apt-get -y update
RUN yes | apt-get -y --allow-unauthenticated install oracle-java8-installer

RUN wget https://services.gradle.org/distributions/gradle-5.3.1-bin.zip
RUN mkdir /opt/gradle
RUN unzip -d /opt/gradle gradle-5.3.1-bin.zip

RUN yes | $ANDROID_HOME/tools/bin/sdkmanager "build-tools;28.0.3" "platforms;android-28"

RUN yes no | ionic start app blank

RUN cd app && ionic cordova platform add android
RUN cd app && ionic cordova plugin add cordova-plugin-inappbrowser
RUN cd app && npm install @ionic-native/in-app-browser@5.2.0
RUN cd app && cp config.xml config-template.xml
RUN cd app && keytool -genkey -noprompt  -alias djangoplus -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=djangoplus.net, OU=ID, O=DJANGOPLUS, L=Silva, S=Carlos, C=CS" -keystore djangoplus.keystore -storepass 1793ifrn. -keypass 1793ifrn.

ADD build.sh /
RUN chmod +x build.sh

RUN mkdir -p /tmp/releases

RUN /build.sh "/www.google.com" "Google" "brenokcc@yahoo.com.br" "https://cdn4.iconfinder.com/data/icons/new-google-logo-2015/400/new-google-favicon-512.png"



