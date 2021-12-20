CXX = clang++
CORE_FILE = lib/libcore.cpp
CORE_TARGET = target/libcore.o
SOURCE_MAIN = lib/test_libcore.cpp
TARGET = target/core
LDFLAGS_COMMON = -std=c++20

all:
	$(CXX) -c $(CORE_FILE) $(LDFLAGS_COMMON) -o $(CORE_TARGET)
	$(CXX) $(SOURCE_MAIN) $(CORE_TARGET) $(LDFLAGS_COMMON) -o $(TARGET)

run:
	./$(TARGET)

clean:
	rm -rf *.o $(TARGET)
