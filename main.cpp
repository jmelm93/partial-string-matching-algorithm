#include <string>
#include <vector>
#include <fstream>
#include <iostream>

// Compile with: g++ -O3 -o main main.cpp
// Run         : ./main

int main(){
    std::fstream text_file("string_search/test_files/3q_semrush.csv");
    std::fstream patt_file("string_search/test_files/3q_test_bigrams.csv");

    std::vector<std::string> texts;
    std::vector<std::string> patterns;

    std::string line;
    // === Read texts ===
    std::getline(text_file, line, '\n'); // Skip header
    while(std::getline (text_file, line, ',')){
        texts.push_back(line);
        std::getline(text_file, line, '\n');
    }
    // === Read pattern ===
    std::getline(patt_file, line, '\n'); // Skip header
    while(std::getline (patt_file, line, '\n')){
        patterns.push_back(line);
    }
    //std::cout<<"Texts: "<<texts[0]<<"; "<<texts[1]<<"\n";
    //std::cout<<"Patterns: "<<patterns[0]<<"; "<<patterns[1]<<"\n\n";

    // === Init match mtx ===
    std::vector<std::vector<bool>> mtx(patterns.size(), std::vector<bool>(texts.size()));

    int sum = 0;
    for(int p=0;p<patterns.size();p++){
        for(int t=0;t<texts.size();t++){
            if(texts[t].find(patterns[p]) != std::string::npos){
                mtx[p][t] = 1;
                //if(p==0 && sum++<5) std::cout<<patterns[p]<<" ==> "<<texts[t]<<std::endl;
                std::cout<<1;
            }
            else std::cout<<0;
        }
    }


    return 0;
}