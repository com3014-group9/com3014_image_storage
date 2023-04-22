## Endpoints

**/images/upload** Params: None

Uploads image to the backend storage. Form-data:

- file - file itself
- owner - a user who uploaded the image
- tags - list of tags associated with the image

Creates a database entry with provided owner and tags, the path to the uploaded file, incremented id and a timestamp.

**/images/<filename>** Params: None

Returns an image stored under <filename>.

**/images/id/<id>** Params: None

Returns an image associated with <id>

**/images/user/latest/<owner>** Params: None

Returns last image uploaded by <owner>

**/images/user/<owner>** Params: to, from

Returns a list of image URLs uploaded by the specified <owner>.

**/images/tag/<tag>** Params: to, from

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