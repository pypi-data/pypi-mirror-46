
#include "Constants.h"

#include "Mode.h"
#include "FixLenInteger.h"

#include <map>
#include <utility>
#include <array>
#include <string>
#include <cstdint>

const std::map<std::pair<Mode, Mode>, FixLenInteger> LATCH_TABLE {
	std::make_pair(std::make_pair(Mode::UPPER, Mode::UPPER), FixLenInteger(0, 0)),
	std::make_pair(std::make_pair(Mode::UPPER, Mode::LOWER), FixLenInteger(5, 28)),
	std::make_pair(std::make_pair(Mode::UPPER, Mode::DIGIT), FixLenInteger(5, 30)),
	std::make_pair(std::make_pair(Mode::UPPER, Mode::PUNCT), FixLenInteger(10, (29 << 5) + 30)),
	std::make_pair(std::make_pair(Mode::UPPER, Mode::MIXED), FixLenInteger(5, 29)),
	
	std::make_pair(std::make_pair(Mode::LOWER, Mode::UPPER), FixLenInteger(9, (30 << 4) + 14)),
	std::make_pair(std::make_pair(Mode::LOWER, Mode::LOWER), FixLenInteger(0, 0)),
	std::make_pair(std::make_pair(Mode::LOWER, Mode::DIGIT), FixLenInteger(5, 30)),
	std::make_pair(std::make_pair(Mode::LOWER, Mode::PUNCT), FixLenInteger(10, (29 << 5) + 30)),
	std::make_pair(std::make_pair(Mode::LOWER, Mode::MIXED), FixLenInteger(5, 29)),
	
	std::make_pair(std::make_pair(Mode::DIGIT, Mode::UPPER), FixLenInteger(4, 14)),
	std::make_pair(std::make_pair(Mode::DIGIT, Mode::LOWER), FixLenInteger(9, (14 << 5) + 28)),
	std::make_pair(std::make_pair(Mode::DIGIT, Mode::DIGIT), FixLenInteger(0, 0)),
	std::make_pair(std::make_pair(Mode::DIGIT, Mode::PUNCT), FixLenInteger(14, (14 << 10) + (29 << 5) + 30)),
	std::make_pair(std::make_pair(Mode::DIGIT, Mode::MIXED), FixLenInteger(9, (14 << 5) + 29)),
	
	std::make_pair(std::make_pair(Mode::PUNCT, Mode::UPPER), FixLenInteger(5, 31)),
	std::make_pair(std::make_pair(Mode::PUNCT, Mode::LOWER), FixLenInteger(10, (31 << 5) + 28)),
	std::make_pair(std::make_pair(Mode::PUNCT, Mode::DIGIT), FixLenInteger(10, (31 << 5) + 30)),
	std::make_pair(std::make_pair(Mode::PUNCT, Mode::PUNCT), FixLenInteger(0, 0)),
	std::make_pair(std::make_pair(Mode::PUNCT, Mode::MIXED), FixLenInteger(10, (31 << 5) + 29)),
	
	std::make_pair(std::make_pair(Mode::MIXED, Mode::UPPER), FixLenInteger(5, 29)),
	std::make_pair(std::make_pair(Mode::MIXED, Mode::LOWER), FixLenInteger(5, 28)),
	std::make_pair(std::make_pair(Mode::MIXED, Mode::DIGIT), FixLenInteger(10, (29 << 5) + 30)),
	std::make_pair(std::make_pair(Mode::MIXED, Mode::PUNCT), FixLenInteger(5, 30)),
	std::make_pair(std::make_pair(Mode::MIXED, Mode::MIXED), FixLenInteger(0, 0)),
};

const std::map<std::pair<Mode, Mode>, FixLenInteger> SHIFT_TABLE {
	std::make_pair(std::make_pair(Mode::UPPER, Mode::PUNCT), FixLenInteger(5, 0)),
	
	std::make_pair(std::make_pair(Mode::LOWER, Mode::UPPER), FixLenInteger(5, 28)),
	std::make_pair(std::make_pair(Mode::LOWER, Mode::PUNCT), FixLenInteger(5, 0)),
	
	std::make_pair(std::make_pair(Mode::DIGIT, Mode::UPPER), FixLenInteger(4, 15)),
	std::make_pair(std::make_pair(Mode::DIGIT, Mode::PUNCT), FixLenInteger(4, 0)),
	
	std::make_pair(std::make_pair(Mode::MIXED, Mode::PUNCT), FixLenInteger(5, 0)),
};

const std::map<std::pair<Mode, uint8_t>, FixLenInteger> CHAR_MAP {
#include "charmap.inc"
};

const std::array<Mode, 5> MODE_LIST {Mode::UPPER, Mode::LOWER, Mode::DIGIT, Mode::PUNCT, Mode::MIXED};

const FixLenInteger FNC1 (8, 0);

FixLenInteger ECI(uint32_t code) {
	std::string digits = std::to_string(code % 1000000);
	uint64_t value = digits.size();
	for (uint8_t i = 0; i < digits.size(); i++) {
		value <<= 4;
		value += CHAR_MAP.at(std::make_pair(Mode::DIGIT, static_cast<uint8_t>(digits.at(i)))).getvalue();
	}
	return FixLenInteger(8 + 4 * static_cast<uint8_t>(digits.size()), value);
}