import logging
from ldap3 import Server, Connection, SIMPLE, SYNC, ASYNC, SUBTREE, ALL
import requests
import start
import time

logger = logging.getLogger(__name__)


class Compared:
    def __init__(self, SERVERNAME, USERNAME, PASSWORD, SEARCH_TREE, ADFILTER, MATRIXSRV, TOKEN):
        self._srvname = SERVERNAME
        self._username = USERNAME
        self._passwd = PASSWORD
        self._tree = SEARCH_TREE
        self._adfilter = ADFILTER
        self._token = TOKEN
        self._matrixsrv = MATRIXSRV
        self.suffix = SUFFIX
        logger.info("Compared: initializing variables...")


    def _requestAD(self):
        resulted = []
        server = Server(self._srvname)
        conn = Connection(server, user=self._username, password=self._passwd)
        conn.bind()

        conn.search(self._tree, self._adfilter, SUBTREE, attributes = ['sAMAccountName'])
        for entry in conn.entries:
            resulted.append(str(entry.sAMAccountName))
        logger.info("Compared: response from Active Directory received...")
        return resulted

    def reqst(self, num):
        TOKEN = self._token
        servername = self._matrixsrv

        endpoint = '/_synapse/admin/v2/users?from={}'.format(num)
        header = {"Authorization": "Bearer {}".format(TOKEN)}
        res = requests.get(servername + endpoint, headers=header)
        ddd = res.json()
        logger.info("Compared: API request completed")
        return ddd


    def _requestMatrix(self):
        num = 0
        resulted = []
        while True:
            logger.info("Compared: Executing an API request for next records")
            users = self.reqst(num)
            for i in users["users"]:
                abc = i["name"].rstrip(":{}".format(self.suffix))
                resulted.append(abc.lstrip("@"))
            logger.info("Page complete")
            if "next_token" in users.keys():
                num = int(users["next_token"])
            else:
                logger.info("Compared: A list of active users has been compiled, total number of active users - {}".format(len(resulted)))
                return resulted


    def resp(self):
        logger.info("Compared: Performing list comparison...")
        list_from_ad = self._requestAD()
        list_from_matrix = self._requestMatrix()
        result = []
        for name in list_from_matrix:
            if name in list_from_ad:
                result.append(name)
        logger.info("Compared: Received a list of users to deactivate, total number of accounts to deactivate - {}".format(len(result)))
        return result

class Deactivate:
    def __init__(self, MATRIXSRV, TOKEN, ACCOUNTS):
        self._srvname = MATRIXSRV
        self._token = TOKEN
        self._acclist = ACCOUNTS
        self.suffix = SUFFIX


    def run(self):
        endpoint = "/_synapse/admin/v1/deactivate/"
        header = {"Authorization": "Bearer {}".format(self._token)}
        username = []
        data = {}
        for fullname in self._acclist:
            username.append("@{}:{}".format(fullname, self.suffix))

        for account in username:
            resp = requests.post(self._srvname + endpoint + account, json=data, headers=header)
            print("Waiting for user to be deactivated - {}".format(account))
            logger.info("---{}--- account has been deactivated".format(account))
            time.sleep(2)




