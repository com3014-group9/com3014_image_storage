# com3014_image_storage

Image storage and handling service for the image sharing app

## Overview
This service handles the following functions:
- Storage of the uploaded image
- Retrieval of the stored images based of IDs/Tags/Ownership etc.
- Likes/dislike for the images

## Usage
Docker must be installed on the system. Run `docker-compose up -d --build` from the root of the repository. Once running, the service is accessible on the localhost:5050.

## Testing
Automatic testing is handled by pytest. To run the tests, build and start the container using the `docker-compose up -d --build` command and then `docker compose run imager-app python3 -m pytest` from the root of the repository.

## Endpoints

**/images/upload** Params: None

Uploads image to the backend storage. Form-data:

- file - file itself
- owner - a user who uploaded the image
- tags - list of tags associated with the image

Creates a database entry with provided owner and tags, the path to the uploaded file, incremented id and a timestamp.

**/images/<filename>** [AUTHENTICATED] Params: None

Returns an image stored under <filename>.

**/images/like** [AUTHENTICATED] Params: None

Adds like to the image. Form-data:

- image_id - id of the image to like

**/images/unlike** [AUTHENTICATED] Params: None

Removes like to the image. Form-data:

- image_id - id of the image to unlike

**/images/id/<id>** [AUTHENTICATED] Params: None

Returns an image associated with <id>

**/images/user/latest/<owner>** [AUTHENTICATED] Params: None

Returns last image uploaded by <owner>

**/images/user/<owner>** [AUTHENTICATED] Params: to, from

Returns a list of image URLs uploaded by the specified <owner>.

**/images/tag/<tag>** [AUTHENTICATED] Params: to, from

Returns a list of image URLs associated with a specified <tag>.

## DB Schema

Service uses MongoDB with the following schema:

- **id**: int32 - unique id of an image, increments one by one on each upload
- **owner**: string - the name of a user who uploaded the image
- **path**: string - path to the image in internal storage
- **tags**: array - list of tags associated with each image
- **timestamp**: int32 - UNIX timestamp for when the image was uploaded

## Docker

Image Server - `docker run -d -p 5000:5000 imager-docker`