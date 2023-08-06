# --------------------------------------------------------------------
# CMS REST-API - Configuration
# --------------------------------------------------------------------

from ec4sap import config

# --------------------------------------------------------------------
class CMS_ENV:

    def __init__(self, url, auth=None, token=None, wfuser=[]):
        self.api_url = url
        self.basic_auth = auth
        self.oidb_token = token
        self.wfuser = wfuser

# --------------------------------------------------------------------
CMS_INT = CMS_ENV(url=config.CFG_CMS_URL_INT, auth=("sapmgmt\SA-Int-elwistester","xlnsHDsJ7vj9zpuxH6Gl"), wfuser=config.CFG_CMS_WFUSER_INT)
xCMS_INT = CMS_ENV(url=config.CFG_CMS_URL_PRD, auth=("TMZINTRA\SA-PF03-elwistester","2kR3xR4fY9qX5"), wfuser=config.CFG_CMS_WFUSER_PRD)
xCMS_INT = CMS_ENV(url=config.CFG_CMS_URL_PRD, auth=("TMZINTRA\SA-PF03-reporting","w3JmcXLQtNArTvdH"), wfuser=config.CFG_CMS_WFUSER_PRD)

