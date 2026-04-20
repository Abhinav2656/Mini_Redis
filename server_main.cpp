#include<iostream>
#include "basic_hashmap.h"
#include "lru_cache.h"
#include<string>
#include<vector>
#include<memory> // for smart pointers
#include<chrono>

int main() {
    //R-E-P-L Engine Read-Eval-Print Loop
    LRUCache db(1000);

    std::string command, key, value;
    while(std::cin >> command){
        // Start the microsecond clock
        auto start_time = std::chrono::high_resolution_clock::now();

        if(command == "SET"){
            std::cin >> key >> value;
            db.put(key, std::make_unique<StringValue>(value));
            
            auto end_time = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time).count();
            
            // Output absolute truth: OK|time
            std::cout << "OK|" << duration << std::endl;
            
        } else if (command == "GET") {
            std::cin >> key;
            IValue* res = db.get(key);
            
            auto end_time = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time).count();
            
            if (res) {
                std::cout << res->serialize() << "|" << duration << std::endl;
            } else {
                std::cout << "NULL|" << duration << std::endl;
            }
            
        // } else if (command == "STATS") {
        //     // NOTE: You must add a simple get_size() and get_capacity() method to your LRUCache class for this to work
        //     // If you haven't, just hardcode the capacity for now to prove the concept.
        //     std::cout << "ARENA_ACTIVE|" << duration << std::endl; 
        } else {
            std::cout << "ERROR_UNKNOWN_COMMAND|0" << std::endl;
        }
    }
    return 0;
}




// int main()
// {
//     HashMap db(10; // create a hashmap with capacity of 10
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
