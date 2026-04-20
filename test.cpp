#include <iostream>
#include "lru_cache.h"
#include "basic_hashmap.h"
#include <memory>

int main() {
    LRUCache db(10);
    std::cout << "Setting A..." << std::endl;
    db.put("A", std::make_unique<StringValue>("ValueA"));
    
    std::cout << "Getting A..." << std::endl;
    IValue* res = db.get("A"); // If this hangs, your pointer logic is corrupted.
    
    if(res) std::cout << "Success: " << res->serialize() << std::endl;
    return 0;
}