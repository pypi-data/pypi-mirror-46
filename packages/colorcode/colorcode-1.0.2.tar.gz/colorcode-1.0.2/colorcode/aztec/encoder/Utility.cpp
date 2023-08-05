
#include "Utility.h"

#include "Mode.h"
#include "FixLenInteger.h"
#include "Constants.h"

#include <vector>
#include <utility>
#include <string>


bool charInMode(Mode mode, char character) {
	auto it = CHAR_MAP.find(std::make_pair(mode, character));
	return it != CHAR_MAP.end();
}

std::vector<std::pair<Mode, FixLenInteger>> getAllValues(char character) {
	std::vector<std::pair<Mode, FixLenInteger>> result;
	for (auto const& mode : MODE_LIST) {
		auto it = CHAR_MAP.find(std::make_pair(mode, character));
		if (it != CHAR_MAP.end()) {
			result.push_back(std::make_pair(mode, it->second));
		}
	}
	return result;
}

bool shiftAvailable(Mode start, Mode destination){
	auto it = SHIFT_TABLE.find(std::make_pair(start, destination));
	return it != SHIFT_TABLE.end();
}

std::vector<std::pair<Mode, FixLenInteger>> getAllShifts(Mode start) {
	std::vector<std::pair<Mode, FixLenInteger>> result;
	for (auto const& destination : MODE_LIST) {
		auto it = SHIFT_TABLE.find(std::make_pair(start, destination));
		if (it != SHIFT_TABLE.end()) {
			result.push_back(std::make_pair(destination, it->second));
		}
	}
	return result;
}

std::vector<std::pair<Mode, FixLenInteger>> getAllLatches(Mode start) {
	std::vector<std::pair<Mode, FixLenInteger>> result;
	for (auto const& destination : MODE_LIST) {
		auto it = LATCH_TABLE.find(std::make_pair(start, destination));
		if (it != LATCH_TABLE.end()) {
			result.push_back(std::make_pair(destination, it->second));
		}
	}
	return result;
}

std::string to_string(const std::vector<bool>& bitvector) {
    std::string result((bitvector.size() + 7) / 8, 0);
    auto out = result.begin();
    uint8_t shift = 0;
    for (bool bit : bitvector) {
        *out |= bit << shift;
        if (++shift == 8) {
            ++out;
            shift = 0;
        }
    }
    return result;
}

