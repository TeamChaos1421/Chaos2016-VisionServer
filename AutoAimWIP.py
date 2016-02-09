########################################################################
# Calculate Rotational Movement

if data["useful"] == True:
	
	# Get Offset (in pixels, relative to center)
	cx = data["cx"]
	
	# Proportional Control
	rotation = -0.01*cx
	
	# Bracketing
	if rotation > 0.5:
		rotation = 0.5
	elif rotation < -0.5:
		rotation = 0.5
	
else:
	rotation = 0
########################################################################
# Calculate Forward Movement

forward = 0

########################################################################
# Calculate Roller

roller = 0

########################################################################
# Generate Result, Print, and Return

# Result to "Return"
output = str(forward) + " " + str(rotation) + " " + str(roller)

# Print Result for Debugging
print('"' + request.rstrip() + '" + ' + str(data) + ' => "' + str(output) + '"')
