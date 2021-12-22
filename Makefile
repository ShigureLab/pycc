CXX = clang++
TARGET_DIR = "target"
VM_SRC = cpp/src/libvm.cpp
VM_O = $(TARGET_DIR)/libvm.o
TEST_VM_SRC = cpp/test/test_libvm.cpp
TEST_VM_O = $(TARGET_DIR)/test_libvm.o
EXECUTABLE = $(TARGET_DIR)/vm
LDFLAGS_COMMON = -std=c++20

all:
	$(CXX) -c $(VM_SRC) $(LDFLAGS_COMMON) -o $(VM_O)
	$(CXX) -c $(TEST_VM_SRC) $(LDFLAGS_COMMON) -o $(TEST_VM_O)
	$(CXX) $(VM_O) $(TEST_VM_O) $(LDFLAGS_COMMON) -o $(EXECUTABLE)

run:
	./$(EXECUTABLE)

clean:
	rm -rf $(TARGET_DIR)/*.o
