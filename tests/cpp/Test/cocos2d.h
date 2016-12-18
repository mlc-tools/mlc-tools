#ifndef __cocos2d_h__
#define __cocos2d_h__
#include <algorithm>

namespace cocos2d
{
	class Point
	{
	public:
		float x;
		float y;

		Point( float x = 0, float y = 0 )
		{
			this->x = x;
			this->y = y;
		}

		bool operator == (const Point& rhs)const
		{
			return std::fabs( x - rhs.x ) < 0.001 && std::fabs( y - rhs.y ) < 0.001;
		}
		
		Point operator + (const Point& rhs)const
		{
			Point p;
			p.x = x + rhs.x;
			p.y = y + rhs.y;
			return p;
		}
		Point operator - (const Point& rhs)const
		{
			Point p;
			p.x = x - rhs.x;
			p.y = y - rhs.y;
			return p;
		}
		Point operator * (float rhs)const
		{
			Point p;
			p.x = x * rhs;
			p.y = y * rhs;
			return p;
		}

		float getDistance( const Point& p )const
		{
			auto xx = p.x - x;
			auto yy = p.y - y;
			return std::sqrt( xx*xx + yy*yy );
		}
		float getDistanceSq( const Point& p )const
		{
			auto xx = p.x - x;
			auto yy = p.y - y;
			return ( xx*xx + yy*yy );
		}

	};
}

#endif