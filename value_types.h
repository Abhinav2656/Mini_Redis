#pragma once
#include<string>

class IValue{
public:
    virtual std::string getType() const = 0 ;
    virtual ~IValue() = default;
    virtual std::string serialize() const = 0;
};

class StringValue : public IValue{
    std::string value;

public:
    StringValue(const std::string& data) : value(data){}

    std::string getType() const override { // const here indicates no modification of member variables
        return "string";
    }
    std::string serialize() const override {
        return value;
    }
};