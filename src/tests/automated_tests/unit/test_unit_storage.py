#
#  Copyright (c) 2019-2021, ETH Zurich. All rights reserved.
#
#  Please, refer to the LICENSE file in the root directory.
#  SPDX-License-Identifier: BSD-3-Clause
#
import pytest
import requests
import os
from test_globals import *
from markers import skipif_not_uses_gateway, skipif_uses_gateway

FIRECREST_URL = os.environ.get("FIRECREST_URL")
USE_GATEWAY  = (os.environ.get("USE_GATEWAY","false").lower() == "true")


if FIRECREST_URL and USE_GATEWAY: 
	STORAGE_URL = os.environ.get("FIRECREST_URL") + "/storage"    
else:
    STORAGE_URL = os.environ.get("F7T_STORAGE_URL")

### SSL parameters
USE_SSL = os.environ.get("F7T_USE_SSL", False)
SSL_CRT = os.environ.get("F7T_SSL_CRT", "")
SSL_PATH = "../../../deploy/test-build"


# test upload request: ask for an upload task (must throw 200 OK)
@skipif_not_uses_gateway
def test_post_upload_request(headers):
    data = { "sourcePath": "testsbatch.sh", "targetPath": USER_HOME }
    resp = requests.post(STORAGE_URL + "/xfer-external/upload", headers=headers, data=data, verify= (f"{SSL_PATH}{SSL_CRT}" if USE_SSL else False))
    assert resp.status_code == 201

@skipif_not_uses_gateway
def test_download_file_not_exist(headers):
    data = { "sourcePath": "no-existing-file" }
    resp = requests.post(STORAGE_URL + "/xfer-external/download", headers=headers, data=data, verify= (f"{SSL_PATH}{SSL_CRT}" if USE_SSL else False)) 
    print(resp.json())  
    print(resp.headers)
    assert resp.status_code == 400

@skipif_not_uses_gateway
def test_download_file_not_allowed(headers):
    data = { "sourcePath": "/srv/f7t/test_sbatch_forbidden.sh" }
    resp = requests.post(STORAGE_URL + "/xfer-external/download", headers=headers, data=data, verify= (f"{SSL_PATH}{SSL_CRT}" if USE_SSL else False)) 
    print(resp.json())  
    print(resp.headers)
    assert resp.status_code == 400

@skipif_not_uses_gateway
def test_download_dir_not_allowed(headers):
    data = { "sourcePath": "/srv/f7t" }
    resp = requests.post(STORAGE_URL + "/xfer-external/download", headers=headers, data=data, verify= (f"{SSL_PATH}{SSL_CRT}" if USE_SSL else False)) 
    print(resp.json())  
    print(resp.headers)
    assert resp.status_code == 400

@skipif_not_uses_gateway
def test_internal_cp(headers):
    # jobName, time, stageOutJobId
    data = {"sourcePath":  "/srv/f7t/test_sbatch.sh", "targetPath": USER_HOME + "/testsbatch2.sh", "account": "test"}
    url = "{}/xfer-internal/cp".format(STORAGE_URL)
    resp = requests.post(url, headers=headers,data=data, verify= (f"{SSL_PATH}{SSL_CRT}" if USE_SSL else False))
    assert resp.status_code == 201

@skipif_not_uses_gateway
def test_internal_mv(headers):    
    # jobName, time, stageOutJobId
    data = {"sourcePath": "/srv/f7t/test_sbatch_mv.sh", "targetPath": USER_HOME + "/testsbatch3.sh"}
    url = "{}/xfer-internal/mv".format(STORAGE_URL)
    resp = requests.post(url, headers=headers,data=data, verify= (f"{SSL_PATH}{SSL_CRT}" if USE_SSL else False))
    assert resp.status_code == 201

@skipif_not_uses_gateway
def test_internal_rsync(headers):
    # jobName, time, stageOutJobId
    data = {"sourcePath": USER_HOME + "/", "targetPath": USER_HOME + "/"}
    url = "{}/xfer-internal/rsync".format(STORAGE_URL)
    resp = requests.post(url, headers=headers,data=data, verify= (f"{SSL_PATH}{SSL_CRT}" if USE_SSL else False))
    assert resp.status_code == 201   

@skipif_not_uses_gateway
def test_internal_rm(headers):
    # jobName, time, stageOutJobId
    data = {"targetPath": "/srv/f7t/test_sbatch_rm.sh"}
    
    url = "{}/xfer-internal/rm".format(STORAGE_URL)
    resp = requests.post(url, headers=headers,data=data, verify= (f"{SSL_PATH}{SSL_CRT}" if USE_SSL else False))
    assert resp.status_code == 201   

@skipif_not_uses_gateway
def test_internal_rm_err(headers):
    # jobName, time, stageOutJobId
    data = {"targetPath": "/srv/f7t/test_sbatch_forbidden.sh"}
    
    url = "{}/xfer-internal/rm".format(STORAGE_URL)
    resp = requests.post(url, headers=headers,data=data, verify= (f"{SSL_PATH}{SSL_CRT}" if USE_SSL else False))
    assert resp.status_code == 400


# Test storage microservice status
@skipif_uses_gateway
def test_status():
	url = "{}/status".format(STORAGE_URL)
	resp = requests.get(url, verify= (f"{SSL_PATH}{SSL_CRT}" if USE_SSL else False))
	assert resp.status_code == 200


if __name__ == '__main__':
	pytest.main()
