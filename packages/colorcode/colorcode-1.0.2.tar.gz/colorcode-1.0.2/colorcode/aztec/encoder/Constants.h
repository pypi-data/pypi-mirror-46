#pragma once

#include "Mode.h"
#include "FixLenInteger.h"

#include <map>
#include <utility>
#include <array>
#include <cstdint>

extern const std::map<std::pair<Mode, Mode>, FixLenInteger> LATCH_TABLE;
extern const std::map<std::pair<Mode, Mode>, FixLenInteger> SHIFT_TABLE;
extern const std::map<std::pair<Mode, uint8_t>, FixLenInteger> CHAR_MAP;
extern const std::array<Mode, 5> MODE_LIST;
extern const FixLenInteger FNC1;
FixLenInteger ECI(uint32_t code);