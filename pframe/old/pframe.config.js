module.exports = {
    server: {
                port: 8081,
                logname: '/tmp/bbm360gui.log'
            },
    auth: {
                develmode: true,     // if true, does not use TLS/SSH
                sslkey: '/Users/tristan/vmshared/nevrokey.pem',
                sslcert: '/Users/tristan/vmshared/nevrocert.pem',
                logins: ['foo|bar', 'fred|derf', 'user|password']
          },
    apis: {
             bbm360apiurl: "https://nevroserver/bbm360apiapp/bbm360api/",
             bbm360apirequestkey: 'insertgoodrequestkeyhere'
          },
    testing: {
        baseUrl: "https://localhost:8081/",
        dbHostname: '',
        dbPort: '5432',
        dbName: 'bbmdb',
        dbUser: 'bbmanager',
        dbPassword: 'foobar',
        syncDbHostname: '',
        syncDbPort: '5432',
        syncDbName: 'syncdb',
        syncDbUser: 'syncmanager',
        syncDbPassword: 'foobar',
        testSyncServerName: 'tristantestsync1',
        testSyncServerId: 1,
        uploadFileDirectory: '/mnt/hgfs/vmshared/', // directory where serial number files will live
        testDataDirectory: '/home/tristan/websites/nevroserver/bbm360gui/tests/functional/data/', // directory where test data files live
    }
}
