#include <fstream>
#include <iostream>

using namespace std;

ifstream fin("input.txt");
ofstream fout("result.txt");

int main(){
    int n;
    int s = 0;
    fin>>n;
    for(int i=1;i<=n;i++){
        int x;
        fin>>x;
        s += x;
        fout<<s<< '\n';
    }
    return 0;
}