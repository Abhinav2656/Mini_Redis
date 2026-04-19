#pragma once
#include "value_types.h"
#include<string>
#include<memory>
#include<vector>

struct HashNode {
    std::string key;
    std::unique_ptr<IValue> value; // unique_ptr is used to manage the memory of IValue objects
    HashNode* next; //ensuring proper cleanup and preventing memory leaks.

    HashNode (const std::string& data, std::unique_ptr<IValue> v) 
    : key(data), value(std::move(v)), next(nullptr) {}
};

class HashMap { //hashmap has hashnodes, inheritance follows IS-A relation
private:
    std::vector<HashNode*> bucket;
    int capacity;

    int hash(const std::string& key) const {
        int sum =0;
        for(char c: key){
            sum += (int)c;
        }
        return sum%capacity;
    }
    
public:
    HashMap(int cap = 1000) : capacity(cap), bucket(cap, nullptr) {}
    

    void put(const std::string& key, std::unique_ptr<IValue> val){
        int index = hash(key);

        HashNode* node = bucket[index];
        while(node){
            if(node->key == key){ // key already exists, update value
                node->value = std::move(val);  
                return;
            }
            node = node->next;  
        }
        HashNode* newNode = new HashNode(key, std::move(val)); //insert a new node
        newNode->next =  bucket[index]; // attach to head of list
        bucket[index] = newNode;
    }

    IValue* get(const std::string& key) const {
        int index = hash(key);
        HashNode* node = bucket[index];

        while(node){
            if(node->key == key){
                return node->value.get(); // return raw pointer to value
            }
            node = node->next;
        }
        return nullptr;
    }

    bool del(const std::string& key){
        int index = hash(key);
        HashNode* prev = nullptr, *curr = bucket[index];

        while(curr){
            if(curr->key == key){
                if(prev == nullptr) { // deleting head of list
                    bucket[index] = curr->next; // update head to next node
                }
                else{
                    prev->next = curr->next; // bypass current node
                }
                delete curr; // free memory of current node
                return true;
            }
            prev = curr;
            curr = curr->next;
        }
        return false;
    }
};
