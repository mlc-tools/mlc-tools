/******************************************************************************/
/*
* Copyright 2014-2015 Vladimir Tolmachev
*
* Author: Vladimir Tolmachev
* Project: ml
* e-mail: tolm_vl@hotmail.com
* If you received the code is not the author, please contact me
*/
/******************************************************************************/

#include <cstdint>
#include "Generics.h"
#include <sstream>
#include "cocos2d.h"

// from string

std::string boolToStr( bool value )
{
	return value ? "yes" : "no";
};

std::string intToStr( int value )
{
	static char buffer[32];
	buffer[0] = 0x0;
	sprintf_s( buffer, "%d", value );
	return buffer;
};

std::string floatToStr( float value )
{
	static char buffer[32];
	buffer[0] = 0x0;
	sprintf_s( buffer, "%.2f", value );
	return buffer;
};

bool strToBool( const std::string & value )
{
	if( value.empty() )
		return false;
	bool result( false );
	result = result || value == "yes";
	result = result || value == "Yes";
	result = result || value == "true";
	result = result || value == "True";
	return result;
}

int strToInt( const std::string & value )
{
	return value.empty() ? 0 :
		atoi( value.c_str() );
}

float strToFloat( const std::string & value )
{
	std::stringstream ss( value );
	float result( 0 );
	if( value.empty() == false )
		ss >> result;
	return result;
}
template <> std::string strTo(const std::string &value)
{
	return value;
}
template <> float strTo(const std::string &value)
{
	return strToFloat(value);
}
template <> int32_t strTo(const std::string &value)
{
	return strToInt(value);
}
template <> int64_t strTo(const std::string &value)
{
	return strToInt(value);
}
template <> uint32_t strTo(const std::string &value)
{
	return static_cast<uint32_t>(strToInt(value));
}
template <> uint64_t strTo(const std::string &value)
{
	return static_cast<uint64_t>(strToInt(value));
}
template <> bool strTo( const std::string &value )
{
	return strToBool( value );
}
template <> cocos2d::Point strTo( const std::string &value )
{
	int k = value.find( "x" );
	if( k != std::string::npos )
	{
		cocos2d::Point p;
		p.x = strTo<float>( value.substr( 0, k ) );
		p.y = strTo<float>( value.substr( k + 1 ) );
		return p;
	}
	return cocos2d::Point();
}

// to string

template <> std::string toStr(std::string value)
{
	return value;
}
template <> std::string toStr( char const * value )
{
	return std::string( value ? value : "" );
}
template <> std::string toStr(const std::string &value)
{
	return value;
}
template <> std::string toStr(int value)
{
	return intToStr(value);
}
template <> std::string toStr(long value)
{
	return intToStr(value);
}
template <> std::string toStr(long long value)
{
	return intToStr(static_cast<int>(value));
}
template <> std::string toStr(unsigned int value)
{
	return intToStr(static_cast<int>(value));
}
template <> std::string toStr( unsigned long value)
{
	return intToStr(static_cast<int>(value));
}
template <> std::string toStr( unsigned long long value)
{
	return intToStr( static_cast<int>(value));
}
template <> std::string toStr(bool value)
{
	return boolToStr( value );
}
template <> std::string toStr( float value )
{
	return floatToStr( value );
}
template <> std::string toStr( cocos2d::Point value )
{
	return floatToStr( value.x ) + "x" + floatToStr(value.y);
}
