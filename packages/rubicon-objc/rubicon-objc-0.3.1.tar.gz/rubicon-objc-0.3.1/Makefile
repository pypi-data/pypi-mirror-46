OBJ_FILES=tests/objc/Thing.o tests/objc/Example.o tests/objc/BaseExample.o tests/objc/Blocks.o

# By default, build an x86_64 binary.
# Modify here (or on the command line) to build for other architecture(s).
EXTRA_FLAGS=-arch x86_64

all: tests/objc/librubiconharness.dylib

tests/objc/librubiconharness.dylib: $(OBJ_FILES)
	clang -dynamiclib -fobjc-link-runtime $(EXTRA_FLAGS) $(OBJ_FILES) -o tests/objc/librubiconharness.dylib

clean:
	rm -rf tests/objc/*.o tests/objc/*.d tests/objc/librubiconharness.dylib

%.o: %.m tests/objc/*.h
	clang -x objective-c -I./tests/objc -c $(EXTRA_FLAGS) $< -o $@

