#include <cstdlib>
#include <iostream>
#include <ostream>
#include <string>
#include <vector>

#define num long long

int do_step(num number, int depth = 0) {
  if (depth == 75) {
    return 1;
  }
  if (number == 0) {
    return do_step(1, depth + 1);
  } 
  std::string stone_text = std::to_string(number);
  if (stone_text.size() % 2 == 0) {
    num stone_midponum = stone_text.size() / 2;
    std::string a = stone_text.substr(0, stone_midponum);
    std::string b = stone_text.substr(stone_midponum);
    return do_step(std::atoi(a.c_str()), depth + 1) + do_step(std::atoi(b.c_str()), depth + 1);
  }
  return do_step(number * 2024, depth += 1);
}

int main(int argc, char** argv) {
  std::vector<num> stones;
  stones.reserve(argc);
  for (num i = 1; i < argc; i++) {
    stones.push_back(std::atoi(argv[i]));
  }
  
  int acc = 0;
  for (num i = 0; i < stones.size(); i++ ) {
    std::cout << i << "/" << stones.size() << std::endl;
    acc += do_step(stones[i], 0);
  }
  std::cout << "Result: " << acc << std::endl;
}
