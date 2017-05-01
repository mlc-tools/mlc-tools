#include "Side.h"
#include "SideTestBase.h"
#include "SideTestCommon.h"
#include <iostream>

bool test_common()
{
    bool result = true;
    auto base = make_intrusive<mg::SideTestBase>();
    auto common = make_intrusive<mg::SideTestCommon>();

    std::cout << "Test side: common get_value = " << common->get_value() << std::endl;

    result = result && base != nullptr;
    result = result && common != nullptr;
    return result;
}


#if BUILD_SIDE == SERVER

#include "SideTestServer.h"

bool test_side()
{
    bool result = true;
    auto server = make_intrusive<mg::SideTestServer>();

    result = result && server != nullptr;
    result = result && test_common();
    std::cout << "Test side (server) finished " << (result ? "success" : "with errors") << std::endl;
    return result;
}

#elif BUILD_SIDE == CLIENT

#include "SideTestClient.h"

bool test_side()
{
    bool result = true;
    auto client = make_intrusive<mg::SideTestClient>();

    result = result && client != nullptr;
    result = result && test_common();
    std::cout << "Test side (client) finished " << (result ? "success" : "with errors") << std::endl;
    return result;
}

#endif