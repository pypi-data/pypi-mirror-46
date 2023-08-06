# mlcollect

#HDF5 Data
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
labels = le.fit_transform(labels)

dataset = HDF5DatasetWriter((len(imagePaths), 512 * 7 * 7), args["output"], dataKey="features", bufSize=args["buffer_size"])
dataset.storeClassLabels(le.classes_)

batchImages = np.vstack(batchImages)
features = model.predict(batchImages, batch_size=bs)
features = features.reshape((features.shape[0], 512 * 7 * 7))
dataset.add(features, batchLabels)
