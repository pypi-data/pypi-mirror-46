class ModeError(Exception):
    def __str__(self):
    	return repr("Please Enter A Correct Mode. MU or MD")
