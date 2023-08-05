#pragma once

#include "Mode.h"
#include "FixLenInteger.h"

#include <list>
#include <cstdint>
#include <string>
#include <map>

class EncodingPath {
	
	public:
	
	const Mode currentMode;
	EncodingPath * const parent;
	
	EncodingPath();
	EncodingPath(Mode mode);
	EncodingPath(EncodingPath* parent);
	EncodingPath(Mode mode, EncodingPath* parent);
	EncodingPath(Mode mode, EncodingPath* parent, const std::list<FixLenInteger>& words);
	EncodingPath(Mode mode, EncodingPath* parent, std::list<FixLenInteger>&& words);
	
	~EncodingPath();
	
	EncodingPath* append(char character);
	EncodingPath* append(const FixLenInteger& word);
	EncodingPath* append(const std::list<FixLenInteger>& words);
	EncodingPath* appendPair(uint8_t paircode);
	EncodingPath* shiftAndAppend(Mode mode, const FixLenInteger& word);
	EncodingPath* latchAndAppend(Mode mode, const FixLenInteger& word);
	EncodingPath* latchAndAppend(Mode mode, const std::list<FixLenInteger>& words);
	EncodingPath* latchAndAppend(Mode mode, std::list<FixLenInteger>&& words);
	EncodingPath* shiftAndAppendPair(uint8_t paircode);
	EncodingPath* latchAndAppendPair(uint8_t paircode);
	EncodingPath* appendBinary(std::string data);
	
	Mode getMode() const;
	
	uint64_t getCurrentLength() const;
	uint64_t getChainLength() const;
	
	std::list<FixLenInteger> getChain() const;
	void buildChain(std::list<FixLenInteger>& chain) const;
	
	std::map<const EncodingPath*, uint64_t> getLengthTable() const;
	void buildLengthTable(std::map<const EncodingPath*, uint64_t>& table) const;
	
	private:
	void forgetChild(const EncodingPath*);
	void buildLengthTable(std::map<const EncodingPath*, uint64_t>& table, uint64_t currentLength) const;
	
	std::list<FixLenInteger> currentElements;
	std::list<EncodingPath*> children;
};