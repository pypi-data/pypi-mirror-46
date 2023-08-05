#pragma once

#include "Mode.h"
#include "FixLenInteger.h"

#include <utility>
#include <vector>
#include <string>

bool charInMode(Mode mode, char character);
bool shiftAvailable(Mode start, Mode destination);
std::vector<std::pair<Mode, FixLenInteger>> getAllValues(char character);
std::vector<std::pair<Mode, FixLenInteger>> getAllShifts(Mode start);
std::vector<std::pair<Mode, FixLenInteger>> getAllLatches(Mode start);
std::string to_string(const std::vector<bool>& bitvector);