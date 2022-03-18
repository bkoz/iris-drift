import os
import numpy as np
import logging
import time
import requests
import random
import subprocess

def predict():
    """
    Make a requests to an Iris model hosted by a Seldon deployment via REST.
    """
    logging.basicConfig(level=logging.INFO)

    #
    # Get the IP of the Kube cluster.
    #
    os.environ["KUBECONFIG"] = ".kubeconfig"
    cmd = ["kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}'"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    hostname = out.decode()
    logging.info(f'CLUSTER_IP: {out.decode()}')

    #
    # Endpoint format: http://{hostname}/seldon/{namespace}/{deployment-name}/api/v0.1/predictions
    #
    url = f'http://{hostname}/seldon/seldon/iris-01/api/v0.1/predictions'
    
    #
    # Build the Iris request payload.
    #
    n_requests = 50
    a = []
    for i in range(n_requests):
        n1 = random.uniform(4.8, 6.8)
        n2 = random.uniform(1.5, 2.8)
        n3 = random.uniform(1.5, 4.8)
        n4 = random.uniform(0.5, 1.5)
        a.append([n1, n2, n3, n4])

    payload = {"data": {"names":["Sepal length","Sepal width","Petal length","Petal Width"], "ndarray": a}}
    logging.debug(f'payload = {payload}')

    logging.info(f'Serializing and predicting via REST at URL: {url}')

    try:
        t0 = time.time()
        r = requests.post(url, json = payload, timeout = 20)
    except requests.exceptions.ConnectionError:
        logging.info(f'REST connection error!')
        return None
    
    logging.debug(f'response: {r}')
    j = r.json()['data']['ndarray'][0]
    logging.info(f'Example response data = {j}, elapsed time = {time.time() - t0:.1f}s')

    pass

predict()