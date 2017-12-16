from flask import Flask, json
from helpers import Helpers

class Response(object):
	"""docstring for Response"""
		
	@staticmethod
	def respondWithItem(data, statusCode=200, message = 'Success', hint=''):
		response = dict(())
		response['data'] = data.transform()
		response['code'] = statusCode
		response['notification'] = {
			'feedCode' : 'WALLET_'+str(statusCode),
			'message' : message,
			'hint' : hint,
			'type' : 'success'
		}
		response['version'] = 1
		return json.jsonify(response)
	
	@staticmethod
	def respondWithCollection(data, statusCode = 200, message = 'Success', hint=''):
	    response_data = []
	    response = dict(())
	    for item in data:
	        response_data.append(data.transformer()) 
	    response['data'] = response_data
	    response['code'] = statusCode
	    response['notification'] = {
	        'feedCode' : 'WALLET_'+str(statusCode),
	        'message' : message,
	        'hint' : hint,
	        'type' : 'success'
	    }
	    response['version'] = 1
	    return json.jsonify(response)
	
	@staticmethod
	def respondWithArray(data, statusCode = 200, message = 'Success', hint=''):
		response = dict(())
		response['data'] = data
		response['code'] = statusCode
		response['notification'] = {
			'feedCode' : 'WALLET_'+str(statusCode),
			'message' : message,
			'hint' : hint,
			'type' : 'success'
		}
		response['version'] = 1
		return json.jsonify(response)
	
	@staticmethod
	def respondWithPaginatedCollection(data, statusCode = 200, message = 'Success', hint=''):
		response_data = []
		response = dict(())
		for item in data.items:
			response_data.append(data.transformer()) 
		response['data'] = response_data
		response['code'] = statusCode
		response['meta'] = {
			'pagination' : {
				'count' : data.per_page,
				'current_page' : data.page,
				'per_page' : data.per_page,
				'total' : data.total,
				'links' : {
					'prev_page' : (Helpers.url_for_other_page(data.prev_num)) if (data.prev_num is not None) else None ,
					'next_page' : (Helpers.url_for_other_page(data.next_num)) if (data.next_num is not None) else None
				},
				'total_page' : data.pages,
			}
		}
		response['notification'] = {
			'feedCode' : 'WALLET_'+str(statusCode),
			'message' : message,
			'hint' : hint,
			'type' : 'success'
		}
		response['version'] = 1
		return json.jsonify(response)
	
	@staticmethod
	def respondOk(message = 'Success', statusCode = 200, hint=''):
		response = dict(())
		response['data'] = []
		response['code'] = statusCode
		response['notification'] = {
			'feedCode' : 'WALLET_'+str(statusCode),
			'message' : message,
			'hint' : hint,
			'type' : 'success'
		}
		response['version'] = 1
		return json.jsonify(response)
	
	@staticmethod
	def respondWithError(message = 'Error', statusCode = 500, hint=''):
		response = dict(())
		response['data'] = []
		response['code'] = statusCode
		response['notification'] = {
			'feedCode' : 'DDT_'+str(statusCode),
			'message' : message,
			'hint' : hint,
			'type' : 'error'
		}
		response['version'] = 1
		return json.jsonify(response)
