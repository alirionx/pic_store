import json

from storage import PicStore
from meta import MetaStore

myPicStore = PicStore()
# myPicStore.get_image_by_filename(filename="")


# with open("./tmp/DaFinoAtWork.jpg", "rb") as fl:
#   payload = fl.read()

# image_payload, thumb_payload = myPicStore.convert_picture(payload=payload)
# myPicStore.save_picture(image_payload=image_payload, thumb_payload=thumb_payload)


# res = myPicStore.list_pictures()
# print(json.dumps(res, indent=2, default=str))
# myPicStore.delete_image(filename="ee40ba4c-eff4-4c6c-8c05-8c856a073aec.jpeg")

# res = myPicStore.get_image_as_byte(filename="bf396953-0285-45fd-a9ae-f303d2b5818c.jpeg")
# print(len(res))

# myMetaStore = MetaStore()

# data = {
#   "filename": "bf396953-0285-45fd-a9ae-f303d2b5818c.jpeg",
#   "album": "Freizeit",
#   "format": "Square"
# }

# myMetaStore.add_picture_meta(data=data)
# myMetaStore.update_picture_meta(
#   filename="ee40ba4c-eff4-4c6c-8c05-8c856a073aec.jpeg", 
#   data=data
# )

# myMetaStore.delete_picture_meta(filename="bf396953-0285-45fd-a9ae-f303d2b5818c.jpeg")

# res = myMetaStore.get_pictures_meta()
# print(res)