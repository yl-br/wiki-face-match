# wiki-face-match

Wiki-Face-Match extracts a face representation from a given image, then compares it against an archive of ~40,000 Wikipedia figures images, to find the best matching faces.


### wiki-face-match-api (api):
written in python.
Using python flask, it exposes an http api, with 2 methods:

- get randomImages:
	Returns 12 images paths, from a paths collection of imdb photos.

- post findMatches: 
	Uses OpenFace and OpenCV2 libraries, to extract a face representation from an input image. Then it compares the given face representation to a pre-calculated representation matrix, composed by a Wikipedia image archive.
After a distance is determined between the given representation and the Wikipedia representations, the top n images with the smallest distances are returned.


### wiki-face-match-client (client):
written in angular 1.
Code for a user interface to consume the wiki-face-match-api.







