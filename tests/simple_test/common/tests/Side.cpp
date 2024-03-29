#include "Side.h"
#include "SideTestBase.h"
#include "SideTestCommon.h"
#include <iostream>

bool test_common()
{
    bool result = true;
    auto base = mg::make_intrusive<mg::SideTestBase>();
    auto common = mg::make_intrusive<mg::SideTestCommon>();

    result = result && base != nullptr;
    result = result && common != nullptr;
    return result;
}


#if BUILD_SIDE == SERVER

#include "SideTestServer.h"

bool test_side()
{
    bool result = true;
    auto server = mg::make_intrusive<mg::SideTestServer>();

    result = result && server != nullptr;
    result = result && test_common();
    if(!result)
        std::cout << "Test side (server) finished with errors" << std::endl;
    return result;
}

#elif BUILD_SIDE == CLIENT

#include "SideTestClient.h"

bool test_side()
{
    bool result = true;
    auto client = mg::make_intrusive<mg::SideTestClient>();

    result = result && client != nullptr;
    result = result && test_common();
    if(!result)
        std::cout << "Test side (client) finished with errors" << std::endl;
    return result;
}

#endif
