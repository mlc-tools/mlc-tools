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

#include "IntrusivePtr.h"
#include "SerializedObject.h"

void __IntrusivePtr__retain( mg::SerializedObject* ptr )
{
	ptr->retain();
}

void __IntrusivePtr__release( mg::SerializedObject* ptr )
{
	ptr->release();
}

