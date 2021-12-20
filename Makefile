CXX = clang++
VM_FILE = lib/libvm.cpp
VM_TARGET = target/libvm.o
SOURCE_MAIN = lib/test_libvm.cpp
TARGET = target/vm
LDFLAGS_COMMON = -std=c++20

all:
	$(CXX) -c $(VM_FILE) $(LDFLAGS_COMMON) -o $(VM_TARGET)
	$(CXX) $(SOURCE_MAIN) $(VM_TARGET) $(LDFLAGS_COMMON) -o $(TARGET)

run:
	./$(TARGET)

clean:
	rm -rf *.o $(TARGET)
