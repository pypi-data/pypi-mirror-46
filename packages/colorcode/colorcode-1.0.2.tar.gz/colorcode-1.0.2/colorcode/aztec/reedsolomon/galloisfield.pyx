
from cpython cimport array
from libc.stdint cimport uint16_t, int16_t
from libc.stdlib cimport malloc, free

from enum import Enum
import array

MODE_MESSAGE = -1

cdef class _GF(object):
	cdef uint16_t* __exptable
	cdef uint16_t* __logtable
	cdef __gencache
	cdef public uint16_t wordsize
	cdef public int16_t minlayers
	cdef public int16_t maxlayers
	cdef public uint16_t polynomial

	def __cinit__(self, wordsize, minlayers, maxlayers, polynomial):
		self.__exptable = <uint16_t*>malloc(sizeof(uint16_t) * (1 << (wordsize + 1)))
		self.__logtable = <uint16_t*>malloc(sizeof(uint16_t) * (1 << wordsize))
		for i in range(1 << (wordsize + 1)):
			self.__exptable[i] = 0
		for i in range(1 << wordsize):
			self.__logtable[i] = 0

	def __init__(self, wordsize, minlayers, maxlayers, polynomial):
		if (bool(minlayers < 0) or bool(maxlayers < 0)) and minlayers != maxlayers:
			raise ValueError("Cannot combine different special layer values: {} (min) and {} (max)".format(minlayers, maxlayers))
		self.wordsize = wordsize
		self.minlayers = minlayers
		self.maxlayers = maxlayers
		self.polynomial = polynomial
		self.__gencache = {}
		self.__init_lut()
	
	def __dealloc__(self):
		free(self.__exptable)
		free(self.__logtable)
	
	@property
	def fieldsize(self):
		return 1 << self.wordsize
	
	@property
	def isMode(self):
		return self.minlayers == MODE_MESSAGE
	
	@property
	def exptable(self):
		return [self.__exptable[i] for i in range(1 << (self.wordsize + 1))]
	
	@property
	def logtable(self):
		return [self.__exptable[i] for i in range(1 << (self.wordsize))]
	
	cdef uint16_t __mul_nolut(self, uint16_t a, uint16_t b):
		cdef uint16_t r = 0
		cdef uint16_t fs = self.fieldsize
		while b:
			if b & 1:
				r ^= a
			a <<= 1
			b >>= 1
			if a & fs:
				a ^= self.polynomial
		return r
	
	cdef void __init_lut(self):
		cdef uint16_t x = 1
		cdef uint16_t i
		for i in range(self.fieldsize - 1):
			self.__exptable[i] = x
			self.__logtable[x] = i
			x = self.__mul_nolut(x, 2)
		for i in range(self.fieldsize - 1, self.fieldsize << 1):
			self.__exptable[i] = self.__exptable[i + 1 - self.fieldsize]
	
	cpdef generator(self, uint16_t n):
		cdef uint16_t i
		result = self.__gencache.get(n, None)
		if result:
			return result
		result = [1]
		for i in range(1, n + 1):
			result = self.poly_mul(result, [1, self.pow(2, i)])
		self.__gencache[n] = result
		return result
	
	cpdef uint16_t add(self, uint16_t a, uint16_t b):
		return a ^ b
	
	cpdef uint16_t sub(self, uint16_t a, uint16_t b):
		return a ^ b
	
	cpdef uint16_t mul(self, uint16_t a, uint16_t b):
		if not(a and b):
			return 0
		return self.__exptable[self.__logtable[a] + self.__logtable[b]]
	
	cpdef uint16_t div(self, uint16_t a, uint16_t b):
		if not b:
			raise ZeroDivisionError()
		if not a:
			return 0
		return self.__exptable[(self.fieldsize - 1 + self.__logtable[a] - self.__logtable[b]) % 255]
	
	cpdef uint16_t pow(self, uint16_t a, uint16_t p):
		if not a:
			return 0
		return self.__exptable[(self.__logtable[a] * p) % (self.fieldsize - 1)]
	
	cpdef uint16_t inv(self, uint16_t a):
		if not a:
			raise ZeroDivisionError()
		return self.__exptable[self.fieldsize - 1 - self.__logtable[a]]
	
	cpdef poly_scale(self, x, uint16_t a):
		return [self.mul(b, a) for b in x]
	
	cpdef poly_eval(self, x, uint16_t a):
		cdef uint16_t b
		result = x[0]
		for b in x[1:]:
			result = self.mul(result, a) ^ b
		return result
	
	cpdef poly_add(self, x, y):
		cdef uint16_t i, a, b
		cdef uint16_t lx, ly
		result = [0] * max(len(x), len(y))
		lx = len(result) - len(x)
		ly = len(result) - len(y)
		for i, a in enumerate(x):
			result[i + lx] = a
		for i, b in enumerate(y):
			result[i + ly] ^= b
		return result
	
	cpdef poly_mul(self, x, y):
		cdef uint16_t i, j, a, b
		result = [0] * (len(x) + len(y) - 1)
		for i, a in enumerate(x):
			for j, b in enumerate(y):
				result[i + j] ^= self.mul(a, b)
		return result
	
	cpdef poly_div(self, x, y):
		cdef uint16_t i, j, coeff
		out = list(x)
		for i in range(len(x) - (len(y) - 1)):
			coeff = out[i]
			if coeff != 0:
				for j in range(1, len(y)):
					if y[j] != 0:
						out[i + j] ^= self.mul(y[j], coeff)
		sep = -(len(y)-1)
		return out[:sep], out[sep:]
	
	cpdef gen_rs_code(self, data, uint16_t n):
		if len(data) + n > self.fieldsize:
			raise ValueError("Message is too long (%i when max is %i)" % (len(data) + n, self.fieldsize - 1))
		gen = self.generator(n)
		_, code = self.poly_div(data + [0] * (len(gen)-1), gen)
		return code

class GalloisField(Enum):
	GF16 = _GF(4, MODE_MESSAGE, MODE_MESSAGE, 0x13)
	GF64 = _GF(6, 1, 2, 0x43)
	GF256 = _GF(8, 3, 8, 0x12D)
	GF1024 = _GF(10, 9, 22, 0x409)
	GF4096 = _GF(12, 23, 32, 0x1096)

	@classmethod
	def getFieldForLayers(cls, layers):
		if layers <= 0:
			return cls.GF16
		for f in cls:
			if layers >= f.value.minlayers and layers <= f.value.maxlayers:
				return f
		return None
