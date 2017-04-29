#include <iostream>
#include "Visitor.h"
#include "Request.h"
#include "RequestFoo.h"
#include "RequestBar.h"

Acceptor::Acceptor()
: base(false)
, foo(false)
, bar(false)
{
}

void Acceptor::visit(mg::Request* ctx)
{
    base = true;
}

void Acceptor::visit(mg::RequestFoo* ctx)
{
    foo = true;
}

void Acceptor::visit(mg::RequestBar* ctx)
{
    bar = true;
}


bool test0()
{
    Acceptor acceptor;
    make_intrusive<mg::Request>()->accept(&acceptor);
    auto result = true;
    result = result && acceptor.base;
    result = result && !acceptor.foo;
    result = result && !acceptor.bar;
    return result;
}

bool test1()
{
    Acceptor acceptor;
    make_intrusive<mg::RequestFoo>()->accept(&acceptor);
    auto result = true;
    result = result && !acceptor.base;
    result = result && acceptor.foo;
    result = result && !acceptor.bar;
    return result;
}

bool test2()
{
    Acceptor acceptor;
    make_intrusive<mg::RequestBar>()->accept(&acceptor);
    auto result = true;
    result = result && !acceptor.base;
    result = result && !acceptor.foo;
    result = result && acceptor.bar;
    return result;
}

bool test3()
{
    Acceptor acceptor;
    intrusive_ptr<mg::Request> base = make_intrusive<mg::RequestFoo>();
    base->accept(&acceptor);

    auto result = true;
    result = result && !acceptor.base;
    result = result && acceptor.foo;
    result = result && !acceptor.bar;
    return result;
}

bool test4()
{
    Acceptor acceptor;
    intrusive_ptr<mg::Request> base = make_intrusive<mg::RequestBar>();
    base->accept(&acceptor);

    auto result = true;
    result = result && !acceptor.base;
    result = result && !acceptor.foo;
    result = result && acceptor.bar;
    return result;
}

bool test_visitor()
{
    auto result = true;
    result = result && test0();
    result = result && test1();
    result = result && test2();
    result = result && test3();
    result = result && test4();

    if(!result)
	    std::cout << "Test visitor failed." << std::endl;
    return result;
}
