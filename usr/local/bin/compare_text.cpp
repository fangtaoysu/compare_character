/*
 * @Author: fangtao
 * @Date: 2024-09-02 21:29:09
 * @LastEditors: 18394604239@163.com 18394604239@163.com
 * @LastEditTime: 2024-09-09 11:05:51
 * @FilePath: /compare-character/usr/local/bin/compare_text.cpp
 * @Description: 后端代码
 * 
 * When I switch mode, I can't kown mode in UI, fix it.
I also need a file select button in file mode. and left part and right part can't input anything, click it can select file.
for compare result, when I press button, scrollbar content is unchanged, You need use color to show changed, eg: use colors to highlight missing and added lines and words as specified.
 * Copyright (c) 2024 by fangtao, All Rights Reserved. 
 */
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include <map>

struct CompareResult {
    std::map<size_t, std::string> increase_part;
    std::map<size_t, std::string> decrease_part;
};

std::pair<CompareResult, CompareResult> CompareWordsByLine(const std::string& str1, const std::string& str2) {
    /**
     * 比较两个字符串，返回多出的部分的缺失的部分
    */
    CompareResult res1, res2;
    std::istringstream stream1(str1), stream2(str2);
    std::string line1, line2;
    size_t line_number = 1;

    // 按行处理
    while (std::getline(stream1, line1) && std::getline(stream2, line2)) {
        std::istringstream iss_line1(line1), iss_line2(line2);
        std::string word1, word2;
        std::map<std::string, int> word_count1, word_count2;

        while (iss_line1 >> word1) { word_count1[word1]++; }
        while (iss_line2 >> word2) { word_count2[word2]++; }

        for (const auto& [word, count] : word_count1) {
            if (word_count2[word] < count) { res1.decrease_part[line_number] = word; }
        }

        for (const auto& [word, count] : word_count2) {
            if (word_count1[word] < count) { res2.increase_part[line_number] = word; }
        }

        line_number++;
    }

    // 处理字符串1缺失的行
    while (std::getline(stream1, line1)) {
        std::istringstream iss_line1(line1);
        std::string word1;
        while (iss_line1 >> word1) { res1.decrease_part[line_number] = word1; }
        line_number++;
    }
    // 处理字符串2多出的行
    while (std::getline(stream2, line2)) {
        std::istringstream iss_line2(line2);
        std::string word2;
        while (iss_line2 >> word2) { res2.increase_part[line_number] = word2; }
        line_number++;
    }

    return {res1, res2};
}

int main(int argc, char* argv[]) {
    if (argc == 3) {
        // 处理文件名
        std::ifstream file1(argv[1]), file2(argv[2]);
        if (!file1.is_open() || !file2.is_open()) {
            std::cerr << "Error: Could not open files.\n";
            return 1;
        }

        std::ostringstream buf1, buf2;
        buf1 << file1.rdbuf();
        buf2 << file2.rdbuf();

        auto result = CompareWordsByLine(buf1.str(), buf2.str());

        std::cout << "Words missing in the second text:\n";
        for (const auto& [line, word] : result.first.decrease_part) {
            std::cout << "Line " << line << ": " << word << "\n";
        }

        std::cout << "\nWords added in the second text:\n";
        for (const auto& [line, word] : result.second.increase_part) {
            std::cout << "Line " << line << ": " << word << "\n";
        }

    } else {
        // 处理复制进来的文本
        std::string text1, text2;
        std::cout << "Enter first text followed by the second text:\n";
        std::getline(std::cin, text1);
        std::getline(std::cin, text2);

        auto result = CompareWordsByLine(text1, text2);

        std::cout << "Words missing in the second text:\n";
        for (const auto& [line, word] : result.first.decrease_part) {
            std::cout << "Line " << line << ": " << word << "\n";
        }

        std::cout << "\nWords added in the second text:\n";
        for (const auto& [line, word] : result.second.increase_part) {
            std::cout << "Line " << line << ": " << word << "\n";
        }
    }

    return 0;
}
