import json
import sys

class jsonObject:
	
	class_define_array = []
	
	class_array = []
	
	file_name = ''
	
	new_line 	 = "\n\n"
	
	protocol	 = "@protocol "
	
	end 		 = "@end "
	
	interface    = "@interface "
	
	implementation = "@implementation "
	
	object_prefix = "@property (nonatomic, strong) "
	
	primitive_prefix = "@property (nonatomic, assign) "
	 
	number_prefix =  " NSNumber <Optional> "
	
	number = " NSNumber "
	
	integer_prefix =  " NSInteger <Optional> "
	
	bool_prefix =  " BOOL <Optional> "
	
	float_prefix =  " float <Optional> "
	
	long_prefix =  " long <Optional> "
	
	string_prefix = " NSString <Optional> "
    
	optional_prefix = " <Optional> "
	
	string = " NSString "
	
	pointer = " * "
	
	class_seperator = "_"
	
	line_end = ";"
	
	base_class = "JSONModel"
	
	inherit_operator = " : "
	
	def printError(self, message):
		print "Error : " + message
		
		
	def __init__(self,file_name,root_class):
	
		self.file_name = file_name
		
		try:
			obj = json.loads(self.readFile(self.file_name) )
			self.parseJson(obj,root_class,False)
		except:
			self.printError("invalid json string !")
        	
		
		
	def write2File(self):
		
		self.writeHeader2File();
		self.writeImpl2File();
	
	def writeHeader2File(self):
	
		text_file = open(self.file_name + ".h", "w")
		for  k in self.class_define_array:
			text_file.write(k)
		text_file.close()
		
	def writeImpl2File(self):
	
		text_file = open(self.file_name + ".m", "w")
		for  k in self.class_array:
			text_file.write(self.new_line + self.implementation + k+ self.new_line + self.end+self.new_line)
		text_file.close()
		
	def readFile (self, file_name ):
        	file_handler = open(file_name)
        	file_text = file_handler.read()
		return file_text
		
	

	def parseJson (self, decoded_json_string, class_name,isprotocol ):
		if isprotocol == True :
			self.class_define_array.append(self.protocol+ class_name +" "+self.new_line+self.end+self.new_line)
		self.class_array.append(class_name)
		str =  self.new_line + self.interface +  class_name + self.inherit_operator + self.base_class
		for  k in decoded_json_string.keys():
			v = decoded_json_string[k]
			if isinstance(v,float) or isinstance(v,int) or isinstance(v,long) or isinstance(v,bool):
				str += self.new_line + self.object_prefix + self.number_prefix + self.pointer+ k + self.line_end
			elif isinstance(v,basestring) :
				str += self.new_line + self.object_prefix +  self.string_prefix + self.pointer + k+ self.line_end
			elif isinstance(v,dict):
				class_name = class_name + self.class_seperator + k
				str += self.new_line + self.object_prefix + class_name + self.optional_prefix + self.pointer + k + self.line_end
				self.parseJson(v,class_name,False)
			elif isinstance(v,list) or isinstance(v,tuple) :
				if len(v) == 0 :
					self.printError( "key '" + k + "' can not be empty!");
				value = v[0]
				#print(value)
				if isinstance(value,list):
					subValue = value[0]
					class_name = class_name + self.class_seperator + '0'
					str += self.new_line + self.object_prefix + "NSMutableArray<NSMutableArray <"+ class_name + ">*>*"  + k + self.line_end
					self.parseJson(subValue,class_name,True)
				elif isinstance(value,float) or isinstance(value,int) or isinstance(value,long) or isinstance(value,bool) or isinstance(value,basestring):
					str += self.new_line + self.object_prefix + " NSMutableArray < Optional> * " + k + self.line_end
				else:
					class_name = class_name + self.class_seperator + k
					str += self.new_line + self.object_prefix + " NSMutableArray <" + class_name + ",Optional> * " + k + self.line_end
					self.parseJson(value,class_name,True)
		str += self.new_line+self.end+self.new_line
		self.class_define_array.append(str)
		
	
object = jsonObject(sys.argv[1],sys.argv[2])
object.write2File();
