

class ForecastModel(object):
	def __init__(self, name, model, feature_scaler, label_scaler, features):
		self.name = name
		self.features = features
		self.feature_scaler = feature_scaler
		self.label_scaler = label_scaler
		self.model = model

	def predict(self, x):
		x_featured = x[self.features].copy()
		x_scaled = self.feature_scaler.transform(x_featured)
		print(x_scaled)
		y_scaled = self.model.predict(x_scaled)
		return self.label_scaler.inverse_transform(y_scaled.reshape(-1, 1))

