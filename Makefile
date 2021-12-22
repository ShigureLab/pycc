CXX = clang++
TARGET_DIR = "target"
VM_SRC = lib/libvm.cpp
VM_O = $(TARGET_DIR)/libvm.o
MAIN_TEST_SRC = lib/test_libvm.cpp
MAIN_TEST_O = $(TARGET_DIR)/test_libvm.o
EXECUTABLE = $(TARGET_DIR)/vm
LDFLAGS_COMMON = -std=c++20

all:
	$(CXX) -c $(VM_SRC) $(LDFLAGS_COMMON) -o $(VM_O)
	$(CXX) -c $(MAIN_TEST_SRC) $(LDFLAGS_COMMON) -o $(MAIN_TEST_O)
	$(CXX) $(VM_O) $(MAIN_TEST_O) $(LDFLAGS_COMMON) -o $(EXECUTABLE)

run:
	./$(EXECUTABLE)

clean:
	rm -rf $(TARGET_DIR)/*.o
