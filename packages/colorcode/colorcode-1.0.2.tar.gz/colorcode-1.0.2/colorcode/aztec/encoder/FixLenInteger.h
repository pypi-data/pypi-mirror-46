#pragma once

#include <cstdint>
#include <vector>

class FixLenInteger {
	
	public:
	
	FixLenInteger(const FixLenInteger&) = default;
	FixLenInteger(FixLenInteger&&) = default;
	FixLenInteger& operator=(const FixLenInteger&) = default;
	FixLenInteger& operator=(FixLenInteger&&) = default;
	
	inline FixLenInteger() : bits(64), value(0) {}
	
	inline FixLenInteger(uint8_t bits) : bits(bits), value(0) {}
	
	FixLenInteger(uint8_t bits, uint64_t value);
	
	std::vector<bool> asVector() const;
	void appendTo(std::vector<bool>& vect) const;
	
	inline uint8_t getbits() const { return this->bits; }
	inline uint64_t getvalue() const { return this->value; }
	
	private:
	uint8_t bits;
	uint64_t value;
};