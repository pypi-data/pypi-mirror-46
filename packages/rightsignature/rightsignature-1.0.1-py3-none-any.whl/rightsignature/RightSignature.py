import requests
import urllib.parse

class CRightSignature:
	def __init__(self, key):
		self.apikey = key
		self.valid = True
		r = requests.get('https://rightsignature.com/api/documents.json',headers = {'api-token': self.apikey})
		if r.text == "Invalid OAuth Request":
			self.valid = False
	def getDocuments(self):
		if not self.valid:
			return
		r = requests.get('https://rightsignature.com/api/documents.json',headers = {'api-token': self.apikey})
		documents = list()
		for doc in r.json()['page']['documents']:
			documents.append(CDocument(doc))
		return documents
	def getDocument(self,guid):
		if not self.valid:
			return
		r = requests.get('https://rightsignature.com/api/documents/' + guid + '.json',headers = {'api-token': self.apikey})
		return CDocument(r.json()['document'])
	def downloadSignedPDF(self,document, saveLocation):
		r = requests.get(urllib.parse.unquote(document.getSignedPdfUrl()))
		with open(saveLocation, 'wb') as f:  
			f.write(r.content)
	def isLoggedIn(self):
		return self.valid

class CDocument:
	def __init__(self, data):
		self.audit_trails = list()
		for auditdata in data['audit_trails']:	
			self.audit_trails.append(CAudit(auditdata))
		self.callback_location = data['callback_location']
		self.completed_at = data['completed_at']
		self.content_type = data['content_type']
		self.created_at = data['created_at']
		self.expires_on = data['expires_on']
		self.form_fields = list()
		if 'form_fields' in data:
			for fieldata in data['form_fields']:	
				self.form_fields.append(CField(fieldata))
		self.guid = data['guid']
		self.is_trashed = data['is_trashed']
		self.large_url = data['large_url']
		self.last_activity_at = data['last_activity_at']
		self.merge_state = data['merge_state']
		self.message = data['message']
		self.original_filename = data['original_filename']
		self.original_url = data['original_url']		
		self.pages = list()
		if 'pages' in data:
			for pagedata in data['pages']:	
				self.pages.append(CPage(pagedata))
		self.pdf_url = data['pdf_url']
		self.processing_state = data['processing_state']
		self.recipients = list()
		for recidata in data['recipients']:	
			self.recipients.append(CRecipient(recidata))
		self.signed_pdf_checksum = data['signed_pdf_checksum']
		self.signed_pdf_url = data['signed_pdf_url']
		self.size = data['size']
		self.state = data['state']
		self.subject = data['subject']
		self.tags = data['tags']
		self.thumbnail_url = data['thumbnail_url']
	def getAuditTrails(self):
		return self.audit_trails
	def getCallbackLocation(self):
		return self.callback_location
	def getCompletedAt(self):
		return self.completed_at
	def getContentType(self):
		return self.content_type
	def getCreatedAt(self):
		return self.created_at	
	def getExpiresOn(self):
		return self.expires_on	
	def getFormFields(self):
		return self.form_fields		
	def getGuid(self):
		return self.guid		
	def isTrashed(self):
		return self.is_trashed		
	def getLargeUrl(self):
		return self.large_url		
	def getLastActivityAt(self):
		return self.last_activity_at		
	def getMergeState(self):
		return self.merge_state		
	def getMessage(self):
		return self.message		
	def getOriginalFilename(self):
		return self.original_filename		
	def getOriginalUrl(self):
		return self.original_url		
	def getPages(self):
		return self.pages		
	def getPdfUrl(self):
		return self.pdf_url		
	def getProcessingState(self):
		return self.processing_state		
	def getRecipients(self):
		return self.recipients		
	def getSignedPdfChecksum(self):
		return self.signed_pdf_checksum		
	def getSignedPdfUrl(self):
		return self.signed_pdf_url		
	def getSize(self):
		return self.size	
	def getState(self):
		return self.state
	def getSubject(self):
		return self.subject
	def getTags(self):
		return self.tags
	def getThumbnailUrl(self):
		return self.thumbnail_url
		
class CAudit:
	def __init__(self, data):
		self.keyword = data['keyword']
		self.message = data['message']
		self.timestamp = data['timestamp']
	def getKeyword(self):
		return self.keyword
	def getMessage(self):
		return self.message
	def getTimestamp(self):
		return self.timestamp
	
class CRecipient:
	def __init__(self, data):
		self.completed_at = data['completed_at']
		self.document_role_id = data['document_role_id']
		self.email = data['email']
		self.is_sender = data['is_sender']
		self.must_sign = data['must_sign']
		self.name = data['name']
		self.role_id = data['role_id']
		self.state = data['state']
		self.viewed_at = data['viewed_at']
	def getCompletedAt(self):
		return self.completed_at
	def getDocumentRoleID(self):
		return self.document_role_id
	def getEmail(self):
		return self.email
	def isSender(self):
		return self.is_sender
	def getMustSign(self):
		return self.must_sign
	def getName(self):
		return self.name
	def getRoleID(self):
		return self.role_id
	def getState(self):
		return self.state
	def getViewedAt(self):
		return self.viewed_at

class CPage:
	def __init__(self, data):
		self.original_template_filename = data['original_template_filename']
		self.original_template_guid = data['original_template_guid']
		self.page_number = data['page_number']
	def getOriginalTemplateFilename(self):
		return self.original_template_filename
	def getOriginalTemplateGUID(self):
		return self.original_template_guid
	def getPageNumber(self):
		return self.page_number						
	
class CField:
	def __init__(self, data):
		self.id = data['id']
		self.name = data['name']
		self.page = data['page']
		self.role_id = data['role_id']
		self.value = data['value']
	def getID(self):
		return self.id
	def getName(self):
		return self.name
	def getPage(self):
		return self.page
	def getRoleID(self):
		return self.role_id
	def getValue(self):
		return self.value

