import subprocess

CREATE_NAMESPACE = """kubectl create namespace {namespace}"""

CREATE_IMAGE_PULL_SECRET = """
kubectl create --namespace {namespace} secret docker-registry registry-secret \
--docker-server={url} \
--docker-username={user} \
--docker-password={password}
"""

DEPLOY_SKAFFOLD = """skaffold deploy --namespace {namespace}"""

EXECUTE_TESTS = """kubectl exec --namespace {namespace} {pod} -- /scripts/test"""

DELETE_NAMESPACE = """kubectl delete namespaces {namespace}"""

GET_POD_NAME = """kubectl --namespace {namespace} get pods -l app.kubernetes.io/component=app -o name"""


def create_namespace(namespace):
    command = CREATE_NAMESPACE.format(namespace=namespace).strip().split(' ')
    subprocess.call(command)


def create_image_pull_secret(namespace, url, user, password):
    command = CREATE_IMAGE_PULL_SECRET.format(namespace=namespace,
                                              url=url,
                                              user=user,
                                              password=password).strip().split(' ')
    subprocess.call(command)


def deploy_skaffold(namespace):
    command = DEPLOY_SKAFFOLD.format(namespace=namespace).strip().split(' ')
    subprocess.call(command)


def cleanup_test_env(namespace):
    command = DELETE_NAMESPACE.format(namespace=namespace)
    subprocess.call(command)


def deploy_test_env(namespace, registry_url, registry_user, registry_password):
    create_namespace(namespace)
    create_image_pull_secret(namespace, registry_url, registry_user, registry_password)
    deploy_skaffold(namespace)


def get_pod_name(namespace):
    command = GET_POD_NAME.format(namespace=namespace)
    output = subprocess.run(command, capture_output=True)
    pod_name = output.stdout.decode('ascii')[4:]
    return pod_name


def execute_tests(namespace):
    pod = get_pod_name(namespace)
    command = EXECUTE_TESTS.format(namespace=namespace,
                                   pod=pod)
    subprocess.call(command)
