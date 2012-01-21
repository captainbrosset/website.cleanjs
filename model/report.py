try:
	from google.appengine.ext import db
except:
	# Mocking
	class IntegerProperty(object): pass
	class TextProperty(object): pass
	class Model(object): pass
	class db(object):
		Model = Model
		IntegerProperty = IntegerProperty
		TextProperty = TextProperty

def get_file_index_from_src(src_file):
	hashed = src_file.__hash__()
	query = SourceFile.all().filter("hashed = ", hashed)
	indexes = query.fetch(1)
	if len(indexes) == 1:
		return indexes[0].index
	else:
		return None

def add_file(src_file):
	file_index = get_file_index_from_src(src_file)

	if not file_index:
		#increment counter
		try:
			index = SourceFileCounter.all().fetch(1)[0]
		except:
			index = SourceFileCounter(currentIndex=0)
		index.currentIndex += 1
		index.put()
		
		new_ds_entry = SourceFile()
		new_ds_entry.content = src_file
		new_ds_entry.index = index.currentIndex
		new_ds_entry.hashed = src_file.__hash__()
		new_ds_entry.put()
		
		file_index = index.currentIndex
	
	return file_index
	
def get_file(index):
	"""
	Returns a file model instance from a given index.
	"""
	query = SourceFile.all().filter("index = ", int(index))
	indexes = query.fetch(1)
	if len(indexes) == 1:
		index = indexes[0]
		return index.content
	else:
		return None

class SourceFile(db.Model):
	index = db.IntegerProperty()
	content = db.TextProperty()
	hashed = db.IntegerProperty()

class SourceFileCounter(db.Model):
	"""
	There is no auto-increment primary key thing in the datastore,
	so this model class is here to keep only one entity, that gets incremented everytime something is
	added to the model
	"""
	currentIndex = db.IntegerProperty()