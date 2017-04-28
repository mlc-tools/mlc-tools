#ifndef __ml_CONVERTERS_h__
#define __ml_CONVERTERS_h__
#include <string>

bool strToBool(const std::string &value);
std::string boolToStr(bool value);

int strToInt(const std::string &value);
std::string intToStr(int value);

float strToFloat(const std::string &value);
std::string floatToStr(float value);
std::string floatToStr2(float value);

#endif
