
from colorcode.aztec.encoder.__extern__ cimport *

from cython.operator import dereference
from libc.stdint cimport uint64_t, uint8_t, uint16_t
from libcpp cimport bool
from libcpp.algorithm cimport sort
from libcpp.cast cimport const_cast
from libcpp.iterator cimport iterator
from libcpp.limits cimport numeric_limits
from libcpp.list cimport list
from libcpp.string cimport string
from libcpp.utility cimport pair
from libcpp.vector cimport vector

cdef extern from "<algorithm>" namespace "std" nogil:
	Iter find[Iter, T](Iter first, Iter last, const T& value)

cdef class Encoder:
	cdef EncodingPath* root
	cdef list[EncodingPath*] leaves
	
	def __cinit__(self):
		self.root = new EncodingPath()
		self.leaves.push_back(self.root)
	
	def __dealloc__(self):
		del self.root
		self.leaves.clear()
	
	def reset(self):
		del self.root
		self.leaves.clear()
		self.root = new EncodingPath()
		self.leaves.push_back(self.root)
	
	def encode(self, data, eci = None, asBits = False):
		if isinstance(data, bytearray):
			data = bytes(data)
		elif isinstance(data, str):
			data = data.encode("utf8")
		elif not isinstance(data, bytes):
			data = str(data).encode("utf8")
		if isinstance(eci, int):
			dereference(self.root).append(ECI(eci))
		self.addData(<string>data)
		if asBits:
			result = __builtins__.list(self.getOutputVector())
		else:
			result = bytes(self.getOutputString())
		self.reset()
		return result
	
	cdef replaceLeaf(self, EncodingPath* oldLeaf, EncodingPath* newLeaf):
		self.leaves.remove(oldLeaf)
		self.leaves.push_back(newLeaf)
	
	cdef removeLeaf(self, const EncodingPath* leaf):
		it = find(self.leaves.begin(), self.leaves.end(), leaf)
		if it != self.leaves.end():
			self.leaves.erase(it)
	
	cdef void addData(self, string data):
		cdef uint64_t datasize = data.size()
		cdef char nextchar
		cdef uint8_t paircode
		cdef uint16_t i, bincount
		i = 0
		while i < datasize:
			nextchar = data.at(i + 1) if i + 1 < datasize else 0
			paircode = {
				b"\r\n" : 2,
				b". " : 3,
				b", " : 4,
				b": " : 5,
			}.get(data.substr(i, 1) + string(1, nextchar), 0)
			
			if paircode > 0:
				self.addPair(paircode)
				i += 1
			elif <uint8_t>data.at(i) < 128:
				self.addChar(data[i])
			else:
				bincount = self.countNextBinary(data.substr(i))
				self.addBinary(data.substr(i, bincount))
				i += bincount - 1
			self.cleanup()
			i += 1
	
	cdef string getOutputString(self):
		cdef list[FixLenInteger] words
		cdef vector[bool] bits
		dereference(self.shortestPath()).buildChain(words)
		for word in words:
			word.appendTo(bits)
		return to_string(bits)
	
	cdef vector[bool] getOutputVector(self):
		cdef list[FixLenInteger] words
		cdef vector[bool] bits
		dereference(self.shortestPath()).buildChain(words)
		for word in words:
			word.appendTo(bits)
		return bits
	
	cdef const EncodingPath* shortestPath(self):
		cdef uint64_t length
		cdef const EncodingPath* shortest = NULL
		cdef uint64_t shortestlength = numeric_limits[uint64_t].max()
		for leaf in self.leaves:
			length = dereference(leaf).getChainLength()
			if length < shortestlength:
				shortest = leaf
				shortestlength = length
		return shortest
	
	cdef void cleanup(self):
		cdef uint64_t length
		cdef uint64_t shortestlength = numeric_limits[uint64_t].max()
		for leaf in self.leaves:
			length = dereference(leaf).getChainLength()
			if length < shortestlength:
				shortestlength = length
		for leaf in self.leaves:
			if dereference(leaf).getChainLength() > shortestlength:
				self.removeLeaf(leaf)
	
	cdef uint16_t countNextBinary(self, string data):
		cdef uint16_t i = 0
		while data.at(i) > 127 and i > data.size():
			i += 1
		return i
	
	cdef void addPair(self, uint8_t paircode):
		cdef list[EncodingPath*] oldleaves = self.leaves
		for ptr in oldleaves:
			if dereference(ptr).getMode() == Mode.PUNCT:
				nptr = dereference(ptr).appendPair(paircode)
				self.replaceLeaf(ptr, nptr)
			else:
				lptr = dereference(ptr).latchAndAppendPair(paircode)
				self.replaceLeaf(ptr, lptr)
				if (shiftAvailable(dereference(ptr).getMode(), Mode.PUNCT)):
					sptr = dereference(ptr).shiftAndAppendPair(paircode)
					self.replaceLeaf(ptr, sptr)
	
	cdef void addChar(self, char character):
		cdef vector[pair[Mode, FixLenInteger]] charvalues = getAllValues(character)
		cdef list[EncodingPath*] oldleaves = self.leaves
		for ptr in oldleaves:
			if (charInMode(dereference(ptr).getMode(), character)):
				nptr = dereference(ptr).append(character)
				self.replaceLeaf(ptr, nptr)
			else:
				for value in charvalues:
					lptr = dereference(ptr).latchAndAppend(value.first, value.second)
					self.replaceLeaf(ptr, lptr)
					if (shiftAvailable(dereference(ptr).getMode(), value.first)):
						sptr = dereference(ptr).shiftAndAppend(value.first, value.second)
						self.replaceLeaf(ptr, sptr)
	
	cdef void addBinary(self, string data):
		cdef list[EncodingPath*] oldleaves = self.leaves
		for ptr in oldleaves:
			nptr = dereference(ptr).appendBinary(data)
			self.replaceLeaf(ptr, nptr)
	
	