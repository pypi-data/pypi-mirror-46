import re
import time
import getpass
from sts_auth import stsauth
from sts_auth import utils

from sts_auth.stsauth import STSAuth
from sts_auth.okta import Okta
from bs4 import BeautifulSoup
from collections import defaultdict, OrderedDict

sts_auth = STSAuth(
    username='s103151',
    password=getpass.getpass(),
    credentialsfile='~/.aws/credentials',
    okta_org='bbva-us'
)
sts_auth.parse_config_file()
response = sts_auth.session.get(sts_auth.idpentryurl)
response.soup = BeautifulSoup(response.text, "lxml")
assertion_pattern = re.compile(r'name=\"SAMLResponse\" value=\"(.*)\"\s*/><noscript>')
# response_assertion = re.search(assertion_pattern, response.text)


# login_form = response.soup.find(id='loginForm')
# okta_login = response.soup.find(id='okta-login-container')

form_response = sts_auth.authenticate_to_adfs_portal(response)
# form_response.soup = BeautifulSoup(form_response.text, "lxml")

# form_login_form = form_response.soup.find(id='loginForm')
# form_okta_login = form_response.soup.find(id='okta-login-container')

state_token = utils.get_state_token_from_response(form_response)

okta_client = Okta(
    session=sts_auth.session,
    okta_org=sts_auth.okta_org,
    okta_shared_secret=sts_auth.okta_shared_secret,
    state_token=state_token
)

okta_response = okta_client.handle_okta_verification(form_response)
okta_response.soup = BeautifulSoup(okta_response.text, "lxml")
# okta_assertion = re.search(assertion_pattern, okta_response.text)

hiddenform = okta_response.soup.find('form', {'name': 'hiddenform'})
headers = {'Referer': okta_response.url, 'Content-Type': 'application/x-www-form-urlencoded'}
selectors = ",".join("{}[name]".format(i) for i in ("input", "button", "textarea", "select"))
data = [(tag.get('name'), tag.get('value')) for tag in hiddenform.select(selectors)]
adfs_response = okta_client.session.post(hiddenform.attrs.get('action'), data=data, headers=headers)
adfs_response.soup = BeautifulSoup(adfs_response.text, "lxml")
accts = [acct.contents[0] for acct in adfs_response.soup.find_all('div', {'class': 'saml-account-name'})]
acct_map = {}
for acct in accts:
    acct_map[acct.split(' ')[2].strip('()')] = acct.split(' ')[1]
