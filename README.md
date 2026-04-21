# Mini Redis - In-Memory Cache Engine

A lightweight, high-performance in-memory cache system inspired by Redis, built with C++ and exposed through a Python FastAPI web interface. This project demonstrates the core concepts of distributed systems, data structures, and inter-process communication.

---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Execution Steps](#execution-steps)
- [Usage Guide](#usage-guide)
- [Accomplishments](#accomplishments)
- [Future Scope](#future-scope)

---

## 🎯 About the Project

**Mini Redis** is a simplified but functional in-memory key-value store that combines the performance of C++ with the accessibility of Python. It implements an LRU (Least Recently Used) cache eviction policy to manage memory efficiently and provides a real-time web dashboard for interaction.

### Motivation & Reasoning

This project was created to:

1. **Deep dive into data structures**: Understand how hash maps and doubly-linked lists work under the hood
2. **Learn LRU caching**: Implement efficient cache replacement policies with O(1) operations
3. **Master inter-process communication**: Bridge C++ and Python using pipes and subprocess communication
4. **Build a full-stack system**: Create both backend logic and user-facing interface
5. **Understand performance optimization**: Measure and optimize operation latency at the microsecond level

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────┐
│   Web Browser (HTML/JavaScript UI)  │
└────────────────┬────────────────────┘
                 │
                 │ HTTP/REST API
                 ▼
┌─────────────────────────────────────┐
│  FastAPI Python Server (server.py)  │
│   - API Endpoints (SET, GET, MSET)  │
│   - Web Dashboard                   │
│   - Request/Response Handling       │
└────────────────┬────────────────────┘
                 │
                 │ IPC (stdin/stdout pipes)
                 ▼
┌─────────────────────────────────────┐
│  C++ REPL Engine (server_main.cpp)  │
│   - Command Parser                  │
│   - Operation Execution             │
│   - Latency Measurement             │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│      LRU Cache (lru_cache.h)        │
│  ┌──────────────────────────────┐   │
│  │ Doubly-Linked List (DLL)     │   │
│  │ Head ↔ Node ↔ Node ↔ Tail   │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │ Hash Map (O(1) Lookup)       │   │
│  │ [key] → CacheNode*           │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

### Component Details

#### 1. **LRU Cache** (`lru_cache.h`)

- **Data Structure**: Doubly-Linked List + Hash Map
- **Capacity**: Configurable (default: 1000 nodes)
- **Operations**:
  - `put(key, value)`: Insert or update with O(1) complexity
  - `get(key)`: Retrieve value and mark as recently used with O(1) complexity
  - LRU eviction: When capacity exceeded, removes least recently used node
- **Key Feature**: Recently accessed nodes move to head; least used moves to tail

#### 2. **Value Type System** (`value_types.h`)

- **Abstract Interface**: `IValue` with virtual methods
- **Concrete Implementation**: `StringValue` for string data
- **Extensible Design**: Easy to add other types (int, list, hash, set)
- **Serialization**: `serialize()` method for data conversion

#### 3. **Hash Map** (`basic_hashmap.h`)

- **Collision Resolution**: Chaining (linked list per bucket)
- **Hash Function**: Sum of ASCII values modulo capacity
- **Capacity**: Configurable (default: 1000)
- **Operations**:
  - `put(key, value)`: Insert/update with O(1) average
  - `get(key)`: Lookup with O(1) average
  - `del(key)`: Delete with O(1) average

#### 4. **Python FastAPI Server** (`server.py`)

- **Communication**: Subprocess IPC with pipes
- **Endpoints**:
  - `/`: Web dashboard UI
  - `/set`: Single SET operation
  - `/get`: Single GET operation
  - `/mset`: Batch SET operation
- **Features**:
  - Real-time latency reporting
  - Input validation and error handling
  - Terminal-like web interface

#### 5. **C++ REPL Engine** (`server_main.cpp`)

- **Loop Model**: Continuous read-eval-print loop
- **Commands**: SET, GET with microsecond timing
- **Output Format**: `RESULT|LATENCY_MICROSECONDS`
- **Performance**: Measures execution time for each operation

---

## 📁 Project Structure

```
Practice/
├── server_main.cpp          # C++ REPL engine with command parser
├── server.py                # Python FastAPI web server
├── lru_cache.h              # LRU cache implementation
├── basic_hashmap.h          # Hash map with chaining
├── value_types.h            # Type system (IValue interface)
├── test.cpp                 # Unit tests for cache operations
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container configuration
└── README.md               # Project documentation
```

---

## 💻 Tech Stack

| Layer                | Technology                 | Purpose                  |
| -------------------- | -------------------------- | ------------------------ |
| **Frontend**         | HTML5, JavaScript, CSS     | Web Dashboard UI         |
| **Backend API**      | Python 3.10, FastAPI       | REST API & Server        |
| **Backend Engine**   | C++17, STL                 | Core Data Structures     |
| **Communication**    | Subprocess IPC, Pipes      | Python ↔ C++ Bridge      |
| **Containerization** | Docker                     | Deployment & Portability |
| **Dependencies**     | FastAPI, Uvicorn, Pydantic | Python packages          |

---

## 🚀 Execution Steps

### Prerequisites

- **Linux/macOS**: G++ compiler, Python 3.10+
- **Windows**: MinGW/Visual Studio compiler, Python 3.10+
- **Docker** (optional): For containerized deployment

### Method 1: Local Execution

#### Step 1: Compile C++ Engine

```bash
cd c:\Users\abhin\OneDrive\Desktop\Practice
g++ -o mini_redis server_main.cpp -std=c++17
```

#### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Run the FastAPI Server

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

#### Step 4: Access the Web Dashboard

```
Open browser: http://localhost:8000
```

### Method 2: Docker Execution

#### Step 1: Build Docker Image

```bash
docker build -t mini-redis:latest .
```

#### Step 2: Run Container

```bash
docker run -p 8000:8000 mini-redis:latest
```

#### Step 3: Access the Web Dashboard

```
Open browser: http://localhost:8000
```

### Method 3: Testing Only

#### Run Unit Tests

```bash
g++ -o test_runner test.cpp -std=c++17
./test_runner
```

---

## 📖 Usage Guide

### Web Dashboard Interface

#### Single SET Operation

1. Enter **Key** (e.g., `player`)
2. Enter **Value** (e.g., `Abhinav`)
3. Click **SET** button
4. Response: `OK|<latency_microseconds>`

#### Single GET Operation

1. Enter **Key** (e.g., `player`)
2. Leave **Value** empty
3. Click **GET** button
4. Response: `<value>|<latency_microseconds>` or `NULL|<latency_microseconds>`

#### Batch SET Operation (Multiple Key-Value Pairs)

1. Enter **Keys** (comma-separated, e.g., `key1,key2,key3`)
2. Enter **Values** (comma-separated, e.g., `val1,val2,val3`)
3. Click **SET** button
4. Validation:
   - Equal number of keys and values required
   - No spaces allowed within individual items
   - Response: `OK|<batch_latency_microseconds>`

#### Terminal Output

- Real-time execution logs with timestamps
- Error messages for invalid operations
- Latency metrics for performance analysis
- System status messages

### Direct API Calls (Using cURL)

#### SET Operation

```bash
curl -X POST http://localhost:8000/set \
  -H "Content-Type: application/json" \
  -d '{"key":"mykey", "value":"myvalue"}'
```

#### GET Operation

```bash
curl -X GET http://localhost:8000/get?key=mykey
```

#### Batch SET Operation

```bash
curl -X POST http://localhost:8000/mset \
  -H "Content-Type: application/json" \
  -d '{"items":[{"key":"k1","value":"v1"},{"key":"k2","value":"v2"}]}'
```

---

## ✅ Accomplishments

### 1. **Core Data Structures**

- ✅ Implemented LRU Cache from scratch using doubly-linked list + hash map
- ✅ Built custom hash map with collision handling via chaining
- ✅ Achieved O(1) average time complexity for GET, PUT, DELETE operations

### 2. **Type System**

- ✅ Designed extensible value type system using polymorphism (IValue interface)
- ✅ Implemented StringValue concrete type
- ✅ Created serialization mechanism for type-agnostic data handling

### 3. **Performance**

- ✅ Measured and logged operation latency in microseconds
- ✅ Optimized cache operations for sub-millisecond performance
- ✅ Implemented efficient memory management with smart pointers

### 4. **Inter-Process Communication**

- ✅ Established bidirectional communication between Python and C++ via subprocess pipes
- ✅ Implemented command parsing and response formatting protocol
- ✅ Handled concurrent requests through IPC bridge

### 5. **Full-Stack Integration**

- ✅ Created responsive web dashboard with real-time terminal UI
- ✅ Built REST API endpoints using FastAPI framework
- ✅ Implemented input validation and error handling at multiple levels
- ✅ Added batch operation support with safety shields

### 6. **Deployment**

- ✅ Created production-ready Dockerfile
- ✅ Configured multi-stage compilation and deployment
- ✅ Ensured cross-platform compatibility

---

## 🔮 Future Scope

### 1. **Extended Data Types**

- [ ] **Integer Type**: `IntValue` for numeric data with increment/decrement operations
- [ ] **List Type**: `ListValue` for ordered collections with PUSH, POP, INDEX operations
- [ ] **Hash Type**: `HashValue` for nested key-value pairs with HGET, HSET operations
- [ ] **Set Type**: `SetValue` for unique collections with ADD, REMOVE, CONTAINS operations

### 2. **Advanced Caching Strategies**

- [ ] **LFU Cache**: Least Frequently Used eviction policy as alternative to LRU
- [ ] **TTL Support**: Time-to-live for automatic key expiration
- [ ] **Cache Preloading**: Bulk import data from files
- [ ] **Warm-up Strategies**: Intelligent cache priming

### 3. **Persistence Layer**

- [ ] **Disk Persistence**: Save cache state to disk (RDB format)
- [ ] **Write-Ahead Logging (WAL)**: Journaling for durability
- [ ] **Recovery Mechanism**: Restore cache from persisted state on startup
- [ ] **Snapshot Export**: Export cache contents to JSON/binary format

### 4. **Cluster & Replication**

- [ ] **Multi-node Support**: Distributed cache across multiple servers
- [ ] **Replication**: Master-slave replication for high availability
- [ ] **Sharding**: Horizontal partitioning of data
- [ ] **Consensus Protocol**: Raft or similar for distributed consistency

### 5. **Advanced Features**

- [ ] **Pub/Sub Messaging**: Publish-subscribe pattern for real-time updates
- [ ] **Transactions**: MULTI/EXEC with ACID guarantees
- [ ] **Lua Scripting**: Execute custom scripts on server
- [ ] **Geospatial Queries**: Support for location-based operations

### 6. **Performance Enhancements**

- [ ] **Lock-free Data Structures**: Concurrent access optimization
- [ ] **Memory Pooling**: Reduce allocation overhead
- [ ] **Adaptive Eviction**: Machine learning-based eviction predictions
- [ ] **Hardware Acceleration**: SIMD operations for faster hashing

### 7. **Monitoring & Observability**

- [ ] **STATS Endpoint**: Detailed cache statistics (hit rate, miss rate, evictions)
- [ ] **Prometheus Metrics**: Export metrics for monitoring systems
- [ ] **Health Checks**: Endpoint for load balancer health probes
- [ ] **Slow Query Logging**: Track slow operations for optimization

### 8. **Security**

- [ ] **Authentication**: User credentials for access control
- [ ] **Authorization**: Role-based access control (RBAC)
- [ ] **Encryption**: TLS for data in transit, encryption at rest
- [ ] **Rate Limiting**: Prevent abuse and DDoS attacks

### 9. **Developer Experience**

- [ ] **CLI Client**: Command-line tool for Redis-like interaction
- [ ] **Admin Dashboard**: Advanced monitoring and management UI
- [ ] **Configuration File**: YAML/JSON config for server settings
- [ ] **Benchmarking Tools**: Performance testing utilities

### 10. **Testing & Documentation**

- [ ] **Comprehensive Unit Tests**: Full test coverage for all components
- [ ] **Integration Tests**: Cross-component interaction validation
- [ ] **Stress Tests**: Performance under high load scenarios
- [ ] **API Documentation**: OpenAPI/Swagger spec with examples
- [ ] **Architecture Diagrams**: Visual documentation of system design

---

## 🔧 How to Extend

### Adding a New Data Type

1. **Extend `value_types.h`**:

   ```cpp
   class IntValue : public IValue {
       int value;
   public:
       IntValue(int v) : value(v) {}
       std::string getType() const override { return "int"; }
       std::string serialize() const override { return std::to_string(value); }
       int getValue() const { return value; }
   };
   ```

2. **Update `server_main.cpp`** to handle the new type in SET/GET operations

3. **Test** with the test suite

### Adding a New Cache Strategy

1. **Create new header file** (e.g., `lfu_cache.h`) similar to `lru_cache.h`
2. **Implement the new eviction policy** in the template class
3. **Update `server_main.cpp`** to support switching between strategies
4. **Benchmark** against LRU implementation

---

## 📊 Performance Characteristics

| Operation       | Time Complexity | Space Complexity | Notes                           |
| --------------- | --------------- | ---------------- | ------------------------------- |
| GET             | O(1) average    | O(1)             | Hash map lookup + DLL traversal |
| PUT (new)       | O(1) average    | O(1)             | Insert at head, hash map entry  |
| PUT (update)    | O(1) average    | O(1)             | Move to head, update value      |
| DELETE/Eviction | O(1)            | O(1)             | Remove node, erase from map     |
| **Total**       | **O(1) per op** | **O(capacity)**  | Bounded by cache capacity       |

---

## 📝 License

This project is provided as-is for educational purposes.

---

## 👤 Author

Built as a learning project to master data structures, system design, and inter-process communication.

---

## 📞 Support

For issues or questions:

1. Check the Architecture section for design details
2. Review code comments in header files
3. Run test.cpp to validate setup
4. Monitor browser console and server logs for debugging

---

**Happy Caching! 🚀**
