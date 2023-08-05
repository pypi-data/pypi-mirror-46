# flask.conf.py

# to encrypt cookie data
# SECRET_KEY = 'makeThisSomethingNonGuessable'  # required
SECRET_KEY = 'this is not secret...'
REMEMBER_COOKIE_NAME = 'scout_remember_me'

# connection details for MongoDB
MONGO_DBNAME = 'scout'                        # required
MONGO_PORT = 27017
MONGO_USERNAME = 'mongoUser'
MONGO_PASSWORD = 'mongoUserPassword'

# connection string for Chanjo coverage database
#SQLALCHEMY_DATABASE_URI = 'mysql://chanjo:CHANJO_PASSWORD@localhost:3306/chanjo'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:aquarius-leap-cork@localhost:3306/chanjo4_demo'


# connection details for LoqusDB MongoDB database
LOQUSDB_SETTINGS = dict(
    database='loqusdb',
    uri=("mongodb://{}:{}@localhost:{}/loqusdb"
         .format(MONGO_USERNAME, MONGO_PASSWORD, MONGO_PORT)),
)

# default chanjo coverage report language: 'sv' or 'en'
REPORT_LANGUAGE = 'sv'

# Google email account to user for sending emails
MAIL_USERNAME = 'paul.anderson@gmail.com'
MAIL_PASSWORD = 'mySecretPassw0rd'
MAIL_SERVER = 'smtp.google.com'

# emails to send error log message to
ADMINS = ['robin.andeer@scilifelab.se']

# enable Google OAuth-based login
#GOOGLE = dict(
#    consumer_key='CLIENT_ID.apps.googleusercontent.com',
#    consumer_secret='CLIENT_SECRET',
#    # Prepend to all (non-absolute) request URLs
#    base_url='https://www.googleapis.com/oauth2/v1/',
#    authorize_url='https://accounts.google.com/o/oauth2/auth',
#    request_token_url=None,
#    request_token_params={
#        'scope': ("https://www.googleapis.com/auth/userinfo.profile "
#                  "https://www.googleapis.com/auth/userinfo.email"),
#    },
#    access_token_url='https://accounts.google.com/o/oauth2/token',
#    access_token_method='POST'
#)

# Use local files for the genome viewer pileup.js
#PILEUP_GENOME = '/path/to/local/pileup_refs/hg19.2bit'
#PILEUP_EXONS = '/path/to/local/pileup_refs/ensGene.bb'


# enable the phenomizer service which links HPO phenotype terms to diseases/genes
PHENOMIZER_USERNAME = 'phenoUser'
PHENOMIZER_PASSWORD = 'phenoPassword'
