
from libc.stdint cimport uint64_t, uint8_t, uint32_t
from libcpp.vector cimport vector
from libcpp.list cimport list
from libcpp.utility cimport pair
from libcpp cimport bool
from libcpp.string cimport string
from libcpp.map cimport map

cdef extern from "Mode.h":
	ctypedef enum Mode:
		UPPER "Mode::UPPER"
		LOWER "Mode::LOWER"
		DIGIT "Mode::DIGIT"
		PUNCT "Mode::PUNCT"
		MIXED "Mode::MIXED"
		BINARY "Mode::BINARY"

cdef extern from "FixLenInteger.h":
	cdef cppclass FixLenInteger:
		FixLenInteger() except +
		FixLenInteger(uint8_t) except +
		FixLenInteger(uint8_t, uint64_t) except +
		vector[bool] asVector()
		void appendTo(vector[bool]& vect)
		uint8_t getbits()
		uint64_t getvalue()

cdef extern from "Constants.h":
	cdef const map[pair[Mode, Mode], FixLenInteger] LATCH_TABLE
	cdef const map[pair[Mode, Mode], FixLenInteger] SHIFT_TABLE
	cdef const map[pair[Mode, uint8_t], FixLenInteger] CHAR_MAP
	cdef const FixLenInteger FNC1
	FixLenInteger ECI(uint32_t code)

cdef extern from "EncodingPath.h":
	cdef cppclass EncodingPath:
		EncodingPath* append(char character)
		EncodingPath* append(const FixLenInteger& word)
		EncodingPath* append(const list[FixLenInteger]& words)
		EncodingPath* appendPair(uint8_t paircode)
		EncodingPath* shiftAndAppend(Mode mode, const FixLenInteger& word)
		EncodingPath* latchAndAppend(Mode mode, const FixLenInteger& word)
		EncodingPath* latchAndAppend(Mode mode, const list[FixLenInteger]& words)
		EncodingPath* latchAndAppend(Mode mode, list[FixLenInteger]&& words)
		EncodingPath* shiftAndAppendPair(uint8_t paircode)
		EncodingPath* latchAndAppendPair(uint8_t paircode)
		EncodingPath* appendBinary(string data)
		
		Mode getMode()
		uint64_t getCurrentLength()
		uint64_t getChainLength()
		list[FixLenInteger] getChain()
		void buildChain(list[FixLenInteger]& chain)
		
		map[const EncodingPath*, uint64_t] getLengthTable()
		void buildLengthTable(map[const EncodingPath*, uint64_t]& table)

cdef extern from "Utility.h":
	bool charInMode(Mode mode, char character)
	bool shiftAvailable(Mode start, Mode destination)
	vector[pair[Mode, FixLenInteger]] getAllValues(char character)
	vector[pair[Mode, FixLenInteger]] getAllShifts(Mode start)
	vector[pair[Mode, FixLenInteger]] getAllLatches(Mode start)
	string to_string(const vector[bool]& bitvector)