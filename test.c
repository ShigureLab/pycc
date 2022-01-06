int main() {
  int a;
  int i;

  i = 0;
  a = 0;
  while (i < 10) {
    a = a + i;
    i = i + 1;
  }
  return a;
}

// int fibonacci(int i) {
//   if (i <= 1) {
//     return 1;
//   }
//   return fibonacci(i - 1) + fibonacci(i - 2);
// }

// int main() {
//   int i;
//   i = 0;
//   return fibonacci(10);
// }
