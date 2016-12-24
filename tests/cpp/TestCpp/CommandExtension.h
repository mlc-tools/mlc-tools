#ifndef __CommandSequenceExtension_h__
#define __CommandSequenceExtension_h__

#include "commands/Command.h"
#include "IntrusivePtr.h"
#include "jsoncpp/json.h"
#include "IntrusivePtr.h"
#include <vector>

IntrusivePtr<mg::Command> createCommand( const Json::Value& json );

#endif