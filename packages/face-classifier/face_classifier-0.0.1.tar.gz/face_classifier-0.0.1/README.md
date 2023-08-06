# Face-Classification

Face classification is a simple package running on top of face_recognition package which automates the training processes and helps in easily getting the prediction. This could be a helpful addition to developers looking forward to adding the face recognition functionality in their projects.

It uses K-nn algorithm and the model provided by face_recognition which spits out a vector of 128 length. Face classification has setup all the things to train and predict faces with optimum precision.

## Installing

```bash
pip install face_classification
```

## A simple example

```bash
# To train create a directory with images stored in sub directories and the label as the folder name
from face_classification import train_model, FaceClassifier

train_model(train_dir='path_to/directories_containing/sub_folders_with_labels_as_folder_name', 
            model_save_path='path/to/store_model'
)

# Initialize object with path of the saved model in above step
face_classifier = FaceClassifier('path/to/store_model')

# Get the boundings of the faces, their embeddings and the predicted class from any image
boundings, embeddings, predictions = face_classifier(image)
```

# License

Apache License 2
