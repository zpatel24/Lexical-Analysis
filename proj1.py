import sys

# Comparison lists
_operator = [  "(", ")",  "*",  "/",  "+",  "-",  "^",  "=" ]
_op_types = [ "LP","RP","MUL","DIV","ADD","SUB","EXP","ASN" ]
_operator_tuple = list( zip(_operator,_op_types) )

_skip = [ "\t", " " ]
_separator = [ "\n", ";" ] 
_alpha = [ chr(i) for i in range(65,123) if not i in range(91,97) ] + ['_'] 
_numeric = [ str(i) for i in range(10) ] + ['.'] # . gives floating point

_unary = ['-']
_unary_tuple = [('-','NEG')]

# Valid States
END=-1
START=0
IDENTIFIER=1
LITERAL=2
SEPARATOR=3
OPERATOR=4

# Parent State
class State:
	# FUNC : run()
	# ARGS
	#   @self : instance reference
	#   @input_list  : list of remaining input to be processed
	#   @output_list : list of tuples (TOKEN,TYPE)
	# DESC: 
	#   returns the next state given input_list[0]
	def run(self,input_list,output_list):
		raise NotImplementedError

### TASK 01 (OF 04): COMPLETE THE START CLASS
        
## Start ##
# Transition Function {
#   [\t| ] -> START
#   [0-9] -> LITERAL
#   [(|)|*|+|-|^|=] -> OPERATOR
#   [\n|;] -> SEPARATOR
#   [a-zA-z_] -> IDENTIFIER
#   else -> END
# }
##
# DESC :
#   Return state that handles symbol at input_list[0]
##
class Start(State):

	def run( self, input_list, output_list ):

		if not input_list:
			return END

		elif input_list[0] in _skip:
			input_list.pop(0)
			return START

		elif input_list[0] in _numeric:
			return LITERAL

		elif input_list[0] in _operator:
			return OPERATOR

        elif input_list[0] in _separator:
            return SEPARATOR
               
        elif input_list[0] in _identifier:
            return IDENTIFIER

		#elif ...
		#	return SEPARATOR

		#elif ...
		#	return IDENTIFIER

		else:
			return END
        
### TASK 02 (OF 04): COMPLETE THE IDENTIFIER CLASS    
    
## Identifier ##
# Transition Function {
#   [\t| ] -> START
#   [\n|;] -> SEPARATOR
#   [0-9a-zA-z_] -> IDENTIFIER
#   [(|)|*|+|-|^|=] -> OPERATOR
#   else -> END
# }
##
# DESC :
#  self-loop: Consume input_list[0] and append input_list[0] to TOKEN
#  else: Append (TOKEN,"ID") to output_list and clear TOKEN
##
class Identifier(State):

	def __init__(self):
		self.token = []

	# Clear the token and append the tuple to the output_list
	def append_to_output(self, output_list):
		tok = "".join( self.token )
		output_list.append( (tok,"ID") )
		self.token.clear()

	def run( self, input_list, output_list ):

		if not input_list:
			self.append_to_output( output_list )
			return END

		elif input_list[0] in _skip:
			self.append_to_output( output_list )
			input_list.pop(0)
			return START

        elif input_list[0] in _separator:
            self.append_to_output( output_list )
            return SEPARATOR
       
        elif input_list[0] in _identifier:
            self.append_to_output( output_list )
            return IDENTIFIER


		#elif ...
		#	return SEPARATOR

		#elif ...
		#	return IDENTIFIER

		elif input_list[0] in _operator:
			self.append_to_output( output_list )
			return OPERATOR

		else:
			self.append_to_output( output_list )
			return END

### TASK 03 (OF 04): COMPLETE THE LITERAL CLASS

