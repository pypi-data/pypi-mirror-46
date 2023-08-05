
from diffgram import Project
import settings_debug as settings

project = Project(
			client_id = settings.CLIENT_ID,
			client_secret = settings.CLIENT_SECRET,
			project_string_id = settings.PROJECT_STRING_ID,
			debug = True)

#file = project.file.from_url("apples")

#path = "A:/Sync/work/diffgram/som_test_jpg.jpg"

#file = project.file.from_local(path)


#print(file)

#file2 = project.file.from_url(1, 1)

#print(file2)

#file.id = 17

#brain = project.train.start(name = "my brain")

brain = project.get_model(name = "Lightningtrader")

inference = brain.predict_from_file(file_id = 111546)

#brain.check_status()

#print(brain.status)

#brain.name = "alphabet"
#expect 
#Exception: {'ai': 'AI named alphabet not found in project som-gms-training-data-aug-2018'}

print(inference.instance_list)

print(inference.instance_list[0].location)


#brain.predict(file)

# inference = brain.predict_from_url("apples.com")
# returns Exception: {'input': 'failed , invalid url'}

#url = "https://www.readersdigest.ca/wp-content/uploads/sites/14/2011/01/4-ways-cheer-up-depressed-cat.jpg"

url = "https://storage.googleapis.com/diffgram-002/projects/images/36/12533?Expires=1555202574&GoogleAccessId=storage%40diffgram-001.iam.gserviceaccount.com&Signature=aE7ODVaIktULa2nvEbllTmlIf%2BQb0KM%2FhcXLf5kuyJn8VQJJkuURMnd9RrOP%2BkJELTgcWOhSjvaJhjzvJ1j%2FYz%2B7Wbwhl%2B3NOvIbMYikLd2mkVxydXgxS5eyg58KM%2BuKDDI%2BXqSyj%2BhNKXG4NTUWEcarQtUdUjw66nMm2jUccAFcJoZF8sSfjejemNgjlV0icx5GTXaSDvcs04wqYoVjZ4Bmsf6VlDXKKtS2btxm4jS58YMfySIj9SXjJAoguBBn5YEgrGS5W8cA8e1WPArLmIFPShbibFN4%2FcazUOGTxM2T%2BAuJd0jRcSFei4vh5obs56eKZPOGDoc4DBp1a1G2Jg%3D%3D"

#inference = brain.predict_from_url(url)


#inference = brain.predict_from_file(file_id = 13622)




