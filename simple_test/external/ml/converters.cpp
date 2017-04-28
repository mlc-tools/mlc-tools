#include "converters.h"
#include <sstream>
#include <stdio.h>

std::string boolToStr(bool value)
{
	return value ? "yes" : "no";
};

std::string intToStr(int value)
{
	static char buffer[32];
	buffer[0] = 0x0;
	sprintf(buffer, "%d", value);
	
	return buffer;
};

std::string floatToStr(float value)
{
	static char buffer[32];
	buffer[0] = 0x0;
	sprintf(buffer, "%.2f", value);
	return buffer;
};

std::string floatToStr2(float value)
{
	static char buffer[32];
	buffer[0] = 0x0;
	sprintf(buffer, "%f", value);
	return buffer;
};

bool strToBool(const std::string & value)
{
	if (value.empty())
		return false;
	bool result(false);
	result = result || value == "yes";
	result = result || value == "Yes";
	result = result || value == "true";
	result = result || value == "True";
	return result;
}

int strToInt(const std::string & value)
{
	return value.empty() ? 0 :
		atoi(value.c_str());
}

float strToFloat(const std::string & value)
{
	return value.empty() ? 0 :
		atof(value.c_str());
}

