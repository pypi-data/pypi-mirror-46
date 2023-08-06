import pickle

from face_recognition import face_locations, face_encodings

class FaceClassifier:
    """
    Face recognition model to predict the faces in the images passes to it and return the predicted face"s location,
    the face embedding and the predicted class.

    Parameters
    -----------
    model_path : string
        The location of the trained model"s pickle file.
        Training can be done from train_model module of this package which requires location to store the pickle file.
    
    threshold_value : float, optional
        Show prediction only if the distance between the nearest point to the predicted embedding of image is less than the threshold_value.
        0.4 is default as it works well in most of the cases and is better for precision.
    """
    
    def __init__(self, model_path, threshold_value=0.4):
        """
        Initialising parameters to the class.
        """
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        self.threshold_value = threshold_value


    def get_face_boundings(self, img):
        """ 
        Returns the face boundings from image.

        Parameters
        ----------

        img : float array of image of 3 channel
            The image should be in RGB format and the pixels value between 0 and 1.

        Returns
        -------

        face_boundings : array of shape [n, 4] where n is the number of faces in the image
            The face boundings is returned in (y1, x2, y2, x1) format where (x1, y1) is the top left point of the box 
            and (x2, y2) is the botton left corner of the box.
        """

        face_boundings = face_locations(img)

        return face_boundings


    def get_face_embeddings(self, img, bounding_boxes):
        """ 
        Returns the encoding from the image and face location.

        Parameters
        ----------

        img : float array of image of 3 channel
            The image should be in RGB format and the pixels value between 0 and 1.
        
        bounding_boxes : array of size [n, 4] where n is the number of faces
            Location of the faces returned from the get_face_boudings function.

        Returns
        -------

        embeddings : array of size [n, 128] where n is the number of faces
            The face embeddings from cropped faces ina image.
        """

        embeddings = face_encodings(img, known_face_locations=bounding_boxes)

        return embeddings

    def classify_face(self, embeddings):
        """ 
        Classify whose face it is from the face embeddings.

        Parameters
        ----------

        embeddings : array of size [n, 128] where n is the number of faces

        Returns
        -------

        predictions : array
            The prediction of the faces.     
        """
        
        closest_distances = self.model.kneighbors(embeddings, n_neighbors=1)
        matches = [closest_distances[0][i][0] <= self.threshold_value for i in range(len(embeddings))]
        predictions = [pred if rec else 'unknown' for pred, rec in zip(self.model.predict(embeddings), matches)]

        return predictions


    def predict(self, img):
        """
        Returns the boundings, embeddings and the predicted classes of the faces in the image passed to it.
        
        Parameters
        ----------

        img : float array of image of 3 channel
            The image should be in RGB format and the pixels value between 0 and 1.

        Returns
        -------

        boundings : array of shape [n, 4] where n is the number of faces in the image
            The face boundings is returned in (y1, x2, y2, x1)
        
        embeddings : array of size [n, 128] where n is the number of faces
            The face embeddings from cropped faces in the image.

        predictions : array
            The prediction of the faces. 
        """

        boundings = self.get_face_boundings(img)
    
        if len(boundings) != 0:            
            embeddings = self.get_face_embeddings(img, boundings)
            predictions = self.classify_face(embeddings)
        else:
            boundings = None
            embeddings = None
            predictions = None
        
        return boundings, embeddings, predictions
