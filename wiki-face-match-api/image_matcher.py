import numpy as np

class ImageMatcher:
    def __init__(self, representation_store):
        self.representation_store = representation_store

    def get_top_faces_matches(self,image_rep, top_limit=3):
        top_limit = top_limit if top_limit<10 else 10

        distances = []

        for img_id,curr_rep in self.representation_store.get_representations().items():
            distance = self.calculate_similarity_distance(image_rep,curr_rep)
            distances.append((img_id, distance))

        distances.sort(key=lambda tup: tup[1])
        distances = distances[:top_limit]

        return distances

    def calculate_similarity_distance(self, rep1, rep2):
        d = rep1 - rep2
        return np.dot(d, d)
