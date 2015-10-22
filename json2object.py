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
	 
	number_prefix =  " NSNumber <Optional> "
	
	string_prefix = " NSString <Optional> "
	pointer = " * "
	
	class_seperator = "_"
	
	line_end = ";"
	
	base_class = "JSONModel"
	
	inherit_operator = " : "
	
	def __init__(self,file_name,root_class):
		self.file_name = file_name
		self.parseJson(json.loads(self.readFile(self.file_name) ),root_class,False)
		
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
			if isinstance(v,int) or isinstance(v,float) or isinstance(v,long) :
				str += self.new_line + self.object_prefix + self.number_prefix + self.pointer + k + self.line_end
			elif isinstance(v,basestring) :
				str += self.new_line + self.object_prefix +  self.string_prefix + self.pointer + k+ self.line_end
			elif isinstance(v,dict):
				class_name = class_name + self.class_seperator + k
				str += self.new_line + self.object_prefix + class_name + self.pointer + k + self.line_end
				self.parseJson(v,class_name,False)
			elif isinstance(v,list) or isinstance(v,tuple) :
				class_name = class_name + self.class_seperator + k
				str += self.new_line + self.object_prefix + " NSMutableArray <" + class_name + ",Optional> * " + k + self.line_end
				self.parseJson(v[0],class_name,True)
		str += self.new_line+self.end+self.new_line
		self.class_define_array.append(str)
			
	
	

print "\n\nusage: \n python json2Object.py your_json_file your_base_class_name\n\n"
	
object = jsonObject(sys.argv[1],sys.argv[2])
object.write2File();

print "\nsuccess!\n\n"
