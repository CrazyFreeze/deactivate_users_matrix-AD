import classes
import logging

logging.basicConfig(level=logging.INFO, filename="script.log", filemode="a", format="%(processName)s %(name)s %(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)



#### VARIABLES ######

SERVERNAME = "" #"DOMAIN CONTROLLER IP-ADDRESS"
USERNAME = "" #"DOMAIN\UserName"
PASSWORD = "" #"Password"
SEARCH_TREE = "" # -> "ou=Отключенные,dc=corp,dc=YOUR_COMPANY_DOMAIN"
ADFILTER = "(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=2))"
MATRIXSRV = "" #URL_MATRIX_SYNAPSE -> "http://IP-ADDRESS:8008"
TOKEN = "" #ACCESS_TOKEN -> "syt_XXXXXXXXXXXXXXXXXXXXX"
SUFFIX = "" #if @user:domain.com your_suffix -> "domain.com"

if __name__ == "__main__":
    logger.info("Start script")
    list_users = classes.Compared(SERVERNAME, USERNAME, PASSWORD, SEARCH_TREE, ADFILTER, MATRIXSRV, TOKEN).resp()
    print(list_users)
    logger.info("Success")
