from models import *
import datetime
import env
from sqlalchemy.orm import  sessionmaker
from sqlalchemy import create_engine

class Repository(object):
	"""docstring for Repository"""

	'''
	filter by model attribute
	'''
	@staticmethod
	def filter_by_attribute(modelName, filterKeys):
	    return modelName.query.get(filterKeys)

	'''
	return paginated data 
	'''
	@staticmethod
	def filer_by_paginated(modelName, filterKeys, item=25, page=1):
		return modelName.query.filter_by(**filterKeys).paginate(page=int(page), per_page=int(item), error_out=False)

	'''
	return data using filter by
	'''
	@staticmethod
	def filter_attribute(modelName, filterKeys):
	    return modelName.query.filter_by(**filterKeys)

	'''
	update data in database
	'''
	@staticmethod
	def update(modelName, filterKeys, updateWith):
		row = db.session.query(modelName).filter_by(**filterKeys).update(updateWith) 
		db.session.commit()
		return row

	'''
	fetch all data form model
	'''
	@staticmethod
	def fetchAll(modelName):
	    return modelName.query.all()

	'''
	select the relevent column from database
	'''
	@staticmethod
	def fetchSelect(modelName, select_params):
		from sqlalchemy.orm import load_only
		return modelName.query.options(load_only(*select_params)).all()

	'''
	store the data and return model instance
	'''
	@staticmethod
	def store(modelName, values):
		modelInstance = modelName(**values)
		db.session.add(modelInstance)
		db.session.commit()
		return modelInstance

	'''
	delete rows from database
	'''
	@staticmethod
	def delete(modelName, filterKeys):
		rows = db.session.query(modelName).filter_by(**filterKeys).delete()
		# print dd.delete(synchronize_session = False)
		db.session.commit()
		return rows








