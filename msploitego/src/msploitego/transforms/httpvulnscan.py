from pprint import pprint

from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")
    rep = scriptrunner(port, "http-adobe-coldfusion-apsa1301,http-aspnet-debug,http-axis2-dir-traversal,http-cookie-flags,http-cross-domain-policy,http-dlink-backdoor,http-dombased-xss,http-fileupload-exploiter,http-frontpage-login,http-git,http-huawei-hg5xx-vuln,http-iis-webdav-vuln,http-internal-ip-disclosure,http-jsonp-detection,http-litespeed-sourcecode-download,http-majordomo2-dir-traversal,http-method-tamper,http-phpmyadmin-dir-traversal,http-shellshock,http-slowloris-check,http-sql-injection,http-tplink-dir-traversal,http-trace,http-vmware-path-vuln,http-vuln-cve2006-3392,http-vuln-cve2010-2861,http-vuln-cve2011-3192,http-vuln-cve2011-3368,http-vuln-cve2012-1823,http-vuln-cve2013-0156,http-vuln-cve2013-7091,http-vuln-cve2014-2126,http-vuln-cve2014-2127,http-vuln-cve2014-2128,http-vuln-cve2014-2129,http-vuln-cve2014-8877,http-vuln-cve2015-1427,http-vuln-cve2015-1635,http-vuln-cve2017-1001000,http-vuln-cve2017-5638,http-vuln-cve2017-5689,http-vuln-cve2017-8917,http-vuln-misfortune-cookie,http-vuln-wnr1000-creds", ip, args="-sS -sV")

    if rep.hosts[0].status == "up":
        for res in rep.hosts[0].services[0].scripts_results:
            if res.get("id") == "http-server-header":
                continue
            elements = res.get("elements")
            if elements:
                for cve,d in elements.items():
                    vuln = mt.addEntity("maltego.Vulnerability", cve)
                    vuln.setValue(cve)
                    vuln.addAdditionalFields("details", "Details", False, res.get("output"))
                    for k,v in d.items():
                        if v and v.strip():
                            vuln.addAdditionalFields(k, k.capitalize(), False, v)
            else:
                vid = res.get("id")
                vuln = mt.addEntity("maltego.Vulnerability", vid)
                vuln.setValue(vid)
                vuln.addAdditionalFields("details", "Details", False, res.get("output"))
    else:
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['httpvulnscan.py',
#  'http/80:547',
#  'properties.metasploitservice=http/80:547#info=Apache httpd 2.0.52 (CentOS)#name=http#proto=tcp#service.name=80/Apache 9#port=80#banner=Apache httpd 2.0.52 (CentOS)#properties.service= #ip=10.11.1.10#created_at=24/2/2018#updated_at=24/2/2018#id=6950#state=open#address=10.11.1.8#host_id=547#user=msf#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=#db=msf']
# dotransform(args)
