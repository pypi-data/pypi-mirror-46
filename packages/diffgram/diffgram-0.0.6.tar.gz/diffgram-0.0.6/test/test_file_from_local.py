
from diffgram.core.core import Project
import settings_debug as settings

client = Project(debug=True)

client.auth(client_id = settings.CLIENT_ID,
			client_secret = settings.CLIENT_SECRET,
			project_string_id = settings.PROJECT_STRING_ID)



#path = "A:/Sync/work/ai_vision/examples/pepper_chef/20190311_200900.jpg"
#path = "A:/Sync/work/diffgram/som_test.png"

path = "A:/Sync/work/diffgram/som_test_jpg.jpg"

file = client.file.from_local(path)

"""
red_pepper = client.get_model()

cutting_board = client.get_model()

red_pepper_inference = red_pepper.predict_from_local(path,
									 threshold = .50)


cutting_board_inference = cutting_board.predict_from_local(path,
									 threshold = .50)

if inference.count == 0:

	pass
	# No predictions above threshold


if cutting_board_inference.result and red_pepper_inference.result:

	# valid result
	pass

#if red_pepper_inference.count == 0 and cutting_board_inference.count > 0:
if cutting_board_inference.result and not red_pepper_inference.result:

	# Flag red pepper image for human review

	# Creates task for human review / adds to job etc

	red_pepper.exception.human_review(red_pepper_inference)


if red_pepper_inference in cutting_board_inference:

	# This could get tricky for multiple classes...  maybe have 
	# to declare a class?

	# ie inference.class in inference.class?
	# assumes "any" ... hmmmm

	# May have to have some strong limits 
	# ie only compares first class by default or something
	
	# What about "near" instead of in...

	# red pepper result is inside cutting_board
	# ie default IoU of xyz
	# https://stackoverflow.com/questions/2217001/override-pythons-in-operator

	pass



# What about simple things like
# red_pepper_inference.show() for matplatlib?



"""






