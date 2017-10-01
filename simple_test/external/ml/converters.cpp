/******************************************************************************/
/*
* Copyright 2014-2017 Vladimir Tolmachev
*
* Author: Vladimir Tolmachev
* Project: ml
* e-mail: tolm_vl@hotmail.com
* If you received the code is not the author, please contact me
*/
/******************************************************************************/

#include "converters.h"
#include <sstream>
#include <stdio.h>

std::string boolToStr(bool value)
{
	return value ? "yes" : "no";
};

std::string intToStr(int value)
{
	std::stringstream ss;
	ss << value;
	return ss.str();
};

std::string floatToStr(float value)
{
	std::stringstream ss;
	ss << value;
	return ss.str();
};

std::string floatToStr2(float value)
{
	std::stringstream ss;
	ss << value;
	return ss.str();
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
	std::stringstream ss(value);
	int result(0);
	ss >> result;
	return result;
}

float strToFloat(const std::string & value)
{
	std::stringstream ss(value);
	float result(0.f);
	ss >> result;
	return result;
}

