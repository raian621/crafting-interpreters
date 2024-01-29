#include <stdio.h>

#include "common.h"
#include "vm.h"
#include "debug.h"

VM vm;

void resetStack() {
  vm.stackTop = vm.stack;
}

void initVM() {
  resetStack();
}

void freeVM() {}

InterpretResult interpret(Chunk* chunk) {
  vm.chunk = chunk;
  vm.ip = vm.chunk->code;
}

static InterpretResult run() {
  #define READ_BYTE() (*vm.ip++)
  #define READ_CONSTANT() (vm.chunk->constants.values[READ_BYTE()])
  #define BINARY_OP(op) \
    do {\
      double a = pop();\
      double b = pop();\
      push(a op b);\
    } while(false);

  for (;;) {
    uint8_t instruction;
    #ifdef DEBUG_TRACE_EXECUTION
    printf("        ");
    for (Value* slot = vm.stack; slot < vm.stackTop; slot++) {
      printf("[ ");
      printValue(*slot);
      printf(" ]");
    }
    printf("\n");
    disassembeInstruction(vm.chunk, (int)(vm.ip - vm.chunk->code));
    #endif
    switch (instruction = READ_BYTE()) {
      case OP_CONSTANT:
        Value constant = READ_CONSTANT();
        push(constant);
        break;
      case OP_NEGATE:
        push(-pop());
        break;
      case OP_ADD:      BINARY_OP(+); break;
      case OP_SUBTRACT: BINARY_OP(-); break;
      case OP_MULTIPLY: BINARY_OP(*); break;
      case OP_DIVIDE:   BINARY_OP(/); break;
      case OP_RETURN:
        printValue(pop());
        printf("\n");
        return INTERPRET_OK;
    }
  }

  #undef BINARY_OP
  #undef READ_CONSTANT
  #undef READ_BYTE
}

void push(Value value) {
  *vm.stackTop = value;
  vm.stackTop++;
}

Value pop() {
  vm.stackTop--;
  return *vm.stackTop;
}