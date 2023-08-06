#!/usr/bin/env bash

export JAVA_HOME=/usr/lib/jvm/java-8-oracle
export ANDROID_HOME=/opt/android
export PATH=$ANDROID_HOME/platform-tools:$PATH
export PATH=$ANDROID_HOME/tools:$PATH
export PATH=/opt/gradle/gradle-5.3.1/bin:$PATH

cd /app
cp config-template.xml config.xml

printf "import { Component } from '@angular/core';
import { InAppBrowser } from '@ionic-native/in-app-browser/ngx';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
 constructor(private iab: InAppBrowser) {
 const browser = this.iab.create('https://$1', '_self', 'location=no,toolbar=no');
 }
}
" > src/app/home/home.page.ts

printf "" > src/app/home/home.page.html

sed -i '14i\    <allow-navigation href="*" />' config.xml
sed -i "s/io.ionic.starter/$1/g" config.xml
sed -i "s/MyApp/$2/g" config.xml
sed -i "s/hi@ionicframework/$3/g" config.xml
sed -i "s/Ionic Framework Team/$3/g" config.xml
sed -i "s/ionicframework.com/$1/g" config.xml
sed -i "s/value=\"screen\"/value=\"none\"/g" config.xml
rm -f icon.png
wget $4 -O icon.png
cp icon.png resources/android/icon/drawable-hdpi-icon.png
cp icon.png resources/android/icon/drawable-mdpi-icon.png
cp icon.png resources/android/icon/drawable-xxhdpi-icon.png
cp icon.png resources/android/icon/drawable-ldpi-icon.png
cp icon.png resources/android/icon/drawable-xhdpi-icon.png
cp icon.png resources/android/icon/drawable-xxxhdpi-icon.png

rm -f template.apk
ionic cordova build android --release
mv platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk app-release-unsigned.apk
jarsigner -keystore djangoplus.keystore -storepass 1793ifrn. app-release-unsigned.apk djangoplus
/opt/android/build-tools/28.0.3/zipalign -v 4 app-release-unsigned.apk template.apk
rm -f app-release-unsigned.apk
mkdir -p /tmp/releases
mv template.apk /tmp/releases/$1.apk

