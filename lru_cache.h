#pragma once
#include "value_types.h"
#include<unordered_map>
#include<memory>
#include<string>

struct CacheNode{
    std::string key;
    std::unique_ptr<IValue> value;
    CacheNode* prev;
    CacheNode* next;

    CacheNode(const std::string& k, std::unique_ptr<IValue> val) : key(k), value(std::move(val)), prev(nullptr), next(nullptr) {} 
};

class LRUCache{
private:
    int capacity, currentSize;
    std::unordered_map<std::string, CacheNode*> cacheMap;
    CacheNode* head, *tail;

    void addNodeToHead(CacheNode* node){
        node->next = head->next;
        node->prev = head;
        head->next->prev =node;
        head->next =node;
    }

    void removeNode(CacheNode* node){
        CacheNode* p = node->prev;
        CacheNode* n = node->next;
        p->next = n;
        n->prev = p;
    }

public:
    LRUCache(int cap) : capacity(cap), currentSize(0) {
        head = new CacheNode("", nullptr);
        tail = new CacheNode("", nullptr);
        head->next = tail;
        tail->prev = head;
    } 

    IValue* get(const std::string& key){
        if(cacheMap.find(key) == cacheMap.end()){
            return nullptr;
        } else {
            CacheNode* node = cacheMap[key];
            removeNode(node);
            addNodeToHead(node);
            return node->value.get();
        }
    }

    void put(const std::string& key, std::unique_ptr<IValue> value){
        auto it = cacheMap.find(key);
        if(it != cacheMap.end()){
            CacheNode* node = it->second;
            node->value = std::move(value);
            removeNode(node);
            addNodeToHead(node);
            return;
        } 

        if(currentSize == capacity){
            CacheNode* lru = tail->prev;
            cacheMap.erase(lru->key);
            removeNode(lru);
            delete lru;
        } else{
            currentSize++;
        }
        
        CacheNode*newNode = new CacheNode(key, std::move(value));
        addNodeToHead(newNode);
        cacheMap[key] = newNode;
    }

    ~LRUCache(){}
};
