from image_parser import ImageParser
from representation_store import RepresentationStore
import pandas

path_to_open_face_models = '../openface/models'
images_meta_csv_path = '../wiki-faces-meta.csv'
images_dir_path = '../wiki_crop'

images_meta_df = pandas.read_csv(images_meta_csv_path)

image_parser = ImageParser(path_to_open_face_models)
image_parser.init()

representation_store = RepresentationStore(image_parser)
reps = representation_store.calculate_representations(images_meta_df,images_dir_path)
representation_store.save_representations(reps, 'wiki-reps-new.npy')
