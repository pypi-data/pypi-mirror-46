
#include "EncodingPath.h"

#include "Mode.h"
#include "FixLenInteger.h"
#include "Constants.h"

#include <list>
#include <cstdint>
#include <string>
#include <map>
#include <algorithm>

static inline std::list<FixLenInteger> buildFromBinary(std::string data) {
	std::list<FixLenInteger> result;
	for (auto it = data.begin(); it != data.end(); it++) {
		result.emplace_back(8, static_cast<uint8_t>(*it));
	}
	return result;
}

static inline FixLenInteger buildBinarySize(uint16_t datasize) {
	uint64_t value = 31 << 5;
	uint8_t size = 10;
	if (datasize < 32) {
		value += datasize & 0x1F;
	} else {
		size += 11;
		value = (value << 11) + ((datasize - 31) & 0x7FF);
	}
	return FixLenInteger(size, value);
}

EncodingPath::EncodingPath() :
	currentMode(Mode::UPPER),
	parent(nullptr),
	currentElements(),
	children() {}

EncodingPath::EncodingPath(EncodingPath* parent) :
	currentMode(Mode::UPPER),
	parent(parent),
	currentElements(),
	children() {}

EncodingPath::EncodingPath(Mode mode) :
	currentMode(mode),
	parent(nullptr),
	currentElements(),
	children() {}

EncodingPath::EncodingPath(Mode mode, EncodingPath* parent) :
	currentMode(mode),
	parent(parent),
	currentElements(),
	children() {}
	
EncodingPath::EncodingPath(Mode mode, EncodingPath* parent, const std::list<FixLenInteger>& words) :
	currentMode(mode),
	parent(parent),
	currentElements(words),
	children() {}
	
EncodingPath::EncodingPath(Mode mode, EncodingPath* parent, std::list<FixLenInteger>&& words) :
	currentMode(mode),
	parent(parent),
	currentElements(std::move(words)),
	children() {}

EncodingPath::~EncodingPath() {
	for (auto const& child : this->children) {
		delete child;
	}
}

EncodingPath* EncodingPath::append(char character) {
	auto it = CHAR_MAP.find(std::make_pair(this->currentMode, character));
#ifdef EXCEPTIONS
	if (it == CHAR_MAP.end()) {
		throw std::invalid_argument("Character " + character + " does not exist in current mode");
	}
#endif // EXCEPTIONS
	this->currentElements.push_back(it->second);
	return this;
}

EncodingPath* EncodingPath::append(const FixLenInteger& word) {
	this->currentElements.push_back(word);
	return this;
}

EncodingPath* EncodingPath::append(const std::list<FixLenInteger>& words) {
	this->currentElements.insert(this->currentElements.end(), words.begin(), words.end());
	return this;
}

EncodingPath* EncodingPath::appendPair(uint8_t paircode) {
	if (this->currentMode != Mode::PUNCT) {
#ifdef EXCEPTIONS
		throw std::logic_error("Cannot append a pair when not in PUNCT mode");
#else // EXCEPTIONS
		return this->latchAndAppendPair(paircode);
#endif // EXCEPTIONS
	}
	this->currentElements.push_back(FixLenInteger(5, paircode));
	return this;
}

EncodingPath* EncodingPath::shiftAndAppend(Mode mode, const FixLenInteger& word) {
	auto it = SHIFT_TABLE.find(std::make_pair(this->currentMode, mode));
#ifdef EXCEPTIONS
	if (it == SHIFT_TABLE.end()) {
		throw std::invalid_argument("Requested mode shift impossible");
	}
#endif // EXCEPTIONS
	std::list<FixLenInteger> words {it->second, word};
	EncodingPath* newleaf = new EncodingPath(this->currentMode, this, words);
	this->children.push_back(newleaf);
	return newleaf;
}

EncodingPath* EncodingPath::latchAndAppend(Mode mode, const FixLenInteger& word) {
	auto it = LATCH_TABLE.find(std::make_pair(this->currentMode, mode));
#ifdef EXCEPTIONS
	if (it == LATCH_TABLE.end()) {
		throw std::invalid_argument("Requested mode shift impossible");
	}
#endif // EXCEPTIONS
	std::list<FixLenInteger> words {it->second, word};
	EncodingPath* newleaf = new EncodingPath(mode, this, words);
	this->children.push_back(newleaf);
	return newleaf;
}

EncodingPath* EncodingPath::latchAndAppend(Mode mode, const std::list<FixLenInteger>& words) {
	auto it = LATCH_TABLE.find(std::make_pair(this->currentMode, mode));
#ifdef EXCEPTIONS
	if (it == LATCH_TABLE.end()) {
		throw std::invalid_argument("Requested mode shift impossible");
	}
#endif // EXCEPTIONS
	std::list<FixLenInteger> words_copy (words);
	words_copy.push_front(it->second);
	EncodingPath* newleaf = new EncodingPath(mode, this, std::move(words_copy));
	this->children.push_back(newleaf);
	return newleaf;
}

