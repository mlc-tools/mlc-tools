#include "IntrusivePtr.h"
#include <assert.h>
#include "SerializedObject.h"


void __IntrusivePtr__retain( mg::SerializedObject* ptr )
{
	ptr->retain();
}

void __IntrusivePtr__release( mg::SerializedObject* ptr )
{
	ptr->release();
}
