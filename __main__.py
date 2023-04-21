import pulumi
from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import ConfigMap, Service
from pulumi_kubernetes.core.v1 import ServicePortArgs
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from pulumi_kubernetes.core.v1 import VolumeArgs

config_map_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Pulumi Kubernetes Demo</title>
</head>
<body>
    <h1>Hello World, from Pulumi Kubernetes!</h1>
</body>
</html>
'''

config_map = ConfigMap(
    'nginx-index',
    metadata={},
    data={'index.html': config_map_content},
)

deployment = Deployment(
    'nginx-deployment',
    metadata={'name': 'nginx'},
    spec={
        'selector': {'matchLabels': {'app': 'nginx'}},
        'replicas': 2,
        'strategy': { 'type': 'RollingUpdate' },
        'template': {
            'metadata': {'labels': {'app': 'nginx'}},
            'spec': {
                'containers': [{
                    'name': 'nginx',
                    'image': 'nginx',
                    'ports': [{'containerPort': 80}],
                    'resources': {'requests': {
                        'cpu': '100m',
                        'memory': '128Mi',
                    }},
                    "volumeMounts": [{
                        'mountPath': '/usr/share/nginx/html',
                        'name': 'html',
                    }],
                }],
                'volumes': [
                  { 
                    'name': "html", 
                    'configMap': { 'name': config_map.metadata.name } 
                  }
                ],
            },
        },
    },
)


service = Service(
    'nginx-service',
    metadata={'name': 'nginx-service', 'labels': {'app': 'nginx'}},
    spec={
        'selector': {'app': 'nginx'},
        'ports': [ServicePortArgs(port=80, target_port=80)],
        'type': "LoadBalancer",
    },
)

pulumi.export("service_url", service.status.apply(lambda x: x.load_balancer.ingress[0].ip + ":80" if x.load_balancer.ingress != None else ''))
