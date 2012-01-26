try:
	from google.appengine.ext import db
except:
	# Mocking
	class IntegerProperty(object): pass
	class TextProperty(object): pass
	class StringProperty(object): pass
	class Model(object): pass
	class db(object):
		Model = Model
		IntegerProperty = IntegerProperty
		TextProperty = TextProperty
		StringProperty = StringProperty


def get_file_index_from_src(src_file):
	hashed = src_file.__hash__()
	query = SourceFile.all().filter("hashed = ", hashed)
	indexes = query.fetch(1)
	if len(indexes) == 1:
		return indexes[0].index
	else:
		return None

def add_file_to_global_stats(src_code, file_data, rating, message_bag):
	# Retrieve the SourceFileCounter single object
	index = SourceFileCounter.all().fetch(1)[0]
	
	# Gathering stats	
	nb_of_lines = len(file_data.lines.all_lines)
	nb_of_messages = len(message_bag.get_messages())

	if not index.total_lines:
		index.total_lines = 0
	index.total_lines += nb_of_lines

	if not index.total_messages:
		index.total_messages = 0
	index.total_messages += nb_of_messages

	if not index.average_rate:
		index.average_rate = rating
	else:
		index.average_rate = get_average_rating(rating, index.average_rate, index.currentIndex)
	
	index.put()

def get_average_rating(new_rating, current_average, new_nb_of_files):
	map = ["A+","A","A-","B+","B","B-","C+","C","C-","D+","D","D-","E+","E","E-","F+","F","F-"]
	new_index = map.index(new_rating)
	currentIndex = map.index(current_average)
	new_index = (new_index + currentIndex*(new_nb_of_files-1)) / new_nb_of_files
	return map[new_index]

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
	total_lines = db.IntegerProperty()
	total_messages = db.IntegerProperty()
	average_rate = db.StringProperty()

if __name__ == "__main__":
	assert get_average_rating("A+", "A+", 50) == "A+"
	assert get_average_rating("A+", "F-", 2) == "C-"
	assert get_average_rating("F-", "F-", 5) == "F-"

	print "ALL TESTS OK " + __file__