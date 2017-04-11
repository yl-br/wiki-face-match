import numpy as np
import os
import cv2

class RepresentationStore:
    def __init__(self, image_parser):
        self.image_parser = image_parser
        self.representations = {}


    def calculate_representations(self, wiki_meta_df, images_dir_path):
        out_reps = {}

        count = 0
        for index, row in wiki_meta_df.iterrows():
            count+=1
            img_id = row['full_path']
            relative_path = row['full_path']
            img_path = os.path.join(images_dir_path,relative_path)
            print('\n\n{} / {} - {}% : {}:'.format(count, len(wiki_meta_df.index), int(count * 100 / len(wiki_meta_df.index)), img_path))
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            bounding_box = self.image_parser.get_face_bounding_box(rgb_img)
            if(bounding_box):
                rep = self.image_parser.get_face_representation(rgb_img , bounding_box)
                out_reps[img_id] = rep
                print('rep added.')
            else:
                print('Bounding box not found.')

        return out_reps


    def save_representations(self,representations, path_to_save):
        np.save(path_to_save,representations)

    def load_representations(self, rep_file_path):
        self.representations = np.load(rep_file_path).item()

    def get_representations(self):
        return self.representations