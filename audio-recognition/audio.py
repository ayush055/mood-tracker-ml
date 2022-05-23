import requests
import time

headers = {"authorization": auth_key, "content-type": "application/json"}
def read_file(filename):
   with open(filename, "rb") as _file:
       while True:
           data = _file.read(5242880)
           if not data:
               break
           yield data
 
upload_response = requests.post("https://api.assemblyai.com/v2/upload", headers=headers, data=read_file("day3.mp3"))
audio_url = upload_response.json()["upload_url"]

transcript_request = {"audio_url": audio_url}
print(transcript_request)
transcript_response = requests.post("https://api.assemblyai.com/v2/transcript", json=transcript_request, headers=headers)
_id = transcript_response.json()["id"]

polling_response = requests.get("https://api.assemblyai.com/v2/transcript/" + _id, headers=headers)
if polling_response.json()["status"] != "completed":
    print("here")
    print(polling_response.json())
else:
    with open(_id + ".txt", "w") as f:
        f.write(polling_response.json()["text"])
    print("Transcript saved to", _id, ".txt")