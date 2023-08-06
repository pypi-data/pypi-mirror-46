from podder_task_base.api.task_api_executor import TaskApiExecutor
from protos import pipeline_framework_pb2, pipeline_framework_pb2_grpc


class {{ task_class }}Api(pipeline_framework_pb2_grpc.{{ task_class }}ApiServicer):
    def __init__(self, execution_task):
        self.execution_task = execution_task

    def execute(self, request, context):
        return(TaskApiExecutor(self.execution_task, pipeline_framework_pb2).
            execute(request, context))
