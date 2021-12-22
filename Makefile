CXX = clang++
TARGET_DIR = target
VM_SRC = cpp/src/libvm.cpp
VM_O = $(TARGET_DIR)/libvm.o
TEST_VM_SRC = cpp/test/test_libvm.cpp
TEST_VM_O = $(TARGET_DIR)/test_libvm.o
TEST_VM_EXECUTABLE = $(TARGET_DIR)/test_vm
LDFLAGS_COMMON = -std=c++17

all:
	$(CXX) -c $(VM_SRC) $(LDFLAGS_COMMON) -o $(VM_O)
	$(CXX) -c $(TEST_VM_SRC) $(LDFLAGS_COMMON) -o $(TEST_VM_O)
	$(CXX) $(VM_O) $(TEST_VM_O) $(LDFLAGS_COMMON) -o $(TEST_VM_EXECUTABLE)

run:
	./$(TEST_VM_EXECUTABLE)

clean:
	rm -rf $(TARGET_DIR)/*.o
