
#include "FixLenInteger.h"

#include <cstdint>
#include <vector>

FixLenInteger::FixLenInteger(uint8_t bits, uint64_t value) : bits(bits) {
#ifdef EXCEPTIONS
	if (value >= (1 << bits)) {
		throw std::invalid_argument("Value " + std::to_string(value) +
			" is too large for a " + std::to_string(bits) + " bits integer.");
	} else {
#endif // EXCEPTIONS
		this->value = value;
#ifdef EXCEPTIONS
	}
#endif // EXCEPTIONS
}
	
std::vector<bool> FixLenInteger::asVector() const {
	std::vector<bool> result;
	for (uint64_t i = (uint64_t)1 << (this->bits - 1); i > 0; i >>= 1) {
		result.push_back((this->value & i) != 0);
	}
	return result;
}

void FixLenInteger::appendTo(std::vector<bool>& vect) const {
	for (uint64_t i = (uint64_t)1 << (this->bits - 1); i > 0; i >>= 1) {
		vect.push_back((this->value & i) != 0);
	}
}