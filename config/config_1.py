from fernet import Fernet

TOKEN = "7039472276:AAEcg8LqeuW4gyoDdogVDfbmb_G9tyKihx8"


ip = '45.81.226.118'
PGUSER = 'roman'
PGPASSWORD = '1234'
DATABASE = 'hacaton'

POSTGRES_URL = f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'

SECRET_KEY = b'rHOPsLChNAHn_h4LyqfT6kHMUVcnWur1FPMVh3W1vj4='
crypt = Fernet(SECRET_KEY)