import os
import logging
from .kubesubmitmixin import SubmitToKubeMixin
from .kubespecmixin import KubeSpecMixin

log = logging.getLogger(__name__)

class KubernetesDirectJobBackend(SubmitToKubeMixin,KubeSpecMixin):
    def __init__(self,**kwargs):
        SubmitToKubeMixin.__init__(self, **kwargs)
        KubeSpecMixin.__init__(self,**kwargs)

        self.base = os.path.realpath(kwargs.get(
            'path_base',
            os.environ.get('YADAGE_K8S_PATHBASE',os.getcwd())
        ))+'/'
        self.claim_name =  kwargs.get('claim_name','yadagedata')

    def state_mounts_and_vols(self, jobspec):
        container_mounts_state, volumes_state = [],[]
        for i,ro in enumerate(jobspec['state']['readonly']):
            subpath = ro['path'].replace(self.base,'')   
            ctrmnt = {"name": "state", "mountPath": ro['path'], "subPath": subpath}
            container_mounts_state.append(ctrmnt)

        for i,rw in enumerate(jobspec['state']['readwrite']):
            subpath = rw['path'].replace(self.base,'')   
            ctrmnt = {"name": "state", "mountPath": rw['path'], "subPath": subpath}
            container_mounts_state.append(ctrmnt)

        volumes_state.append({
            "name": "state",
            "persistentVolumeClaim": {
                "claimName": self.claim_name,
                "readOnly": False
            }
        })
        return container_mounts_state, volumes_state

    def proxy_data(self, job_uuid, kube_resources):
        jobname = "{}-job-{}".format(self.resource_prefix, job_uuid)
        return {
            'job_id': jobname,
            'resources': kube_resources
        }

    def config(self, job_uuid, jobspec):
        return [], [], []
