#coding=UTF8

class Trans:
	def __init__ ( self ):
        	self.t = { u'А': '\x41', u'а': '\x61', u'Б': '\xa0', u'б': '\xb2', u'В': '\x42', u'в': '\xb3', u'Г': '\xa1', u'г': '\xb4', u'Д': '\xe0', u'д': '\xe3', u'Е': '\x45', u'е': '\x65', u'Ё': '\xa2', u'ё': '\xb5', u'Ж': '\xa3', u'ж': '\xb6', u'З': '\xa4', u'з': '\xb7', u'И': '\xa5', u'и': '\xb8', u'Й': '\xa6', u'й': '\xb9', u'К': '\x4b', u'к': '\xba', u'Л': '\xa7', u'л': '\xbb', u'М': '\x4b', u'м': '\xbc', u'Н': '\x48', u'н': '\xbd', u'О': '\x4f', u'о': '\x6f', u'П': '\xa8', u'п': '\xbe', u'Р': '\x50', u'р': '\x70', u'С': '\x43', u'с': '\x63', u'Т': '\x54', u'т': '\xbf', u'У': '\xa9', u'у': '\x79', u'Ф': '\xaa', u'ф': '\xe4', u'Х': '\x58', u'х': '\x78', u'Ц': '\xe1', u'ц': '\xe7', u'Ч': '\xab', u'ч': '\xc0', u'Ш': '\xac', u'ш': '\xc1', u'Щ': '\xe2', u'щ': '\xe6', u'Ъ': '\xad', u'ъ': '\xc2', u'Ы': '\xae', u'ы': '\xc3', u'Ь': '\x62', u'ь': '\xc4', u'Э': '\xaf', u'э': '\xc5', u'Ю': '\xb0', u'ю': '\xc6', u'Я': '\xb1', u'я': '\xc7', u'\xb0': '\x99' }
        	self.tu = { u'А': u'\x41', u'а': u'\x61', u'Б': u'\xa0', u'б': u'\xb2', u'В': u'\x42', u'в': u'\xb3', u'Г': u'\xa1', u'г': u'\xb4', u'Д': u'\xe0', u'д': u'\xe3', u'Е': u'\x45', u'е': u'\x65', u'Ё': u'\xa2', u'ё': u'\xb5', u'Ж': u'\xa3', u'ж': u'\xb6', u'З': u'\xa4', u'з': u'\xb7', u'И': u'\xa5', u'и': u'\xb8', u'Й': u'\xa6', u'й': u'\xb9', u'К': u'\x4b', u'к': u'\xba', u'Л': u'\xa7', u'л': u'\xbb', u'М': u'\x4b', u'м': u'\xbc', u'Н': u'\x48', u'н': u'\xbd', u'О': u'\x4f', u'о': u'\x6f', u'П': u'\xa8', u'п': u'\xbe', u'Р': u'\x50', u'р': u'\x70', u'С': u'\x43', u'с': u'\x63', u'Т': u'\x54', u'т': u'\xbf', u'У': u'\xa9', u'у': u'\x79', u'Ф': u'\xaa', u'ф': u'\xe4', u'Х': u'\x58', u'х': u'\x78', u'Ц': u'\xe1', u'ц': u'\xe7', u'Ч': u'\xab', u'ч': u'\xc0', u'Ш': u'\xac', u'ш': u'\xc1', u'Щ': u'\xe2', u'щ': u'\xe6', u'Ъ': u'\xad', u'ъ': u'\xc2', u'Ы': u'\xae', u'ы': u'\xc3', u'Ь': u'\x62', u'ь': u'\xc4', u'Э': u'\xaf', u'э': u'\xc5', u'Ю': u'\xb0', u'ю': u'\xc6', u'Я': u'\xb1', u'я': u'\xc7', u'\xb0': u'\x99' }
	def translate ( self, text ):
        	trKeys = self.t.keys ()
		resultText = list ()
		for c in range ( len ( text ) ):
			resultText.append ( '' )
			for i in text [ c ]:
				if i in trKeys:
					resultText [ c ] += self.t [ i ]
				else:
					resultText [ c ] += i.encode ( "ASCII", "ignore" )
		return resultText
	def translateUTF ( self, text ):
        	trKeys = self.t.keys ()
		resultText = list ()
		for c in range ( len ( text ) ):
			resultText.append ( u'' )
			for i in text [ c ]:
				if i in trKeys:
					resultText [ c ] += self.tu [ i ]
				else:
					resultText [ c ] += i
		return resultText
