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

SET_CLUSTER = """kubectl config set-cluster {name} --server {url}"""

SET_CREDENTIALS = """kubectl config set-credentials {user} --token {token}"""

SET_CONTEXT = """kubectl config set-context {name} --cluster={name} --user={user}"""

USE_CONTEXT = """kubectl config use-context {name}"""


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
    command = DELETE_NAMESPACE.format(namespace=namespace).strip().split(' ')
    subprocess.call(command)


def deploy_test_env(namespace, registry_url, registry_user, registry_password):
    create_namespace(namespace)
    create_image_pull_secret(namespace, registry_url, registry_user, registry_password)
    deploy_skaffold(namespace)


def get_pod_name(namespace):
    command = GET_POD_NAME.format(namespace=namespace).strip().split(' ')
    output = subprocess.run(command, capture_output=True)
    pod_name = output.stdout.decode('ascii')[4:]
    return pod_name


def execute_tests(namespace):
    pod = get_pod_name(namespace)
    command = EXECUTE_TESTS.format(namespace=namespace,
                                   pod=pod).strip().split(' ')
    subprocess.call(command)


def set_cluster(name, url):
    command = SET_CLUSTER.format(name=name, url=url).strip().split(' ')
    subprocess.call(command)


def set_credentials(user, token):
    command = SET_CREDENTIALS.format(user=user, token=token).strip().split(' ')
    subprocess.call(command)


def set_context(name, user):
    command = SET_CONTEXT.format(name=name, user=user).strip().split(' ')
    subprocess.call(command)


def use_context(name):
    command = USE_CONTEXT.format(name=name).strip().split(' ')
    subprocess.call(command)


def init_kubectl(name, url, user, token):
    set_cluster(name, url)
    set_credentials(user, token)
    set_context(name, user)
    use_context(name)
