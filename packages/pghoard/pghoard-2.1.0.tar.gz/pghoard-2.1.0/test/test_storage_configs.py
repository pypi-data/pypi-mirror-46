def config_google():
    return {
        "bucket_name": "aiven-test-euw1",
        "credentials": {
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "client_email": "aiven-test-storage-user@ohmu-pgaas.iam.gserviceaccount.com",
            "client_id": "110954886190241628906",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/aiven-test-storage-user%40ohmu-pgaas.iam.gserviceaccount.com",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCfUarzs8QfyPt6\n1+ldRMSCbIECKeEEk+sUHSV9SUBmTApvRi+2t428bX1aEiGcAJjS7ekIAh93BqJQ\n/KdcpGHyhS+Jz3/VvjRWwQuLtIdWHZ0ds8LHrLD3JSFCX5MQUqVyer8iKie1JA/5\ngZTNv6h9p3goXY4be7NfWJ+uxYaGloBc44a7nhckoQtq6XrtLrAkhTiIGCW1MynW\nJNgop5L+jDxuGzEocsFrmPF4k0Uxxn3ztbIyvOiOgr2YkwEc67iDuza5AFGvSx0n\nM8sw97zqBzA5J9nc040WJmy1Q9J1/uPRmeOAym38SvrhDy/cAkk+tK9OEKjBfTdt\nVRAUQLA1AgMBAAECggEASthO+1YEWPpOShOMqihYOP1ITf/mmgPzd+uJZSY4ftZS\nQJw0Zh4tE8xMCzhhWaxeHxltVDnLFlujfXB0H22KJiizgIZeg8drRyZBikwxGB+p\nY/7DDpLuP+zNhyTnLc/lsbZAfIhZRxu99XUOtunG+eDm7e+lhvvB9JTpz200GZ10\nERretDAdXjh82V6Db8BKy3ZxprHdVlkljK7RS24zWyUqvi+z6KTKIMLh1WtXJGvy\n24WerD1EAzsFKnt1YGVt/7BFL1d5bF/XglvFH7mFl4V9O2zAHUvlLyv23UDF5dD8\nAcNLMkcFCpF7RSngCQI7cUOttuvrxoszYSoQwgz8sQKBgQDcPtCsOxDhV/zcf/Gv\nrKfo9w9nTu6JtC66bSDp/mAhvJ5ADTa9ftqyn456XY2DCVF3yzt0hBg1vFt717BR\nVpLwmjcqN7decQeOuIKht8HjeG7jEDd8FhtpKc8jStjiXVUG64veYZ/AWnVSMCyW\nqFpnMjqX3j8QqYdPcn554pRTywKBgQC5Ls/nP5ru+FRElnXXcIXCUt36ORmcd8Rg\nujuGLTXKpgD2IYuqCgqUyZrB7/mDobrGkeglYxxub1BDRVqOSJGJCsG0gMfUYSSP\nLddyv7Ltn6rSH+i4bNn6Y7vY41Hd+0VvyLE3qddeS2enXzCVHr/1k41KeAUw1b++\nTWj63saL/wKBgQCLaKtXSW/u423n+Ih4BVanTLMQVlMBEO8/C9J4qo4Y7LZSnsqW\nedRemkZqSAtJ9Tz/EcJJh093vAlAQ4+UfLM33rWqYGgOPIdnHH17dcAhhtrRmTM1\ntRyWnWNC2J6d8ive3HvFQJAJBnkak+m1V00Z4x5ZgND0cAp5DGToK7ZtrwKBgQC3\n6JO1N2fpOFqIG11A7pEIoj+tx5N130P6RDnlUXUAosiFqF8KKhrEFUxKmscUQUQ6\n/KCusLWFv6rYhEIg2FUg4rvpRZQviaJDR+WWImfSsiV1tRbsQb5hezcNeQTPDkKx\nd4D4pQYssXppsJGRJw7BFx7U/Ek7bKyWlE5UB3brhQKBgQChjCFHSRh6U8fGrJRF\nTLdaXeQZAwSLr4Fjk5zEDhe/Z0mLFHCPeaup3CWg1Kvlz8fD35lkq+AfWko94+lm\neHnWTav1QoMnyoKfmFvbqaJFTOgxw1zenvoLNDIVVKf/IFyIFrYkHXSn5gL2oLt/\npVZqzZZogBRQTirtdyYWywJbEA==\n-----END PRIVATE KEY-----\n",
            "private_key_id": "8206530bd8447ff7b2eeeaa94661323fefe32f5e",
            "project_id": "ohmu-pgaas",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
            "type": "service_account"
        },
        "prefix": "rikonen-test/561372a8-24f6-4095-94b2-f5d19fc99b90/6896820b-d729-40ab-a16f-342b7d55e5b7",
        "project_id": "ohmu-pgaas",
        "storage_type": "google"
    }

def config_aws_s3():
    return {
        "aws_access_key_id": "AKIAJJP7ZVTTVK7DSPFA",
        "aws_secret_access_key": "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",
        "bucket_name": "aiventest-eu-west-2",
        "prefix": "rikonen-test/561372a8-24f6-4095-94b2-f5d19fc99b90/6896820b-d729-40ab-a16f-342b7d55e5b7",
        "region": "eu-west-2",
        "storage_type": "s3"
    }

def config_azure():
    return {
        "account_key": "x3RAF3dG/Fmeqe6DYoKJjXUr6K2F98qdbXn/ylgSTKROpnPozk7/dXPBQ7/uPVytMkk95AKe26NMp/98jfT9bQ==",
        "account_name": "aiventestuksouth",
        "bucket_name": "uksouth",
        "prefix": "rikonen-test/561372a8-24f6-4095-94b2-f5d19fc99b90/6896820b-d729-40ab-a16f-342b7d55e5b7",
        "storage_type": "azure"
    }
