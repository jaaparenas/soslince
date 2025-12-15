import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.lincesr.sos',
  appName: 'SOSLince',
  webDir: 'dist',
  server: {
    androidScheme: 'https'
  },
  // 'none' | 'debug' | 'production'
  loggingBehavior: 'debug',
  android: {
    useLegacyBridge: true
  }
};

export default config;
