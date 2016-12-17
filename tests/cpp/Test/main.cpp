#include "../../../out/RequestScore.h"
#include "../../../out/SerializedObject.h"
#include "../../../out/IVisitorRequest.h"

using namespace mg;

class Visitor : public IVisitorRequest
{
	virtual void visit( Request* ctx )
	{
	}

	virtual void visit( RequestScore* ctx )
	{
	}
};

int main()
{
	Visitor visitor;
	Request* request = new RequestScore;
	request->accept( &visitor );
	return 0;
}