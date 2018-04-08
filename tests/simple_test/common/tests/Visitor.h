#ifndef __test_visitor__
#define __test_visitor__

#include "IVisitorRequest.h"


class Acceptor : public mg::IVisitorRequest
{
public:
    Acceptor();

    virtual void visit(mg::Request* ctx) override;
    virtual void visit(mg::RequestFoo* ctx) override;
    virtual void visit(mg::RequestBar* ctx) override;
public:

    bool base;
    bool foo;
    bool bar;
};

bool test_visitor();

#endif