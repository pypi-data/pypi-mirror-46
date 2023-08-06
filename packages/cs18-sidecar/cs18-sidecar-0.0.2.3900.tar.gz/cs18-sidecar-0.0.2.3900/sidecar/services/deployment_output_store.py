import json
import threading
from abc import ABCMeta, abstractmethod
from logging import Logger

from sidecar.aws_session import AwsSession
from sidecar.aws_status_maintainer import AWSStatusMaintainer
from sidecar.aws_tag_helper import AwsTagHelper
from sidecar.const import Const
from sidecar.services.deployment_output_converter import DeploymentOutputConverter


class DeploymentOutputStore(metaclass=ABCMeta):

    @abstractmethod
    def save_app_output(self, app_name: str, app_instance_id: str, output: str):
        raise NotImplemented()

    @abstractmethod
    def save_service_output(self, service_name: str, output_json: {}):
        raise NotImplemented()


class AwsDeploymentOutputStore(DeploymentOutputStore):
    def __init__(self, logger: Logger,
                 aws_session: AwsSession,
                 status_maintainer: AWSStatusMaintainer):
        self._aws_session = aws_session
        self._status_maintainer = status_maintainer
        self._logger = logger
        self._lock = threading.RLock()

    def save_service_output(self, service_name: str, output_json: {}):
        try:
            converted_output = DeploymentOutputConverter.convert_from_terraform_output(output_json)
            self._logger.info(f"service '{service_name}' deployment output is:\n{converted_output}")
        except Exception as exc:
            output_str = json.dumps(output_json)
            self._logger.exception(f"service '{service_name}' "
                                   f"deployment output is not valid:\n{output_str}")
            raise exc
        with self._lock:
            self._status_maintainer.update_service_output(service_name, converted_output)

    def save_app_output(self, app_name: str, app_instance_id: str, output: str):
        try:
            converted_output = DeploymentOutputConverter.convert_from_configuration_script(output)
            self._logger.info(f"application '{app_instance_id}/{app_name}' deployment output is:\n{converted_output}")
        except Exception as exc:
            self._logger.exception(f"application '{app_instance_id}/{app_name}' "
                                   f"deployment output is not valid:\n{output}")
            raise exc
        instance = self._get_instance_by_id(instance_id=app_instance_id)
        instance_logical_id = AwsTagHelper.wait_for_tag(instance, Const.INSTANCELOGICALID, self._logger)
        with self._lock:
            self._status_maintainer.update_app_instance_output(instance_logical_id,
                                                               app_instance_id,
                                                               app_name,
                                                               converted_output)

    def _get_instance_by_id(self, instance_id: str):
        ec2 = self._aws_session.get_ec2_resource()
        return ec2.Instance(instance_id)
