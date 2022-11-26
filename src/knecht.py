import json

from storage import PicStore

myPicStore = PicStore()


# with open("./tmp/DaFinoAtWork.jpg", "rb") as fl:
#   payload = fl.read()

# new_payload = myPicStore.convert_picture(payload=payload)
# myPicStore.save_picture(payload=new_payload)


res = myPicStore.list_pictures()
print(json.dumps(res, indent=2, default=str))
# myPicStore.delete_picture(filename="ee40ba4c-eff4-4c6c-8c05-8c856a073aec.jpeg")