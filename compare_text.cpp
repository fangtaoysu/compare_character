/*
 * @Author: fangtao
 * @Date: 2024-09-02 21:29:09
 * @LastEditors: 18394604239@163.com 18394604239@163.com
 * @LastEditTime: 2024-09-08 11:57:47
 * @FilePath: /compare_character/compare_text.cpp
 * @Description: 实现对文本的逐行比较
 * 
 * Copyright (c) 2024 by fangtao, All Rights Reserved. 
 */
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include <iostream>
#include <map>

// Structure to store comparison results
struct CompareResult {
    std::map<size_t, std::string> increase_part; // Added words and their line numbers
    std::map<size_t, std::string> decrease_part; // Missing words and their line numbers
};

std::pair<CompareResult, CompareResult> CompareWordsByLine(const std::string& str1, const std::string& str2) {
    /**
     * @description: 按行比较两个字符串
     * @return {行号， 单词}
     */    
    CompareResult res1, res2;
    std::istringstream stream1(str1), stream2(str2);
    std::string line1, line2;
    size_t line_number = 1; // Line counter

    // Read lines from both strings
    while (std::getline(stream1, line1) && std::getline(stream2, line2)) {
        std::istringstream iss_line1(line1), iss_line2(line2);
        std::string word1, word2;
        std::map<std::string, int> word_count1, word_count2;

        // Read words from the first line
        while (iss_line1 >> word1) {
            word_count1[word1]++;
        }
        // Read words from the second line
        while (iss_line2 >> word2) {
            word_count2[word2]++;
        }

        // Compare words from line1 to line2
        for (const auto& [word, count] : word_count1) {
            if (word_count2[word] < count) {
                res1.decrease_part[line_number] = word;
            }
        }

        // Compare words from line2 to line1
        for (const auto& [word, count] : word_count2) {
            if (word_count1[word] < count) {
                res2.increase_part[line_number] = word;
            }
        }

        line_number++; // Increment line counter
    }

    // Handle remaining lines if the line counts are unequal
    while (std::getline(stream1, line1)) {
        std::istringstream iss_line1(line1);
        std::string word1;
        while (iss_line1 >> word1) {
            res1.decrease_part[line_number] = word1;
        }
        line_number++;
    }

    while (std::getline(stream2, line2)) {
        std::istringstream iss_line2(line2);
        std::string word2;
        while (iss_line2 >> word2) {
            res2.increase_part[line_number] = word2;
        }
        line_number++;
    }

    return {res1, res2};
}

std::pair<CompareResult, CompareResult> CompareWordsByLine(std::ifstream& file1, std::ifstream& file2) {
    /**
     * @description: 按行比较两个文件
     * @return {行号，单词}
     */    
    CompareResult res1, res2;
    std::string line1, line2;
    size_t line_number = 1;

    // Read lines from both files
    while (std::getline(file1, line1) && std::getline(file2, line2)) {
        // std::cout << line1 << std::endl;
        // std::cout << line2 << std::endl;
        std::istringstream iss_line1(line1), iss_line2(line2);
        std::string word1, word2;
        std::map<std::string, int> word_count1, word_count2;

        // Read words from the first line
        while (iss_line1 >> word1) {
            // std::cout << word1 << std::endl;
            word_count1[word1]++;
        }
        // Read words from the second line
        while (iss_line2 >> word2) {
            // std::cout << word2 << std::endl;
            word_count2[word2]++;
        }

        // Compare words from line1 to line2
        for (const auto& [word, count] : word_count1) {
            if (word_count2[word] < count) {
                res1.decrease_part[line_number] = word;
            }
        }

        // Compare words from line2 to line1
        for (const auto& [word, count] : word_count2) {
            if (word_count1[word] < count) {
                res2.increase_part[line_number] = word;
            }
        }

        line_number++; // Increment line counter
    }

    // Handle remaining lines if the line counts are unequal
    while (std::getline(file1, line1)) {
        std::istringstream iss_line1(line1);
        std::string word1;
        while (iss_line1 >> word1) {
            res1.decrease_part[line_number] = word1;
        }
        line_number++;
    }

    while (std::getline(file2, line2)) {
        std::istringstream iss_line2(line2);
        std::string word2;
        while (iss_line2 >> word2) {
            res2.increase_part[line_number] = word2;
        }
        line_number++;
    }

    return {res1, res2};
}

int main() {
    std::string str1("abc defg\nasdh\nas dd ivuo\nabcd\nabcd eg\naab");
    std::string str2("abc defg\nah\nas ddiv uo\nabcd\nab eg\nab");

    // Compare the two strings
    // auto result = CompareWordsByLine(str1, str2);
    std::ifstream ifs1("/home/fangtao/compare_character/file1.txt"), ifs2("/home/fangtao/compare_character/file2.txt");
    // Check if the files were opened correctly
    if (!ifs1.is_open()) {
        std::cerr << "Error: Could not open file1.txt" << std::endl;
        return 1;
    }
    if (!ifs2.is_open()) {
        std::cerr << "Error: Could not open file2.txt" << std::endl;
        return 1;
    }
    auto result = CompareWordsByLine(ifs1, ifs2);

    // Output results
    std::cout << "Words missing in second string:\n";
    for (const auto& [line, word] : result.first.decrease_part) {
        std::cout << "Line " << line << ": " << word << "\n";
    }

    std::cout << "\nWords added in second string:\n";
    for (const auto& [line, word] : result.second.increase_part) {
        std::cout << "Line " << line << ": " << word << "\n";
    }

    return 0;
}