EncodingPath* EncodingPath::latchAndAppend(Mode mode, std::list<FixLenInteger>&& words) {
	auto it = LATCH_TABLE.find(std::make_pair(this->currentMode, mode));
#ifdef EXCEPTIONS
	if (it == LATCH_TABLE.end()) {
		throw std::invalid_argument("Requested mode shift impossible");
	}
#endif // EXCEPTIONS
	words.push_front(it->second);
	EncodingPath* newleaf = new EncodingPath(mode, this, std::move(words));
	this->children.push_back(newleaf);
	return newleaf;
}

EncodingPath* EncodingPath::shiftAndAppendPair(uint8_t paircode) {
	auto it = SHIFT_TABLE.find(std::make_pair(this->currentMode, Mode::PUNCT));
#ifdef EXCEPTIONS
	if (it == SHIFT_TABLE.end()) {
		throw std::invalid_argument("Requested mode shift impossible");
	}
#endif // EXCEPTIONS
	EncodingPath* newleaf = new EncodingPath(this->currentMode, this, std::list<FixLenInteger> { it->second, FixLenInteger(5, paircode) });
	this->children.push_back(newleaf);
	return newleaf;
}

EncodingPath* EncodingPath::latchAndAppendPair(uint8_t paircode) {
	auto it = LATCH_TABLE.find(std::make_pair(this->currentMode, Mode::PUNCT));
#ifdef EXCEPTIONS
	if (it == LATCH_TABLE.end()) {
		throw std::invalid_argument("Requested mode shift impossible");
	}
#endif // EXCEPTIONS
	EncodingPath* newleaf = new EncodingPath(Mode::PUNCT, this, std::list<FixLenInteger> { it->second, FixLenInteger(5, paircode) });
	this->children.push_back(newleaf);
	return newleaf;
}

EncodingPath* EncodingPath::appendBinary(std::string data) {
	EncodingPath* result;
	std::list<FixLenInteger> words = buildFromBinary(data);
	words.push_front(buildBinarySize(static_cast<uint16_t>(data.size() & 0xFFFF)));
	switch (this->currentMode) {
		case Mode::DIGIT:
		case Mode::PUNCT:
			words.push_front(LATCH_TABLE.at(std::make_pair(this->currentMode, Mode::UPPER)));
			result = new EncodingPath(Mode::UPPER, this, std::move(words));
			break;
		case Mode::UPPER:
		case Mode::LOWER:
		case Mode::MIXED:
		default:
			result = new EncodingPath(this->currentMode, this, std::move(words));
			break;
	}
	this->children.push_back(result);
	return result;
}

Mode EncodingPath::getMode() const {
	return this->currentMode;
}

uint64_t EncodingPath::getCurrentLength() const {
	uint64_t len = 0;
	for (auto const& item : this->currentElements) {
		len += item.getbits();
	}
	return len;
}

uint64_t EncodingPath::getChainLength() const {
	uint64_t len = 0;
	for (const EncodingPath* ptr = this; ptr != nullptr; ptr = ptr->parent) {
		len+= ptr->getCurrentLength();
	}
	return len;
}

std::list<FixLenInteger> EncodingPath::getChain() const {
	std::list<FixLenInteger> result;
	this->buildChain(result);
	return result;
}

void EncodingPath::buildChain(std::list<FixLenInteger>& chain) const{
	for (const EncodingPath* ptr = this; ptr != nullptr; ptr = ptr->parent) {
		chain.insert(chain.begin(), ptr->currentElements.begin(), ptr->currentElements.end());
	}
}
	
std::map<const EncodingPath*, uint64_t> EncodingPath::getLengthTable() const {
	std::map<const EncodingPath*, uint64_t> result;
	this->buildLengthTable(result);
	return result;
}

void EncodingPath::buildLengthTable(std::map<const EncodingPath*, uint64_t>& table) const {
	this->buildLengthTable(table, 0);
}

void EncodingPath::buildLengthTable(std::map<const EncodingPath*, uint64_t>& table, uint64_t currentLength) const {
	if (this->children.empty()) {
		table.insert(std::make_pair(this, currentLength + this->getCurrentLength()));
		return;
	}
	currentLength += this->getCurrentLength();
	for (auto const& child : this->children) {
		child->buildLengthTable(table, currentLength);
	}
}

void EncodingPath::forgetChild(const EncodingPath* child) {
	auto it = std::find(this->children.begin(), this->children.end(), child);
	if (it != this->children.end()) {
		this->children.erase(it);
	}
}