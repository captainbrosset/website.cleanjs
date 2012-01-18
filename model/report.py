from google.appengine.ext import db

def add_file(src_file):
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
	new_ds_entry.put()
	
	return index.currentIndex
	
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

class SourceFileCounter(db.Model):
    """
    There is no auto-increment primary key thing in the datastore,
    so this model class is here to keep only one entity, that gets incremented everytime something is
    added to the model
    """
    currentIndex = db.IntegerProperty()