import pickle
import json
import tensorflow as tf

from keras.models import model_from_json, load_model
from sklearn.externals import joblib


from forecastlib.models.ClassificationModel import ClassificationModel
from forecastlib.models.ForecastModel import ForecastModel


class ModelSerializer(object):

	@staticmethod
	def save_classification_model(model: ClassificationModel, folder: str):
		with open(folder + ModelSerializer.get_model_filename("classification"), 'wb') as outfile:
			pickle.dump(model.model, outfile)

	@staticmethod
	def save_classification_features(model: ClassificationModel, folder: str):
		with open(folder + ModelSerializer.get_feature_filename("classification"), 'w') as outfile:
			json.dump(model.features, outfile)

	@staticmethod
	def save_classification(model: ClassificationModel, folder: str):
		ModelSerializer.save_classification_model(model, folder)
		ModelSerializer.save_classification_features(model, folder)

	@staticmethod
	def save_all(model: ForecastModel, folder: str, name: str):
		ModelSerializer.save_model(model, folder, name)
		ModelSerializer.save_scalers(model, folder, name)
		ModelSerializer.save_features(model, folder, name)

	@staticmethod
	def save_model(model: ForecastModel, path: str, name: str):
		model.model.save(path + ModelSerializer.get_model_filename(name))
		architecture = model.model.to_json()
		with open(path + name + ".arch.json", 'w') as f:
			f.write(architecture)
		model.model.save_weights(path + name + ".weights.h5")

	@staticmethod
	def save_scalers(model: ForecastModel, folder: str, name: str):
		from sklearn.externals import joblib
		joblib.dump(model.feature_scaler, folder + ModelSerializer.get_feature_scaler_filename(name))
		joblib.dump(model.label_scaler, folder + ModelSerializer.get_label_scaler_filename(name))

	@staticmethod
	def save_features(model: ForecastModel, folder: str, name: str):
		with open(folder + ModelSerializer.get_feature_filename(name), 'w') as outfile:
			json.dump(model.features, outfile)

	@staticmethod
	def load_forecast_model(folder: str, name: str, get_file_callback):
		feature_file = get_file_callback(ModelSerializer.get_feature_filename(name), folder)
		model_file = get_file_callback(ModelSerializer.get_model_filename(name), folder)
		model_arch_file = get_file_callback(ModelSerializer.get_model_architecture_filename(name), folder)
		model_weigths_file = get_file_callback(ModelSerializer.get_model_weights_filename(name), folder)
		model_feature_scaler_file = get_file_callback(ModelSerializer.get_feature_scaler_filename(name), folder)
		model_label_scaler_file = get_file_callback(ModelSerializer.get_label_scaler_filename(name), folder)

		with open(feature_file) as json_file:
			features = json.load(json_file)

		with open(model_arch_file) as json_file:
			model = model_from_json(json_file.read())
		model.load_weights(model_weigths_file)
		model._make_predict_function()

		feature_scaler = joblib.load(model_feature_scaler_file)
		label_scaler = joblib.load(model_label_scaler_file)

		return ForecastModel(name, model, feature_scaler, label_scaler, features)

	@staticmethod
	def load_classification_model(folder: str, name: str, get_file_callback):
		feature_file = get_file_callback(ModelSerializer.get_feature_filename(name), folder)
		model_file = get_file_callback(ModelSerializer.get_model_filename(name), folder)

		with open(model_file, "rb") as dump_file:
			model = pickle.load(dump_file)

		with open(feature_file) as json_file:
			features = json.load(json_file)

		return ClassificationModel(model, features)

	@staticmethod
	def get_feature_filename(name):
		return name + ".features.json"

	@staticmethod
	def get_model_filename(name):
		return name + ".model.h5"

	@staticmethod
	def get_model_architecture_filename(name):
		return name + ".arch.json"

	@staticmethod
	def get_model_weights_filename(name):
		return name + ".weights.h5"

	@staticmethod
	def get_feature_scaler_filename(name):
		return name + ".scaler.features"

	@staticmethod
	def get_label_scaler_filename(name):
		return name + ".scaler.label"
