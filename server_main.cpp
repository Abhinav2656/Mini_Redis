#include<iostream>
#include "basic_hashmap.h"
#include "lru_cache.h"
#include<string>
#include<vector>
#include<memory> // for smart pointers

int main() {
    //R-E-P-L Engine Read-Eval-Print Loop
    LRUCache db(100);

    std::string command, key, value;
    while(std::cin >> command){
        if(command == "SET"){
            std::cin >> key >> value;
            db.put(key, std::make_unique<StringValue>(value));
            std::cout << "OK" << std::endl;
        } else if (command == "GET") {
            std::cin >> key;
            IValue* res = db.get(key);
            if (res) {
                std::cout << res->serialize() << std::endl;
            } else {
                std::cout << "NULL" << std::endl;
            }
        } else if(command == "DEL"){
            std::cout<< "Unsupported Command !" << std::endl;
        }else {
            std::cout << "ERROR_UNKNOWN_COMMAND" << std::endl;
        }
    }
    return 0;
}




// int main()
// {
//     HashMap db(10); // create a hashmap with capacity of 10
//     std::cout<< "Mini Redis ENgine Initialized!" << std::endl;

//     db.put("player", std::make_unique<StringValue>("Abhinav"));//insertion using smart pointer to manage memory
//     std::cout<< "Player added!" << std::endl;

//     IValue* result = db.get("player"); // retrieval of value using raw pointer
//     if(result){
//         std::cout << "Retrieved Player : " << result->serialize() << "\n";
//     } else{
//         std:: cout << "Player not found !" << std::endl;
//     }

//     IValue* missing = db.get("user");// trying to retrieve a non-existent key
//     if(!missing){
//         std::cout << "User not found !" << std::endl;
//     }

//     if(db.del("player")){// deletion of key-value pair
//         std::cout << "Player deleted!" << std::endl;
//     }

//     return 0;
// }