## Literal ##
# Transition Function {
#   [\t| ] -> START
#   [0-9] -> LITERAL
#   [(|)|*|+|-|^|=] -> OPERATOR
#   [\n|;] -> SEPARATOR
#   [a-zA-z_] -> IDENTIFIER
#   else -> END
# }
##
# DESC :
#  self-loop: Consume input_list[0] and append input_list[0] to TOKEN
#  else: Append (TOKEN,"LITERAL") to output_list and clear TOKEN
##
class Literal(State):

	def __init__(self):
		self.token = []

	# Clear the token and append the tuple to the output_list
	def append_to_output(self, output_list):
		tok = "".join( self.token )
		output_list.append( (tok,"LITERAL") )
		self.token.clear()

	def run( self, input_list, output_list ):

		if not input_list:
			self.append_to_output( output_list )
			return END

		elif input_list[0] in _skip:
			self.append_to_output( output_list )
			input_list.pop(0)
			return START

		elif input_list[0] in _numeric:
			self.token.append( input_list[0] )
			input_list.pop(0) 
			return LITERAL

		elif input_list[0] in _operator:
			self.append_to_output( output_list )
			return OPERATOR
       
        elif input_list[0] in _separator:
            self.append_to_output( output_list )
            return SEPARATOR
        
        elif input_list[0] in _identifier:
            self.append_to_output( output_list )
            return IDENTIFIER
		#elif ...
		#	return SEPARATOR

		#elif ...
		#	return IDENTIFIER

		else:
			self.append_to_output( output_list )
			return END

### TASK 04 (OF 04): COMPLETE THE SEPARATOR CLASS        
        
## Separator ##
# Transition Function {
#   [\n|;] -> START
#   else -> END
# }
##
# DESC :
#   Consumes input_list[0] and appends (TOKEN,"SEP") to the output_list
#     where TOKEN is in _separator
##
class Separator(State):
	def run( self, input_list, output_list ):
        if input_list and input_list[0] in _separator:
            i = _separator.index( input_list[0] )
            output_list.append( _operator_tuple[i] )
            input_list.pop(0)
            return START
        
        else:
            return END
		#if ...
		#	return START

		#else ...
		#	return END

		pass
        
### THE REST OF THE CLASSES HAVE BEEN COMPLETED FOR YOU        
        
## Operator ##
# Transition Function {
#   [(|)|*|+|-|^|=] -> START
#   else -> END
# }
##
# DESC :
#   Consumes input_list[0] and appends (TOKEN,TYPE) to output_list
#     where TOKEN is in _operator and TYPE is in _op_types
##
class Operator(State):
	def run( self, input_list, output_list):

		# Unary NEG, different from minus
		if len( input_list ) > 1 and input_list[0] in _unary \
			and input_list[1] in _alpha+_numeric+['(']:

			if not output_list or output_list[-1] in _operator_tuple:
				i = _unary.index( input_list[0] )
				output_list.append( _unary_tuple[i] )
				input_list.pop(0)
				return START

		# Find the operator tuple and append to list
		if input_list and input_list[0] in _operator:
			i = _operator.index( input_list[0] )
			output_list.append( _operator_tuple[i] )
			input_list.pop(0)
			return START

		else:
			return END
        
class Lexer():
	machine = {
		START : Start(),
		IDENTIFIER : Identifier(),
		LITERAL : Literal(),
		SEPARATOR : Separator(),
		OPERATOR : Operator()
	}

	# Initialize the start state to START
	def __init__(self, input_list):
		self.state = START
		self.input = input_list.copy()
		self.output = []

    # Return and consume the next token
    # Return none if current state == END
	def next_token(self):
		old = len(self.output)

		while old == len(self.output) and self.state != END:
			self.state = self.machine[ self.state ].run( self.input, self.output )

		if old != len(self.output):
			return self.output[-1]

    # Look <depth> tokens into the future
    # Return a token or none
	def peek_token(self, depth=1):
		old = self.output.copy()
		new = self.output.copy()
		inp = self.input.copy()
		state = self.state

		while len(new)-len(old) != depth and state != END:
			state = self.machine[ state ].run( inp, new )

		if len(old) != len(new):
			return new[-1]

	# Generate all tokens, run the machine
	def all_tokens(self):
		while self.state != END:
			self.state = self.machine[ self.state ].run( self.input, self.output )
		return self.output

# Try with "echo -n 1234 + 45 - \( | python3 proj1" => (1234,LITERAL),(+,ADD),...,((,LP)
if __name__ == "__main__":
	# Gather the inputstring from stdin
	instr = ""
	for line in sys.stdin:
		instr = instr + line

	# Convert the string into a list of characters
	input_list = list( instr )

	lexer = Lexer( input_list )
	output = lexer.all_tokens()

	if lexer.input:
		print( "ERROR: invalid symbol [ %s ]" % lexer.input[0] )
	else:
		print( output )
