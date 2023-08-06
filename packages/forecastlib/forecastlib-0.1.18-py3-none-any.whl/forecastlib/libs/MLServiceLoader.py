from azureml.core.model import Model

class MLServiceLoader(object):


	def bind_to_workspace(self, subsciption_name:str, resource_group_name: str, service_name: str):
		self.subscription_name = subsciption_name
		self.resource_group_name = resource_group_name
		self.service_name = service_name

	def download(self, model_name: str):
		Model.